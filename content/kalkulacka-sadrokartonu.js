function calc(v){
  var a = v.delka * v.vyska;
  var sides = 2 * v.vrstvy;
  var boards = Math.ceil(a * sides * 1.1 / v.deska);
  var cw = Math.ceil(v.delka / (v['rozteč']/100)) + 1;
  var uw = Math.ceil(2 * v.delka / 4);
  return [
    {label:'Sádrokartonové desky', value: boards, unit:'ks', main:true},
    {label:'Profily CW (délka ≥ ' + v.vyska.toLocaleString('cs-CZ') + ' m)', value: cw, unit:'ks'},
    {label:'Profily UW (délka 4 m)', value: uw, unit:'ks'},
    {label:'Šrouby do SDK', value: Math.ceil(a * sides * 15 / 100) * 100, unit:'ks'},
    {label:'Spárovací tmel', value: Math.ceil(a * 2 * 0.35), unit:'kg'},
    {label:'Minerální izolace', value: Math.ceil(a), unit:'m²'}
  ];
}
