function calc(v){
  var a = v.plocha * (1 + v.prorez/100);
  var tile = (v.delka/100) * (v.sirka/100);
  var L = v.delka*10, W = v.sirka*10;
  var grout = (L + W) / (L * W) * v.spara * v.tloustka * 1.6 * v.plocha;
  var glue = v.plocha * v.lepidlo;
  return [
    {label:'Počet balení', value: Math.ceil(a / v.baleni), unit:'bal.', main:true},
    {label:'Plocha včetně prořezu', value: a, unit:'m²'},
    {label:'Počet dlaždic', value: Math.ceil(a / tile), unit:'ks'},
    {label:'Lepidlo', value: Math.ceil(glue), unit:'kg'},
    {label:'= pytlů lepidla 25 kg', value: Math.ceil(glue/25), unit:'ks'},
    {label:'Spárovací hmota', value: Math.max(grout, 0.1), unit:'kg'}
  ];
}
