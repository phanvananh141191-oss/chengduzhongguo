/* ===== ULAY · bộ gom bài cho 汉语口语 (KY) ===== */
(function(){
var A=ULAY.arr;
function T(n){return ULAY.txt(n).replace(/\s+/g,' ').trim()}
var ACT=/^(牛刀小试|[A-G][\s\.．、 ]|任务支持|任务选择|任务[一二三四五六七八九十]|小词库)/;
function groupBy(nodes,isStart){
  var out=[],g=null;
  nodes.forEach(function(n){
    var h=n.nodeType===1&&/^H[1-6]$/.test(n.tagName);
    if(h){g=null;out.push(n);return}
    if(n.nodeType===1&&isStart(n)){g=document.createElement('div');g.className='ul-act';out.push(g)}
    if(g){g.appendChild(n)}else out.push(n)});
  return out}
function speakers(p){
  var s=p.firstElementChild;
  if(s&&s.tagName==='STRONG'&&s.textContent.trim().length<=8&&p.firstChild===s){s.classList.add('ul-spk');return}
  var f=p.firstChild;if(f&&f.nodeType===3){var m=f.nodeValue.match(/^([一-鿿]{2,4})[：:]/);if(m){var b=document.createElement('b');b.className='ul-spk';b.textContent=m[0];f.nodeValue=f.nodeValue.slice(m[0].length);p.insertBefore(b,f)}}}
A(document.querySelectorAll('main section')).forEach(function(sec){
  var num=(sec.id.match(/^s(\d+)$/)||[])[1];
  if(!num)return;num=+num;
  var h1=sec.querySelector(':scope>h1');
  if(num<1||num>12){
    /* phần mở đầu / phụ lục: không chia tab, chỉ dùng chung đầu trang và kiểu chữ */
    var pb=document.createElement('div');pb.className='ul-pb ul-plain';
    A(sec.children).forEach(function(n){if(n!==h1)pb.appendChild(n)});
    var H=document.createElement('header');H.className='ul-head';var k=document.createElement('p');k.className='ul-kick';k.textContent=ULAY.cfg.name;H.appendChild(k);if(h1)H.appendChild(h1);
    sec.appendChild(H);sec.appendChild(pb);ULAY.tagZh(pb);return}
  A(sec.querySelectorAll('.exk')).forEach(function(c,i){c.setAttribute('data-ux-i',i)});
  var B={ov:[],vo:[],tx:[],gr:[],pr:[],ex:[]},pend=[],area='head',mode='ov',dlg=false,last='ov',vtable=false;
  function put(p,n){if(pend.length){pend.forEach(function(h){B[p].push(h)});pend=[]}B[p].push(n);last=p}
  A(sec.children).forEach(function(n){
    var tag=n.tagName,t=T(n);
    if(tag==='H1')return;
    if(tag==='DIV'&&n.classList.contains('uxp')){B.pr.push(n);return}
    if(area==='head'&&tag==='P'&&/^Bài \d+:/.test(t)){n.classList.add('ul-dup');B.ov.push(n);return}
    if(tag==='H2'){dlg=false;
      if(/^PREPARE/.test(t)){area='prep';mode='ov'}else if(/^EXPLORE/.test(t))area='expl';else if(/^PRODUCE/.test(t))area='prod';else if(/^附录/.test(t))area='app';
      pend.push(n);return}
    if(tag==='H3'){dlg=false;
      if(area==='app'){put('ex',n);return}
      if(area==='expl'&&/^词语表/.test(t)){put('vo',n);return}
      if(area==='expl'&&/^[A-G][\s\.．、 ]/.test(t)){put('pr',n);return}
      pend.push(n);return}
    if(tag==='HR'){B[last].push(n);return}
    if(area==='app'){put('ex',n);return}
    if(area==='prod'){put('pr',n);return}
    if(area==='prep'){
      if(tag==='P'&&/^牛刀小试/.test(t))mode='pr';else if(tag==='P'&&/^学习目标/.test(t))mode='ov';
      put(mode,n);return}
    if(area==='expl'){
      if(tag==='P'&&/^词语表/.test(t)){put('vo',n);return}
      if(tag==='DIV'&&n.querySelector('table.vt')){put('vo',n);return}
      if(tag==='P'&&/^B[\s\.．、 ]*朗读/.test(t)){dlg=true;put('tx',n);return}
      if(dlg&&tag==='P'&&ACT.test(t))dlg=false;
      if(dlg){if(tag==='P')speakers(n);put('tx',n);return}
      put('pr',n);return}
    if(area==='head'){put(tag==='BLOCKQUOTE'?'ex':'pr',n);return}
    put(last,n)});
  pend.forEach(function(h){B[last].push(h)});
  B.pr=groupBy(B.pr,function(n){return n.tagName==='P'&&ACT.test(T(n))&&!/^[A-G][\s\.．、 ]*朗读/.test(T(n))});
  B.ex=groupBy(B.ex,function(n){return false});
  /* bản ghi: mỗi H3 + các đoạn sau nó vào một thẻ */
  (function(){var out=[],g=null;B.ex.forEach(function(n){if(n.nodeType===1&&n.tagName==='H3'){g=document.createElement('div');g.className='ul-act';out.push(g);g.appendChild(n)}else if(g)g.appendChild(n);else out.push(n)});B.ex=out})();
  /* hộp hội thoại */
  if(B.tx.length){var box=document.createElement('div');box.className='ul-card ul-dlg';B.tx.forEach(function(n){box.appendChild(n)});B.tx=[box]}
  var info=ULAY.lessonInfo(sec.id)||{};
  ULAY.mount(sec,{key:sec.id,num:num,zhEl:h1,vi:info.vi,buckets:B});
});
})();
