// Ověří, že každá kalkulačka s výchozími hodnotami vrací konečná čísla a že JSON má všechna pole.
const fs = require('fs'), path = require('path');
const dir = path.join(__dirname, '..', 'content');
let bad = 0;
for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.json'))) {
  const slug = f.slice(0, -5);
  const meta = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'));
  for (const k of ['category','h1','title','description','lead','inputs','article','faq'])
    if (!meta[k]) { console.log(`${slug}: chybí pole ${k}`); bad++; }
  const js = fs.readFileSync(path.join(dir, slug + '.js'), 'utf8');
  const calc = new Function(js + '; return calc;')();
  const v = {}; meta.inputs.forEach(i => v[i.id] = Number(i.default));
  const out = calc(v);
  if (!Array.isArray(out) || !out.length) { console.log(`${slug}: calc nevrací pole`); bad++; continue; }
  for (const r of out) if (typeof r.value === 'number' && !isFinite(r.value)) { console.log(`${slug}: ${r.label} = ${r.value}`); bad++; }
  console.log(`${slug}: OK – ${out.map(r => r.label + ' ' + r.value).join(' | ')}`);
}
if (bad) { console.log(`CHYBY: ${bad}`); process.exit(1); }
