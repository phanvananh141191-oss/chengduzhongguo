"""Đợt 1 giao diện bài tập (theo đề xuất UI): khung thẻ chung cho fz — đầu thẻ (huy hiệu dạng bài + chấm trạng thái),
chân thẻ (nút Kiểm tra nổi bật), thanh tiến độ số chữ cho khung viết. Không đổi dữ liệu, không đổi khoá lưu.
Dùng: python3 tools/fz_cardui.py <html>"""
import re, sys, json

CSS = """
.card.ex.xc{padding:0;overflow:hidden;border-radius:12px}
.card.ex.xc>.xb{padding:12px 16px 14px}
.xh{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:10px 16px;border-bottom:1px solid var(--bd);background:var(--u-card,var(--card))}
.xh .xbd{font-size:.78rem;padding:2px 10px;border-radius:99px;background:var(--u-hl,#e8efe9);color:var(--acc,#17685c);font-weight:600;white-space:nowrap}
.xh .xst{font-size:.82rem;color:var(--mut,#777);display:inline-flex;align-items:center;gap:6px}
.xh .xst:before{content:"";width:8px;height:8px;border-radius:50%;background:var(--mut,#999)}
.xc[data-st=doing] .xst:before{background:#d98a00}.xc[data-st=checked] .xst:before{background:#1a8f4a}
.xc[data-st=checked]{border-color:#1a8f4a55}
.xc .uxb{display:flex;gap:8px;flex-wrap:wrap;align-items:center;justify-content:flex-end;margin:12px 0 0;padding-top:10px;border-top:1px solid var(--bd)}
.xc .uxb .b:first-child{background:var(--acc,#17685c);color:#fff;border-color:var(--acc,#17685c);font-weight:600}
.xc .uxb .sc{margin-right:auto;margin-left:0}
.xc .uin{margin:12px 0}
.wr .wbar{height:6px;border-radius:3px;background:var(--bd);overflow:hidden;margin:6px 0}.wr .wbar>i{display:block;height:100%;width:0;background:var(--acc,#17685c);transition:width .2s}.wr .wbar>i.full{background:#1a8f4a}
.xh .xvt{margin-left:auto;font-size:.78rem;border:1px solid var(--bd);background:transparent;color:var(--mut,#777);border-radius:99px;padding:2px 10px;cursor:pointer}
.xh .xvt[aria-pressed=true]{background:var(--u-hl,#e8efe9);color:var(--acc,#17685c)}
.xc.novi .lv,.xc.novi .lvb{display:none!important}
.xbank{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 10px;padding:8px 10px;border:1px dashed var(--bd);border-radius:10px;background:var(--u-card,var(--card))}
.xbank .xch{font:inherit;font-size:1rem;line-height:1.15;padding:5px 12px;border:1px solid var(--bd);border-radius:8px;background:var(--card);color:inherit;cursor:pointer;text-align:center}
.xbank .xch small{display:block;font-size:.66rem;color:var(--mut,#777);margin-top:2px}
.xbank .xch.sel{border-color:var(--acc,#17685c);background:var(--u-hl,#e8efe9);color:var(--acc,#17685c);box-shadow:0 0 0 2px #17685c33}
.xbank .xch.used{opacity:.4}
.xbank .xtip{flex:1 0 100%;font-size:.78rem;color:var(--mut,#777)}
.xbsrc{display:none!important}
.xc.xsel input[data-a],.xc.xsel input.uw{outline:1px dashed var(--acc,#17685c);cursor:pointer}
.xin{margin:6px 0 12px}.xin textarea{width:100%;min-height:3.2em;box-sizing:border-box;border:1px dashed var(--u-line,var(--bd));border-radius:8px;background:var(--u-card,var(--card));color:inherit;font:inherit;padding:6px 8px}
.xc input.uw.xmir{background:transparent;border-bottom:1px dotted var(--mut,#999);pointer-events:none;color:var(--acc,#17685c);min-width:6em}
.ordw{margin:8px 0 10px;display:flex;flex-direction:column;gap:8px}
.ordi{display:flex;gap:8px;align-items:stretch;border:1px solid var(--bd);border-radius:10px;background:var(--card);padding:6px 8px}
.ordi.ok{border-color:#1a8f4a;background:#1a8f4a14}.ordi.no{border-color:#c0392b;background:#c0392b12}
.ordi .ordn{flex:none;width:26px;height:26px;border-radius:50%;background:var(--u-hl,#e8efe9);color:var(--acc,#17685c);display:flex;align-items:center;justify-content:center;font-weight:700;margin-top:4px}
.ordi .ordc{flex:1;min-width:0}.ordi .ordc .ln{margin:2px 0}
.ordi .ordb{flex:none;display:flex;flex-direction:column;gap:4px;justify-content:center}
.ordi .ordb button,.mtw button{font:inherit;font-size:.85rem;border:1px solid var(--bd);background:var(--card);color:inherit;border-radius:8px;padding:2px 9px;cursor:pointer}
.ordi.drag{opacity:.5}
.ordmsg{font-size:.85rem;color:var(--mut)}
.mtw{margin:8px 0 12px;border:1px dashed var(--bd);border-radius:10px;padding:10px;background:var(--u-card,var(--card))}
.mtw .mtc{display:grid;grid-template-columns:1fr 1fr;gap:6px 16px}
.mtw .mti{display:block;width:100%;text-align:left;margin:0;padding:6px 10px;font-size:1rem;border-radius:8px;line-height:1.3}
.mtw .mti small{display:block;color:var(--mut);font-size:.72rem}
.mtw .mti.sel{border-color:var(--acc,#17685c);box-shadow:0 0 0 2px #17685c33}
.mtw .mti[data-c]{border-left:6px solid var(--mc)}
.mtw .mti.ok{background:#1a8f4a18}.mtw .mti.no{background:#c0392b18}
.mtw .mtl{font-size:.9rem;margin-top:8px;color:var(--mut)}.mtw .mtb{margin-top:8px;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.rdt{display:none;gap:6px;margin:6px 0}.rdt button{font:inherit;font-size:.85rem;border:1px solid var(--bd);background:var(--card);color:inherit;border-radius:99px;padding:3px 12px;cursor:pointer}.rdt button.on{background:var(--acc,#17685c);color:#fff;border-color:var(--acc,#17685c)}
.rd{display:grid;grid-template-columns:1fr;gap:12px}
@media(min-width:860px){.rd{grid-template-columns:1.25fr 1fr;align-items:start}.rd .rdl{max-height:78vh;overflow:auto;padding-right:6px}.rd .rdr{position:sticky;top:8px}}
@media(max-width:859px){.rdt{display:flex}.rd[data-v=r] .rdl{display:none}.rd[data-v=l] .rdr{display:none}}
"""

