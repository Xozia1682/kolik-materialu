function calc(v){
  var vol = v.delka * v.sirka * (v.tloustka/100) * v.pocet * (1 + v.rezerva/100);
  return [
    {label:'Objem betonu', value: vol, unit:'m³', main:true},
    {label:'Suchá betonová směs (pytle 25 kg)', value: Math.ceil(vol*2100/25), unit:'ks'},
    {label:'nebo cement (pytle 25 kg)', value: Math.ceil(vol*300/25), unit:'ks'},
    {label:'+ štěrkopísek 0–16 mm', value: vol*1.9, unit:'t'},
    {label:'+ voda', value: Math.round(vol*170), unit:'l'}
  ];
}
