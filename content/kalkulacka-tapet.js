function calc(v){
  var strip = v.vyska + v.strida/100 + 0.05;
  var perRoll = Math.floor(v.delkarole / strip);
  var strips = Math.ceil(v.sirkasteny / v.sirkarole);
  if (perRoll < 1) return [{label:'Role je kratší než výška stěny', value:'—', unit:'', main:true}];
  return [
    {label:'Počet rolí', value: Math.ceil(strips / perRoll), unit:'ks', main:true},
    {label:'Počet pruhů', value: strips, unit:'ks'},
    {label:'Pruhů z jedné role', value: perRoll, unit:'ks'},
    {label:'Plocha stěn', value: v.sirkasteny * v.vyska, unit:'m²'}
  ];
}