JS = r"""
(function(){
var TYPES=[[/排序/,'排序'],[/连线/,'连线'],[/改写/,'改写'],[/完成对话|对话/,'完成对话'],[/完成句子/,'完成句子'],[/选词|选择合适|选择最合适|填空/,'选词填空'],[/写一写|写作/,'写一写'],[/课本剧|分享/,'表演·分享'],[/阅读|短文/,'阅读'],[/拓展/,'拓展'],[/回答|理解课文|问题/,'问答'],[/字词|新词语|注释|字源/,'字词'],[/想一想|思考/,'想一想']];
function sec(c){var r='',hs=c.closest('section')?c.closest('section').querySelectorAll('h2'):[];for(var i=0;i<hs.length;i++){if(hs[i].compareDocumentPosition(c)&4)r=hs[i].textContent}return r}
function typeOf(t){for(var i=0;i<TYPES.length;i++)if(TYPES[i][0].test(t))return TYPES[i][1];return '练习'}
function status(c){
  var v=false;c.querySelectorAll('input.uw,input[data-a],textarea').forEach(function(x){if((x.value||'').trim())v=true});
  if(c.querySelector('.ans:not([hidden])'))return 'checked';
  return v?'doing':'todo'}
var LAB={todo:'Chưa làm',doing:'Đang làm',checked:'Đã kiểm tra'};
function setSt(c,s){c.dataset.st=s;var e=c.querySelector('.xst');if(e)e.textContent=LAB[s]}

var HAN=/[一-鿿]/;
function parseComma(t){
  t=t.replace(/^\s*(?:Bảng từ|词库|词语库)\s*[:：]\s*/,'');
  var parts=t.split(/[,，、;；]\s*/).map(function(x){return x.trim()}).filter(Boolean);
  if(parts.length<4)return null;var out=[];
  for(var i=0;i<parts.length;i++){var m=parts[i].match(/^(\S*[一-鿿]\S*?)(?:\s+([^一-鿿]*))?$/);if(!m)return null;out.push([m[1],(m[2]||'').trim()])}
  return out}
function parseSpace(t){
  t=t.replace(/^\s*(?:[（(][一二三四五六七八九十][）)]\s*)?/,'').replace(/^[一二三四五六七八九十]、选词填空\s+/,'').replace(/^[^：:]{0,40}[：:]\s*/,'');
  var parts=t.trim().split(/\s+/);if(parts.length<4)return null;
  for(var i=0;i<parts.length;i++)if(!/^[一-鿿]{1,8}$/.test(parts[i]))return null;
  return parts.map(function(x){return [x,'']})}
function answersOf(c){var a={};c.querySelectorAll('input[data-a]').forEach(function(i){i.dataset.a.split('|').forEach(function(x){a[x.trim()]=1})});return a}
function mkBank(c,ents,after){
  var ans=answersOf(c),hit=0,tot=ents.length;ents.forEach(function(e){if(ans[e[0]])hit++});
  if(!Object.keys(ans).length||hit<2)return null;
  var b=document.createElement('div');b.className='xbank';
  ents.forEach(function(e){var x=document.createElement('button');x.type='button';x.className='xch';x.dataset.w=e[0];x.textContent=e[0];if(e[1]){var s=document.createElement('small');s.textContent=e[1];x.appendChild(s)}b.appendChild(x)});
  var tip=document.createElement('div');tip.className='xtip';tip.textContent='Chạm một từ, rồi chạm ô trống để điền. Nhấp đúp ô đã điền để trả từ về khung.';b.appendChild(tip);
  after.parentNode.insertBefore(b,after.nextSibling);return b}
function banks(c){
  if(c.querySelector('.bank')||c.querySelector('.xbank'))return;
  var made=0;
  c.querySelectorAll('.ln').forEach(function(l){
    if(l.closest('.xbank'))return;var t=l.textContent.trim();if(t.length>1200||/—/.test(t.slice(0,40)))return;
    var e=parseComma(t);if(!e||!/^Bảng từ|^[一-鿿]/.test(t))return;
    var b=mkBank(c,e,l);if(b){l.classList.add('xbsrc');made++}});
  c.querySelectorAll('.xbl').forEach(function(l){var e=l.dataset.b.split(' ').filter(Boolean).map(function(x){return [x,'']});if(e.length<3)return;var b=mkBank(c,e,l);if(b)l.classList.add('xbsrc')});
  var w=document.createTreeWalker(c,NodeFilter.SHOW_TEXT,null),n,list=[];
  while((n=w.nextNode())){var p=n.parentNode;if(p.closest('.xbank,.xbsrc,.ans,textarea,.uin'))continue;
    var nx=n.nextSibling,pv=n.previousSibling;
    if(!(nx&&nx.nodeName==='BR')||!(pv==null||pv.nodeName==='BR'))continue;
    if(!HAN.test(n.nodeValue)||n.nodeValue.length>200)continue;
    var e=parseSpace(n.nodeValue);if(e)list.push([n,e])}
  list.forEach(function(x){var n=x[0],sp=document.createElement('span');sp.className='xbsrc';n.parentNode.insertBefore(sp,n);sp.appendChild(n);
    var br=sp.nextSibling;var holder=document.createElement('span');br.parentNode.insertBefore(holder,br.nextSibling);
    var b=mkBank(c,x[1],holder);if(!b)sp.className='';else{holder.parentNode.removeChild(holder)}});
}
function bindBank(c){
  var sel=null;
  function upd(){var vals={};c.querySelectorAll('input[data-a],input.uw').forEach(function(i){if(i.value.trim())vals[i.value.trim()]=1});
    c.querySelectorAll('.xch').forEach(function(x){x.classList.toggle('used',!!vals[x.dataset.w])})}
  c.addEventListener('click',function(e){
    var ch=e.target.closest&&e.target.closest('.xch');
    if(ch){if(sel===ch){sel.classList.remove('sel');sel=null;c.classList.remove('xsel')}else{if(sel)sel.classList.remove('sel');sel=ch;ch.classList.add('sel');c.classList.add('xsel')}return}
    var i=e.target.closest&&e.target.closest('input[data-a],input.uw');
    if(i&&sel){i.value=sel.dataset.w;i.dispatchEvent(new Event('input',{bubbles:true}));sel.classList.remove('sel');sel=null;c.classList.remove('xsel');upd()}});
  c.addEventListener('dblclick',function(e){var i=e.target.closest&&e.target.closest('input[data-a],input.uw');if(i&&i.value){i.value='';i.dispatchEvent(new Event('input',{bubbles:true}));upd()}});
  c.addEventListener('input',upd);setTimeout(upd,300)}
var ITEM=/^\s*(?:\d+[\.、．]|[（(]\d+[）)])/;
var FTYPE=/完成对话|完成句子|改写|完成练习|回答|理解课文/;
function mkFrame(it,anchor,inp,kk,append){
  var d=document.createElement('div');d.className='xin';var t=document.createElement('textarea');t.rows=2;t.placeholder='Viết câu của bạn…';d.appendChild(t);
  if(append)anchor.appendChild(d);else anchor.parentNode.insertBefore(d,anchor.nextSibling);
  if(inp){inp.classList.add('xmir');inp.readOnly=true;t.value=inp.value||'';
    t.addEventListener('input',function(){inp.value=t.value;inp.dispatchEvent(new Event('input',{bubbles:true}))});
    var iv=setInterval(function(){if(!t.value&&inp.value)t.value=inp.value},700);setTimeout(function(){clearInterval(iv)},4000)}
  else{try{t.value=UEX.ls.getItem(kk)||''}catch(e){}
    t.addEventListener('input',function(){try{UEX.ls.setItem(kk,t.value)}catch(e){}});
    setTimeout(function(){try{if(!t.value)t.value=UEX.ls.getItem(kk)||''}catch(e){}},900)}
  return d}
function framesAll(){
  document.querySelectorAll('section.les h3').forEach(function(h3){
    if(h3.dataset.fr||!/综合练习/.test(sec(h3))||!FTYPE.test(h3.textContent)||/选/.test(h3.textContent))return;
    h3.dataset.fr='1';
    var card=h3.parentElement&&h3.parentElement.classList.contains('card')?h3.parentElement:null,roots=[];
    if(card)roots=[card];else{var e=h3.nextElementSibling;while(e&&e.tagName!=='H3'&&e.tagName!=='H2'){roots.push(e);e=e.nextElementSibling}}
    var sc=h3.closest('section'),hs=[].slice.call(sc.querySelectorAll('h3')),hi=hs.indexOf(h3);
    var uk=null,items=[];
    roots.forEach(function(r){
      if(!uk){var u=r.matches&&r.matches('textarea.uans')?r:(r.querySelector&&r.querySelector('textarea.uans'));if(u)uk=u.dataset.k}
      var els=[].slice.call(r.querySelectorAll('li,.ln.lz'));if(r.matches&&r.matches('.ln.lz'))els.unshift(r);
      els.forEach(function(e){
        if(e.closest('.ans,.uin,.xin,.xbank,table,.w'))return;
        if(e.tagName==='LI'){if(e.querySelector('li')||e.querySelector('.uin,.xin'))return;items.push(['li',e]);return}
        if(e.closest('li'))return;if(e.querySelector('.ln.lz'))return;
        if(ITEM.test(e.textContent))items.push(['ln',e])})});
    if(items.length<2)return;
    var base=uk||('ans:fz:'+sc.id+':f'+hi),made=0;
    items.forEach(function(x,k){
      var it=x[1],inps=it.querySelectorAll('input.uw'),inp=inps.length===1?inps[0]:null;
      if(inps.length>1)return;
      if(x[0]==='li'){mkFrame(it,it,inp,base+':i'+k,true);made++}
      else{var last=it;while(last.nextElementSibling&&last.nextElementSibling.classList.contains('ln')&&!last.nextElementSibling.classList.contains('lz')&&!ITEM.test(last.nextElementSibling.textContent))last=last.nextElementSibling;
        mkFrame(it,last,inp,base+':i'+k,false);made++}});
    if(made>=2&&card)card.querySelectorAll('.uin').forEach(function(u){if(!u.closest('li'))u.style.display='none'});
  })}

/* ===== Đợt 2: sắp xếp câu · nối cặp · đọc hiểu chia đôi ===== */
function stripLead(el,re){var w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT),n;while((n=w.nextNode())){if(n.nodeValue.trim()){n.nodeValue=n.nodeValue.replace(re,'');return}}}
function ordW(){
 document.querySelectorAll('.card.ex.xc').forEach(function(c){
  if(c.dataset.ow)return;var bd=c.querySelector('.xbd');if(!bd||bd.textContent!=='排序')return;c.dataset.ow='1';
  var xb=c.querySelector('.xb');if(!xb)return;var kids=[].slice.call(xb.children),ans={},at=c.querySelector('.ans');
  if(at)(at.textContent.match(/(\d)\s*([A-F]{2,})/g)||[]).forEach(function(m){var q=m.match(/(\d)\s*([A-F]+)/);ans[q[1]]=q[2]});
  var i=0;
  while(i<kids.length){
    var k=kids[i],m=k.classList.contains('ln')?k.textContent.trim().match(/^(\d+)\.\s*A\./):null;
    if(!m){i++;continue}
    var num=m[1],items=[k],j=i+1;
    while(j<kids.length&&kids[j].classList.contains('ln')&&/^[B-F]\./.test(kids[j].textContent.trim())){items.push(kids[j]);j++}
    var line=kids[j]&&/恰当的顺序/.test(kids[j].textContent)?kids[j]:null,inp=line?line.querySelector('input[data-a],input.uw'):null;
    var key=(inp&&inp.dataset.a)||ans[num]||'';
    stripLead(items[0],/^\s*\d+\.\s*/);
    var w=document.createElement('div');w.className='ordw';var h=document.createElement('div');h.className='ordh';h.innerHTML='<b>'+num+'.</b> Sắp xếp các câu theo thứ tự đúng';
    items[0].parentNode.insertBefore(h,items[0]);h.parentNode.insertBefore(w,items[0].nextSibling?items[0]:null);
    items.forEach(function(el,t){var L=el.textContent.trim().charAt(0),d=document.createElement('div');d.className='ordi';d.dataset.l=L;d.draggable=true;
      d.innerHTML='<span class="ordn"></span><div class="ordc"></div><div class="ordb"><button type="button" data-d="-1" title="Lên">↑</button><button type="button" data-d="1" title="Xuống">↓</button></div>';
      d.querySelector('.ordc').appendChild(el);w.appendChild(d)});
    var msg=document.createElement('div');msg.className='ordmsg';var bt=document.createElement('button');bt.type='button';bt.textContent='Kiểm tra thứ tự';
    var foot=document.createElement('div');foot.className='mtb';foot.appendChild(bt);foot.appendChild(msg);w.parentNode.insertBefore(foot,w.nextSibling);
    (function(w,inp,key,msg,bt){
      function order(){return [].map.call(w.children,function(x){return x.dataset.l}).join('')}
      function num_(){[].forEach.call(w.children,function(x,t){x.querySelector('.ordn').textContent=t+1;x.classList.remove('ok','no')});msg.textContent=''}
      function sync(){num_();var o=order();if(inp){inp.value=o;inp.readOnly=true;inp.dispatchEvent(new Event('input',{bubbles:true}))}}
      w.addEventListener('click',function(e){var b=e.target.closest('button[data-d]');if(!b)return;var it=b.closest('.ordi'),d=+b.dataset.d;
        if(d<0&&it.previousElementSibling)w.insertBefore(it,it.previousElementSibling);else if(d>0&&it.nextElementSibling)w.insertBefore(it.nextElementSibling,it);sync()});
      var drag=null;w.addEventListener('dragstart',function(e){drag=e.target.closest('.ordi');if(drag){drag.classList.add('drag');e.dataTransfer.effectAllowed='move'}});
      w.addEventListener('dragover',function(e){e.preventDefault();var o=e.target.closest('.ordi');if(!drag||!o||o===drag)return;var r=o.getBoundingClientRect();w.insertBefore(drag,(e.clientY-r.top)<r.height/2?o:o.nextSibling)});
      w.addEventListener('dragend',function(){if(drag)drag.classList.remove('drag');drag=null;sync()});
      bt.onclick=function(){var o=order();if(!key){msg.textContent='Chưa có đáp án trong tài liệu nguồn.';return}
        [].forEach.call(w.children,function(x,t){x.classList.toggle('ok',x.dataset.l===key.charAt(t));x.classList.toggle('no',x.dataset.l!==key.charAt(t))});
        msg.textContent=o===key?'✓ Đúng thứ tự':'Chưa đúng — thử sắp lại'};
      sync();
      if(line){var bk=line.querySelector('.bank');if(bk)bk.style.display='none'}
    })(w,inp,key,msg,bt);
    i=j+(line?1:0);
  }
 })}
function scopeRoots(h3){var card=h3.parentElement&&h3.parentElement.classList.contains('card')?h3.parentElement:null;if(card)return [card];var r=[],e=h3.nextElementSibling;while(e&&e.tagName!=='H3'&&e.tagName!=='H2'){r.push(e);e=e.nextElementSibling}return r}
function pairsFrom(t){var o=[];t.replace(/([一-鿿]+)\s*[—–-]+\s*([一-鿿]+)/g,function(m,a,b){o.push([a,b])});return o}
var MC=['#d98a00','#17685c','#7b3f8f','#c0392b','#2a6fb0','#8a6d3b','#b3541e','#4d7c0f'];
function mkMatch(after,title,L,R,key,ex,locked){
  var w=document.createElement('div');w.className='mtw';
  w.innerHTML='<div class="mtc"><div class="mtl0"></div><div class="mtr0"></div></div><div class="mtl"></div><div class="mtb"><button type="button" data-a="ck">Kiểm tra</button><button type="button" data-a="sh">Xem đáp án</button><button type="button" data-a="rs">Làm lại</button><span class="mts"></span></div>';
  var lc=w.querySelector('.mtl0'),rc=w.querySelector('.mtr0');
  function btn(e,side,i){var b=document.createElement('button');b.type='button';b.className='mti';b.dataset.s=side;b.dataset.i=i;b.textContent=e[0];if(e[1]){var sm=document.createElement('small');sm.textContent=e[1];b.appendChild(sm)}return b}
  L.forEach(function(e,i){lc.appendChild(btn(e,'l',i))});R.forEach(function(e,i){rc.appendChild(btn(e,'r',i))});
  var P={},sel=null,mts=w.querySelector('.mts'),lst=w.querySelector('.mtl');
  function paint(){w.querySelectorAll('.mti').forEach(function(b){b.removeAttribute('data-c');b.classList.remove('sel','ok','no');b.style.removeProperty('--mc')});
    Object.keys(P).forEach(function(l){var c=MC[l%MC.length],a=lc.children[l],b=rc.children[P[l]];[a,b].forEach(function(x){x.setAttribute('data-c','1');x.style.setProperty('--mc',c)})});
    if(sel!==null)lc.children[sel].classList.add('sel');
    lst.textContent=Object.keys(P).map(function(l){return L[l][0]+' — '+R[P[l]][0]}).join('  ·  ')}
  function chk(){var ok=0,n=Object.keys(P).length;Object.keys(P).forEach(function(l){var good=key[L[l][0]]===R[P[l]][0];lc.children[l].classList.add(good?'ok':'no');rc.children[P[l]].classList.add(good?'ok':'no');if(good)ok++});mts.textContent='Đúng '+ok+'/'+Object.keys(key).length+(n<Object.keys(key).length?' (còn chưa nối hết)':'')}
  w.addEventListener('click',function(e){var b=e.target.closest('.mti'),a=e.target.closest('button[data-a]');
    if(b){var i=+b.dataset.i;if(b.dataset.s==='l'){if(P[i]!==undefined&&sel===null){delete P[i]}else sel=(sel===i?null:i)}else if(sel!==null){Object.keys(P).forEach(function(l){if(P[l]===i)delete P[l]});P[sel]=i;sel=null}paint();mts.textContent='';return}
    if(a){var k=a.dataset.a;if(k==='ck')chk();else if(k==='rs'){P={};sel=null;if(ex){}paint();mts.textContent=''}else{P={};L.forEach(function(e,i){var r=R.findIndex(function(x){return x[0]===key[e[0]]});if(r>=0)P[i]=r});sel=null;paint();mts.textContent='Đáp án mẫu'}}});
  after.parentNode.insertBefore(w,after.nextSibling);paint();return w}
function entries(t){return t.split(/[,，]\s*(?=[一-鿿])/).map(function(x){var m=x.trim().match(/^(\S+)\s*(.*)$/);return m?[m[1],m[2]]:null}).filter(Boolean)}
function matchW(){
 document.querySelectorAll('section.les h3').forEach(function(h3){
  if(h3.dataset.mw||!/连线/.test(h3.textContent)||!/综合练习/.test(sec(h3)))return;h3.dataset.mw='1';
  var roots=scopeRoots(h3),els=[];roots.forEach(function(r){if(r.matches&&r.matches('.ln.lz,.zu'))els.push(r);els=els.concat([].slice.call(r.querySelectorAll('.ln.lz,.zu')))});
  var an=null;roots.forEach(function(r){var a=(r.matches&&r.matches('.ans'))?r:r.querySelector('.ans');if(a&&!an)an=a});var at=an?an.textContent:'';
  var up=els.filter(function(e){return /^\s*Hàng trên\s*[:：]/.test(e.textContent)})[0],dn=els.filter(function(e){return /^\s*Hàng dưới\s*[:：]/.test(e.textContent)})[0];
  if(up&&dn){var L=entries(up.textContent.replace(/^\s*Hàng trên\s*[:：]\s*/,'')),R=entries(dn.textContent.replace(/^\s*Hàng dưới\s*[:：]\s*/,'')),key={};
    pairsFrom(at).forEach(function(p){key[p[0]]=p[1]});if(L.length>2&&R.length>2&&Object.keys(key).length){up.classList.add('xbsrc');dn.classList.add('xbsrc');mkMatch(dn,'',L,R,key)}return}
  els.filter(function(e){return /↔/.test(e.textContent)}).forEach(function(e){
    var t=e.textContent,lab=/近义/.test(t)?'近义':'反义',x=t.replace(/（例[:：][^）]*）/,'').replace(/^[^：:]*[：:]\s*/,'').split('↔');if(x.length!==2)return;
    var L=x[0].trim().split(/\s+/).map(function(w){return [w,'']}),R=x[1].trim().split(/\s+/).map(function(w){return [w,'']}),key={},seg=at.split(/反义[:：]|近义[:：]/);
    var s=lab==='反义'?(at.split('反义：')[1]||'').split('近义：')[0]:(at.split('近义：')[1]||'');pairsFrom(s).forEach(function(p){key[p[0]]=p[1]});
    if(Object.keys(key).length){e.classList.add('xbsrc');mkMatch(e,'',L,R,key)}})
 })}
function readW(){
 document.querySelectorAll('.card.ex.xc').forEach(function(c){
  if(c.dataset.rw)return;var bd=c.querySelector('.xbd');if(!bd||bd.textContent!=='阅读')return;var xb=c.querySelector('.xb');if(!xb)return;c.dataset.rw='1';
  var kids=[].slice.call(xb.children),h=kids[0]&&kids[0].tagName==='H3'?1:0,b=-1;
  for(var i=h;i<kids.length;i++){var k=kids[i];
    if(k.tagName==='OL'||k.tagName==='UL'||k.classList.contains('uin')||(k.classList.contains('ln')&&k.querySelector(':scope>span.lz')&&/^\s*\d+\./.test(k.textContent))){b=i;break}}
  if(b<0||b-h<3)return;
  var rd=document.createElement('div');rd.className='rd';rd.dataset.v='l';var L=document.createElement('div'),R=document.createElement('div');L.className='rdl';R.className='rdr';
  for(var i=h;i<kids.length;i++)(i<b?L:R).appendChild(kids[i]);rd.appendChild(L);rd.appendChild(R);xb.appendChild(rd);
  var tb=document.createElement('div');tb.className='rdt';tb.innerHTML='<button type="button" data-v="l" class="on">Bài đọc</button><button type="button" data-v="r">Câu hỏi</button>';
  tb.addEventListener('click',function(e){var x=e.target.closest('button');if(!x)return;rd.dataset.v=x.dataset.v;[].forEach.call(tb.children,function(y){y.classList.toggle('on',y===x)})});xb.insertBefore(tb,rd)})}
function run(){
 document.querySelectorAll('.card.ex').forEach(function(c){
  if(c.classList.contains('xc'))return;
  var h=c.querySelector('h3'),t=h?h.textContent:(c.previousElementSibling&&c.previousElementSibling.tagName==='H3'?c.previousElementSibling.textContent:'');
  if(!c.querySelector('.uxb')&&!c.querySelector('textarea'))return;
  var kids=[].slice.call(c.childNodes),b=document.createElement('div');b.className='xb';
  kids.forEach(function(k){b.appendChild(k)});
  var hd=document.createElement('div');hd.className='xh';
  hd.innerHTML='<span class="xbd"></span><span class="xst"></span>';hd.firstChild.textContent=/综合注释/.test(sec(c))?'语法·练习':(/走进课文/.test(sec(c))?'课文·问答':typeOf(t));
  c.appendChild(hd);c.appendChild(b);c.classList.add('xc');
  var vt=document.createElement('button');vt.type='button';vt.className='xvt';vt.textContent='🇻🇳 Dịch';vt.setAttribute('aria-pressed','true');vt.onclick=function(){var off=c.classList.toggle('novi');vt.setAttribute('aria-pressed',off?'false':'true')};hd.appendChild(vt);
  try{banks(c);bindBank(c)}catch(e){}
  setSt(c,status(c));
  c.addEventListener('input',function(){if(c.dataset.st!=='checked')setSt(c,status(c))});
  c.addEventListener('click',function(e){var x=e.target.closest&&e.target.closest('.uxb .b');if(!x)return;var tx=x.textContent;
    setTimeout(function(){if(/Kiểm tra|Xem đáp án|Ẩn đáp án/.test(tx)){setSt(c,/Ẩn đáp án/.test(tx)?status(c):'checked')}else if(/Làm lại/.test(tx))setSt(c,'todo')},60)});
 });
 document.querySelectorAll('.wr').forEach(function(w){
  if(w.querySelector('.wbar'))return;var t=w.querySelector('textarea'),mn=+w.dataset.min||0;if(!t||!mn)return;
  var bar=document.createElement('div');bar.className='wbar';bar.innerHTML='<i></i>';t.parentNode.insertBefore(bar,t.nextSibling);
  function u(){var n=t.value.replace(/\s/g,'').length,i=bar.firstChild;i.style.width=Math.min(100,100*n/mn)+'%';i.className=n>=mn?'full':''}
  t.addEventListener('input',u);u()});
}
function all(){run();try{framesAll()}catch(e){}try{ordW()}catch(e){console.error(e)}try{matchW()}catch(e){console.error(e)}try{readW()}catch(e){console.error(e)}}
function go(){setTimeout(all,900);setTimeout(all,2500)}
if(document.readyState==='complete')go();else addEventListener('load',go);
})();
"""

