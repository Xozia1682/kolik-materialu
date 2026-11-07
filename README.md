# Kolik materiálu

Statický web s bezplatnými stavebními kalkulačkami (čeština). Generuje se skriptem `build.py` z `content/` do `dist/`.

- Build: `python3 build.py` (Cloudflare Pages: build command `python3 build.py`, output `dist`)
- Kontrola: `node scripts/check.js`
- Automatické přidávání obsahu: viz `AUTOMATION.md` a `BACKLOG.md`
- Reklama: po schválení AdSense vyplňte `adsense_client` (ca-pub-…) a `adsense_pub_id` (pub-…) v `site.json`
