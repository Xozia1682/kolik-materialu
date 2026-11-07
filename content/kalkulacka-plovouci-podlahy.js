function calc(v){
  var a = v.delka * v.sirka;
  var need = a * (1 + v.prorez/100);
  var perim = 2*(v.delka + v.sirka) - v.dvere*0.9;
  return [
    {label:'Počet balení', value: Math.ceil(need / v.baleni), unit:'bal.', main:true},
    {label:'Plocha místnosti', value: a, unit:'m²'},
    {label:'Podlaha včetně prořezu', value: need, unit:'m²'},
    {label:'Podložka', value: Math.ceil(a * 1.05), unit:'m²'},
    {label:'Soklové lišty 2,5 m', value: Math.ceil(perim / 2.5) + 1, unit:'ks'}
  ];
}