def main(path):
    h = open(path, encoding='utf-8').read()
    m = re.search(r'(<script type="application/json" id="src-fz">)(.*?)(</script>)', h, re.S)
    d = json.loads(m.group(2))
    W = r'((?:[\u4e00-\u9fff]{1,6} ){3,}[\u4e00-\u9fff]{1,6})'
    def wrap(m): return m.group(1) + '<span class="xbl" data-b="%s">%s</span>' % (m.group(2), m.group(2))
    nb = 0
    for n in (1, 2):
        i0 = d.find('id="l%d"' % n); j0 = d.find('<section class="les', i0 + 10); j0 = len(d) if j0 < 0 else j0
        seg = d[i0:j0]
        if 'class="xbl"' in seg: continue
        for pat in (r'(?<=<br/>)((?:[（(][一二三四五六七八九十][）)] )?(?:[^<：\n↔]{0,30}：)?)' + W + r'(?=<br/>)',
                    r'(<b>[一二三四五六七八九十]、选词填空</b> )' + W + r'(?=</p>)',
                    r'(\(词库：)' + W.replace('{3,}', '{2,}') + r'(?=\))'):
            seg, k = re.subn(pat, wrap, seg); nb += k
        d = d[:i0] + seg + d[j0:]
    print('  bank dòng gắn nhãn xbl:', nb)
    if '.card.ex.xc{' not in d:
        d = d.replace('</style>', CSS + '</style>', 1)
        i = d.rfind('</body>')
        d = d[:i] + '<script>' + JS + '</script>' + d[i:]
    h = h[:m.start(2)] + json.dumps(d, ensure_ascii=False).replace('<', '\\u003c') + h[m.end(2):]
    open(path, 'w', encoding='utf-8').write(h)
    print('fz_cardui: đã chèn')

if __name__ == '__main__':
    main(sys.argv[1])
