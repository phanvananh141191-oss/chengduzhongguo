
/* ===== ULAY · bộ gom bài cho 乐读 5 (D1): 10 tab cũ -> 5 phần chung (+ Bổ sung) ===== */
(function(){
var SUBS={ov:['ov'],vo:['vo','kp','ch'],tx:['r0','r1'],gr:['wd'],pr:['sk','sc'],ex:['lec']};
var PANE_OF={ov:'ov',vo:'vo',kp:'vo',ch:'vo',wd:'gr',r0:'tx',r1:'tx',sk:'pr',sc:'pr',lec:'ex'};
var _tab=tab;
function cur(){return document.querySelector('#lm .ul-lesson')}
function focusSub(t){
  var p=PANE_OF[t];if(!p||SUBS[p][0]===t)return;
  var s=document.getElementById('ul-sub-'+t);if(s)s.scrollIntoView({block:'start'})}
function build(t){
  var L=LC,B={ov:[],vo:[],tx:[],gr:[],pr:[],ex:[]},lb=$('lbody');
  Object.keys(SUBS).forEach(function(p){SUBS[p].forEach(function(sub){
    if(sub==='lec'&&!L.lec)return;
    _tab(sub);
    var box=document.createElement('div');box.className='ul-sub';box.id='ul-sub-'+sub;box.setAttribute('data-sub',sub);
    while(lb.firstChild){var n=lb.firstChild;lb.removeChild(n);if(n.nodeType===1&&n.classList.contains('lnav'))continue;box.appendChild(n)}
    B[p].push(box)})});
  var crumb=document.createElement('div');crumb.className='ul-crumb';
  crumb.innerHTML='<button class="chip" data-back="1">← Quay lại</button><span class="crumb" id="lcr"></span>';
  var p0=PANE_OF[t]||(SUBS[t]?t:'ov');
  ULAY.mount(lb,{key:'l:'+L.n,num:L.n,zhText:L.han,vi:L.vi,crumb:crumb,buckets:B,pane:p0});
  LT=PANE_OF[t]?t:(SUBS[p0]||['ov'])[0];ORIG=null;
  sync();crumbL();$('lm').scrollTop=0;focusSub(t)}
openL=function(i,t){
  LC=LES[i];var m=$('lm');m.style.setProperty('--gc','var(--g'+LC.color+')');
  m.innerHTML='<div class="wrap" id="lbody"></div><div id="vb"></div>';
  m.classList.add('on');document.body.style.overflow='hidden';
  build(t||'ov')};
tab=function(t){
  var L=cur();if(!L){return _tab(t)}
  var p=PANE_OF[t]||(SUBS[t]?t:'ov');
  ULAY.activate(L,p,true);LT=PANE_OF[t]?t:SUBS[p][0];ORIG=null;
  $('vb').classList.remove('on');crumbL();focusSub(t)};
document.addEventListener('ul-pane',function(e){
  if(!window.LC||!$('lm').classList.contains('on')||!$('lcr'))return;
  var p=e.detail.pane;if(!(SUBS[p]&&SUBS[p].indexOf(LT)>=0))LT=(SUBS[p]||['ov'])[0];ORIG=null;crumbL()});
/* nút nghe dùng giọng đọc của trình duyệt: ẩn nếu thiết bị không hỗ trợ */
if(!window.speechSynthesis)document.documentElement.classList.add('ul-nosay');
})();
