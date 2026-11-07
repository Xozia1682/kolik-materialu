# Pokyny pro týdenní automatickou úlohu (Claude)

Cíl: každý týden přidat na web 2 nové kalkulačky, aby web rostl ve vyhledávání Google a Seznam.

## Postup
1. Vezmi první 2 položky ze sekce „Na řadě“ v `BACKLOG.md`.
2. Pro každou vytvoř `content/<slug>.json` a `content/<slug>.js` podle vzoru existujících kalkulaček:
   - JSON: `category` (hruba-stavba | povrchy | malovani | zahrada; nová kategorie se musí přidat do `CATEGORIES` v build.py), `h1`, `title` (do 65 znaků, obsahuje hlavní hledaný výraz), `description` (do 160 znaků), `lead`, `inputs`, `article` (HTML, 350–600 slov, alespoň 2× `<h2>`, ideálně tabulka s typickými hodnotami), `faq` (3–4 otázky, jak je lidé skutečně hledají).
   - JS: funkce `calc(v)` vracející pole `{label, value, unit, main?}`; první výsledek s `main:true`.
   - Texty piš přirozenou spisovnou češtinou, věcně správně, s hodnotami spotřeby podle běžných údajů výrobců. Žádné vymyšlené statistiky ani odkazy.
3. Spusť `node scripts/check.js` a `python3 build.py`. Obojí musí projít bez chyby.
4. Přesuň položky v `BACKLOG.md` do „Hotovo“. Když v „Na řadě“ zbývají méně než 4 položky, doplň nové nápady na kalkulačky, které lidé v Česku hledají při stavbě, rekonstrukci a na zahradě.
5. Commitni a pushni do větve `main` (Cloudflare Pages web automaticky nasadí).

## Nikdy
- neměň `site.json` (AdSense, doména), stránku ochrany soukromí ani existující URL (slugy);
- nemaž existující kalkulačky;
- nepřidávej externí skripty kromě AdSense.
