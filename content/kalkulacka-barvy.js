function calc(v){
  var walls = 2*(v.delka + v.sirka)*v.vyska - v.otvory;
  var ceil = v.strop == 1 ? v.delka*v.sirka : 0;
  var area = Math.max(walls + ceil, 0);
  var paint = area * v.vrstvy / v.vydatnost;
  return [
    {label:'Barva', value: Math.ceil(paint*10)/10, unit:'l', main:true},
    {label:'Plocha k malování', value: area, unit:'m²'},
    {label:'z toho stěny', value: Math.max(walls,0), unit:'m²'},
    {label:'z toho strop', value: ceil, unit:'m²'},
    {label:'Penetrace (koncentrát)', value: Math.ceil(area/30*10)/10, unit:'l'}
  ];
}
