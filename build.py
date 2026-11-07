#!/usr/bin/env python3
"""Generuje statický web z content/*.json (+ content/*.js) do složky dist/.

Každá kalkulačka = dva soubory:
  content/<slug>.json  – texty, vstupy, FAQ
  content/<slug>.js    – funkce calc(v), která vrací [{label, value, unit, main?}]
"""
import json, html, shutil, datetime, pathlib, re

ROOT = pathlib.Path(__file__).parent
DIST = ROOT / "dist"
SITE = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
TODAY = datetime.date.today().isoformat()
E = html.escape

CATEGORIES = {
    "hruba-stavba": "Hrubá stavba",
    "povrchy": "Podlahy a obklady",
    "malovani": "Malování a stěny",
    "zahrada": "Zahrada a venkovní úpravy",
}


def load_calcs():
    calcs = []
    for f in sorted((ROOT / "content").glob("*.json")):
        c = json.loads(f.read_text(encoding="utf-8"))
        c["slug"] = f.stem
        c["js"] = (ROOT / "content" / f"{f.stem}.js").read_text(encoding="utf-8")
        calcs.append(c)
    return calcs


def ads_head():
    cid = SITE.get("adsense_client")
    if not cid:
        return ""
    return (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={E(cid)}" '
            'crossorigin="anonymous"></script>')


def ad_slot():
    if not SITE.get("adsense_client"):
        return ""
    return ('<div class="ad"><ins class="adsbygoogle" style="display:block" data-ad-format="auto" '
            'data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({});</script></div>')


def page(title, description, path, body, extra_head=""):
    canonical = SITE["base_url"].rstrip("/") + path
    return f"""<!doctype html>
<html lang="{SITE['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(description)}">
<link rel="canonical" href="{E(canonical)}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(description)}">
<meta property="og:type" content="website">
<link rel="stylesheet" href="/style.css">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{ads_head()}
{extra_head}
</head>
<body>
<header class="top"><div class="wrap"><a class="logo" href="/">📐 {E(SITE['name'])}</a>
<nav><a href="/">Kalkulačky</a><a href="/o-webu/">O webu</a></nav></div></header>
<main class="wrap">
{body}
</main>
<footer><div class="wrap">
<p>© {datetime.date.today().year} {E(SITE['name'])}. Výpočty jsou orientační – před nákupem si ověřte údaje výrobce materiálu.</p>
<p><a href="/o-webu/">O webu</a> · <a href="/ochrana-soukromi/">Ochrana soukromí</a> · <a href="mailto:{E(SITE['contact_email'])}">Kontakt</a></p>
</div></footer>
</body>
</html>
"""


def calc_page(c, calcs):
    inputs = []
    for i in c["inputs"]:
        if i.get("type") == "select":
            opts = "".join(
                f'<option value="{E(str(o["value"]))}"{" selected" if o["value"] == i.get("default") else ""}>{E(o["label"])}</option>'
                for o in i["options"])
            field = f'<select id="{E(i["id"])}">{opts}</select>'
        else:
            field = (f'<input id="{E(i["id"])}" type="number" inputmode="decimal" value="{E(str(i["default"]))}" '
                     f'step="{E(str(i.get("step", "any")))}" min="{E(str(i.get("min", 0)))}">')
        unit = f'<span class="unit">{E(i.get("unit", ""))}</span>' if i.get("unit") else ""
        hint = f'<small>{E(i["hint"])}</small>' if i.get("hint") else ""
        inputs.append(f'<label><span class="lbl">{E(i["label"])}</span><span class="field">{field}{unit}</span>{hint}</label>')

    ids = json.dumps([i["id"] for i in c["inputs"]])
    faq_html = "".join(f"<details><summary>{E(f['q'])}</summary><p>{E(f['a'])}</p></details>" for f in c.get("faq", []))
    faq_ld = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
                       for f in c.get("faq", [])]}
    related = [x for x in calcs if x["slug"] != c["slug"]]
    related.sort(key=lambda x: x.get("category") != c.get("category"))
    rel_html = "".join(f'<li><a href="/{x["slug"]}/">{E(x["h1"])}</a></li>' for x in related[:5])

    body = f"""
<nav class="crumbs"><a href="/">Kalkulačky</a> › {E(CATEGORIES.get(c.get('category'), ''))}</nav>
<h1>{E(c['h1'])}</h1>
<p class="lead">{E(c['lead'])}</p>
<section class="calc" id="calc">
<form onsubmit="return false">{''.join(inputs)}</form>
<div class="results" id="results" aria-live="polite"></div>
</section>
{ad_slot()}
<article class="text">{c['article']}</article>
{('<section class="faq"><h2>Časté otázky</h2>' + faq_html + '</section>') if faq_html else ''}
{ad_slot()}
<section class="related"><h2>Další kalkulačky</h2><ul>{rel_html}</ul></section>
<script>
{c['js']}
(function(){{
  var ids = {ids};
  var fmt = new Intl.NumberFormat('cs-CZ', {{maximumFractionDigits: 2}});
  function run(){{
    var v = {{}};
    ids.forEach(function(id){{ var el=document.getElementById(id); var n=parseFloat(String(el.value).replace(',','.')); v[id]=isNaN(n)?el.value:n; }});
    var out;
    try {{ out = calc(v); }} catch(e) {{ out = []; }}
    document.getElementById('results').innerHTML = out.map(function(r){{
      var val = typeof r.value === 'number' ? fmt.format(r.value) : r.value;
      return '<div class="res'+(r.main?' main':'')+'"><span>'+r.label+'</span><b>'+val+' '+(r.unit||'')+'</b></div>';
    }}).join('');
  }}
  ids.forEach(function(id){{ document.getElementById(id).addEventListener('input', run); }});
  run();
}})();
</script>
"""
    return page(c["title"], c["description"], f"/{c['slug']}/", body,
                f'<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>')


