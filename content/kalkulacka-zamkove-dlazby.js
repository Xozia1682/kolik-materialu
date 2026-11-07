function calc(v){
  var gravel = v.plocha * (v.podklad/100) * 1.6 * 1.2;
  var bed = v.plocha * (v.loze/100) * 1.6;
  return [
    {label:'Zámková dlažba', value: Math.ceil(v.plocha * (1 + v.prorez/100) * 10)/10, unit:'m²', main:true},
    {label:'Štěrkodrť 0–32 mm (podklad)', value: gravel, unit:'t'},
    {label:'Drť 4–8 mm (lože)', value: bed, unit:'t'},
    {label:'Obrubníky 1 m', value: Math.ceil(v.obvod), unit:'ks'},
    {label:'Beton pod obrubníky', value: v.obvod * 0.05, unit:'m³'},
    {label:'Geotextilie', value: Math.ceil(v.plocha * 1.1), unit:'m²'}
  ];
}