def index_page(calcs):
    groups = []
    for key, name in CATEGORIES.items():
        items = [c for c in calcs if c.get("category") == key]
        if not items:
            continue
        lis = "".join(f'<li><a href="/{c["slug"]}/"><b>{E(c["h1"])}</b><span>{E(c["lead"])}</span></a></li>' for c in items)
        groups.append(f'<h2>{E(name)}</h2><ul class="cards">{lis}</ul>')
    body = f"""<h1>{E(SITE['tagline'])}</h1>
<p class="lead">Zadejte rozměry a hned uvidíte, kolik betonu, dlažby, barvy nebo jiného materiálu potřebujete – včetně rezervy na prořez. Zdarma a bez registrace.</p>
{ad_slot()}
{''.join(groups)}"""
    return page(f"{SITE['name']} – stavební kalkulačky materiálu zdarma",
                "Spočítejte si spotřebu betonu, dlažby, barvy, tapet, sádrokartonu a dalších materiálů. Bezplatné online kalkulačky pro stavbu a rekonstrukci.",
                "/", body)


def static_pages():
    about = f"""<h1>O webu</h1>
<p>{E(SITE['name'])} je sbírka jednoduchých kalkulaček, které pomáhají při stavbě, rekonstrukci a práci na zahradě.
Cílem je, abyste nekupovali zbytečně moc materiálu – ani nemuseli kvůli chybějícímu pytli znovu do stavebnin.</p>
<p>Výpočty vycházejí z běžných hodnot spotřeby uváděných výrobci. Skutečná spotřeba se může lišit podle konkrétního výrobku
a podkladu, proto vždy zkontrolujte údaje na obalu.</p>
<p>Našli jste chybu nebo vám chybí kalkulačka? Napište na <a href="mailto:{E(SITE['contact_email'])}">{E(SITE['contact_email'])}</a>.</p>"""
    privacy = f"""<h1>Ochrana soukromí</h1>
<p>Tento web neukládá žádné údaje, které do kalkulaček zadáte – výpočet probíhá jen ve vašem prohlížeči.</p>
<p>Web může zobrazovat reklamu Google AdSense. Google a jeho partneři mohou používat soubory cookie k zobrazování reklam
na základě vašich předchozích návštěv tohoto a jiných webů. Souhlas s cookies můžete udělit nebo odmítnout v liště při první návštěvě
a personalizovanou reklamu vypnout v <a href="https://adssettings.google.com/" rel="nofollow">nastavení reklam Google</a>.
Více informací: <a href="https://policies.google.com/technologies/partner-sites" rel="nofollow">Jak Google používá data</a>.</p>
<p>Některé odkazy mohou být partnerské – pokud přes ně nakoupíte, můžeme získat provizi, vás to nic nestojí.</p>
<p>Kontakt: <a href="mailto:{E(SITE['contact_email'])}">{E(SITE['contact_email'])}</a></p>"""
    return {
        "o-webu": page(f"O webu – {SITE['name']}", "Informace o webu s bezplatnými stavebními kalkulačkami.", "/o-webu/", about),
        "ochrana-soukromi": page(f"Ochrana soukromí – {SITE['name']}", "Zásady ochrany soukromí a cookies.", "/ochrana-soukromi/", privacy),
    }


def main():
    calcs = load_calcs()
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(ROOT / "static", DIST)
    (DIST / "index.html").write_text(index_page(calcs), encoding="utf-8")
    for c in calcs:
        d = DIST / c["slug"]
        d.mkdir()
        (d / "index.html").write_text(calc_page(c, calcs), encoding="utf-8")
    for slug, content in static_pages().items():
        d = DIST / slug
        d.mkdir()
        (d / "index.html").write_text(content, encoding="utf-8")
    base = SITE["base_url"].rstrip("/")
    urls = ["/", "/o-webu/", "/ochrana-soukromi/"] + [f"/{c['slug']}/" for c in calcs]
    sm = "".join(f"<url><loc>{base}{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls)
    (DIST / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>',
        encoding="utf-8")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n", encoding="utf-8")
    if SITE.get("adsense_pub_id"):
        (DIST / "ads.txt").write_text(f"google.com, {SITE['adsense_pub_id']}, DIRECT, f08c47fec0942fa0\n", encoding="utf-8")
    print(f"OK: {len(calcs)} kalkulaček, {len(urls)} stránek → {DIST}")


if __name__ == "__main__":
    main()
