"""ld — công cụ riêng (UI đợt 3): stepper cho các «Thuật toán» (Kỹ năng, Parsing Lab), ô Slot + checklist 20 giây + đồng hồ 20 giây
cho Scanning, danh sách câu cho «Câu của mình». Không đổi dữ liệu. Dùng: python3 tools/ld_tools.py <html>"""
import re, sys, json

CSS = r"""
.ldst{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:6px 0;font-size:.92rem}
.ldst button,.ldtm button{font:inherit;font-size:.88rem;border:1px solid var(--line,#ccc);background:var(--card,#fff);color:inherit;border-radius:99px;padding:3px 12px;cursor:pointer}
.ldst button:disabled{opacity:.4;cursor:default}
.ldst .ldp{background:var(--seal,#a33);color:#fff;border-color:var(--seal,#a33)}
.ldtm{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:8px 0 12px;padding:8px 12px;border:1px dashed var(--line,#ccc);border-radius:10px}
.ldtm .ldt{font-weight:700;font-variant-numeric:tabular-nums;min-width:3em;text-align:center}.ldtm .ldt.end{color:#c0392b}
.ldin{font:inherit;color:inherit;background:var(--card,#fff);border:1px dashed var(--line,#bbb);border-radius:8px;padding:2px 8px;min-width:9em;max-width:100%;box-sizing:border-box;margin:2px 4px}
.ldcb{margin:0 6px 0 2px;vertical-align:middle}
.mlist{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 8px}.mlist .mc{font-size:.88rem;border:1px solid var(--line,#ccc);border-radius:99px;padding:1px 4px 1px 10px;background:var(--card,#fff)}
.mlist .mc button{border:0;background:transparent;color:inherit;cursor:pointer;font-size:1rem;padding:0 6px;opacity:.6}.mlist small{width:100%;opacity:.7}
"""

JS = r"""
(function(){
var P='ledu5-t-';
function g(k){try{return localStorage.getItem(P+k)}catch(e){return null}}
function s(k,v){try{localStorage.setItem(P+k,v)}catch(e){}}
function hash(t){var h=0;for(var i=0;i<t.length;i++)h=(h*31+t.charCodeAt(i))|0;return (h>>>0).toString(36)}
function txt(e){return e?e.textContent.replace(/\s+/g,' ').trim():''}
/* ---- stepper cho «Thuật toán» ---- */
function isAlgo(ol){var pv=ol.previousElementSibling,ct=(pv?txt(pv):''),par=ol.parentElement,ps=par&&par.querySelector(':scope>strong'),sec=ol.closest('.sec'),h4=sec&&sec.querySelector('h4');
  return /Thuật toán|Quy trình/.test(ct+' '+txt(ps)+' '+txt(h4))}
function stepper(ol){
  if(ol.dataset.sp||!isAlgo(ol))return;var lis=[].filter.call(ol.children,function(x){return x.tagName==='LI'});if(lis.length<2||lis.length>9)return;ol.dataset.sp='1';
  var N=lis.length,cur=0,all=false,bar=document.createElement('div');bar.className='ldst';
  bar.innerHTML='<b>Bước <span class="n">1</span>/'+N+'</b><button type="button" data-a="p">‹ Trước</button><button type="button" class="ldp" data-a="n">Bước tiếp ›</button><button type="button" data-a="a">Hiện tất cả</button>';
  function show(){lis.forEach(function(li,i){li.style.display=(all||i===cur)?'':'none'});bar.querySelector('.n').textContent=cur+1;bar.querySelector('[data-a=p]').disabled=all||cur===0;bar.querySelector('[data-a=n]').disabled=all||cur===N-1;bar.querySelector('[data-a=a]').textContent=all?'Từng bước':'Hiện tất cả'}
  bar.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var a=b.dataset.a;if(a==='p'&&cur>0)cur--;else if(a==='n'&&cur<N-1)cur++;else if(a==='a')all=!all;show()});
  ol.parentNode.insertBefore(bar,ol);show()}
/* ---- Scanning: ô Slot, checklist, đồng hồ ---- */
function fillBlanks(code,key){
  if(code.dataset.sl)return;code.dataset.sl='1';var st={};try{st=JSON.parse(g(key)||'{}')}catch(e){}var w=document.createTreeWalker(code,NodeFilter.SHOW_TEXT),n,list=[],k=0;
  while((n=w.nextNode()))list.push(n);
  list.forEach(function(n){var m=n.nodeValue.split(/_{3,}/);if(m.length<2)return;var fr=document.createDocumentFragment();
    m.forEach(function(x,j){fr.appendChild(document.createTextNode(x));if(j<m.length-1){var i=document.createElement('input'),id='i'+(k++);i.className='ldin';i.value=st[id]||'';i.oninput=function(){st[id]=i.value;s(key,JSON.stringify(st))};fr.appendChild(i)}});n.parentNode.replaceChild(fr,n)});
  code.style.whiteSpace='normal'}
function checks(root,key){
  if(root.dataset.ck)return;root.dataset.ck='1';var st={};try{st=JSON.parse(g(key)||'{}')}catch(e){}var w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT),n,list=[],k=0;
  while((n=w.nextNode()))list.push(n);
  list.forEach(function(n){var m=n.nodeValue.split(/\[\s?\]/);if(m.length<2)return;var fr=document.createDocumentFragment();
    m.forEach(function(x,j){fr.appendChild(document.createTextNode(x));if(j<m.length-1){var c=document.createElement('input'),id='c'+(k++);c.type='checkbox';c.className='ldcb';c.checked=!!st[id];c.onchange=function(){st[id]=c.checked?1:0;s(key,JSON.stringify(st))};fr.appendChild(c)}});n.parentNode.replaceChild(fr,n)})}
function timer(before){
  if(before.dataset.tm)return;before.dataset.tm='1';var bar=document.createElement('div');bar.className='ldtm';
  bar.innerHTML='<b>⏱ Đọc quét 20 giây</b><button type="button" class="ldp">Bắt đầu</button><span class="ldt">0:20</span><small>Đọc câu hỏi trước, nhảy tới đúng mục, rồi điền «Slot lần mình» bên dưới.</small>';
  var go=bar.querySelector('button'),tv=bar.querySelector('.ldt'),left=20,iv=null;
  function show(){tv.textContent='0:'+('0'+left).slice(-2);tv.classList.toggle('end',left===0)}
  go.onclick=function(){if(iv){clearInterval(iv);iv=null;left=20;show();go.textContent='Bắt đầu';return}left=20;show();go.textContent='Làm lại';iv=setInterval(function(){left--;show();if(left<=0){clearInterval(iv);iv=null;go.textContent='Bắt đầu lại'}},1000)};
  before.parentNode.insertBefore(bar,before)}
function scanning(){
  document.querySelectorAll('.sec').forEach(function(sec){var h=sec.querySelector('h4');if(!h)return;var t=txt(h);
    if(/^Thuật toán Question-First/.test(t))timer(sec);
    if(/^Slot lần mình/.test(t)){var key='slot-'+hash(txt(sec));sec.querySelectorAll('code').forEach(function(c){fillBlanks(c,key)})}
    if(/^Checklist 20 giây/.test(t))checks(sec,'chk-'+hash(txt(sec)))})}
/* ---- Câu của mình: danh sách câu ---- */
function mine(){
  document.querySelectorAll('textarea[data-mine]').forEach(function(t){
    if(t.dataset.ml)return;t.dataset.ml='1';var box=document.createElement('div');box.className='mlist';t.parentNode.appendChild(box);
    function draw(){var ls=t.value.split(/\n+/).map(function(x){return x.trim()}).filter(Boolean);box.innerHTML='';if(!ls.length)return;
      var sm=document.createElement('small');sm.textContent='Đã viết '+ls.length+' câu';box.appendChild(sm);
      ls.forEach(function(l,i){var c=document.createElement('span');c.className='mc';c.appendChild(document.createTextNode(l.length>28?l.slice(0,28)+'…':l));var b=document.createElement('button');b.type='button';b.title='Xoá câu này';b.textContent='×';
        b.onclick=function(){ls.splice(i,1);t.value=ls.join('\n');t.dispatchEvent(new Event('input',{bubbles:true}));draw()};c.appendChild(b);box.appendChild(c)})}
    t.addEventListener('input',draw);t.addEventListener('change',draw);draw();setTimeout(draw,600)})}
function all(){document.querySelectorAll('ol').forEach(function(o){try{stepper(o)}catch(e){}});try{scanning()}catch(e){console.error(e)}try{mine()}catch(e){console.error(e)}}
var tm=null,busy=false;
var mo=new MutationObserver(function(){if(busy)return;clearTimeout(tm);tm=setTimeout(function(){busy=true;try{all()}finally{setTimeout(function(){busy=false},50)}},250)});
function start(){all();mo.observe(document.body,{childList:true,subtree:true})}
if(document.readyState==='complete')start();else addEventListener('load',start);
})();
"""

def main(path):
    h = open(path, encoding='utf-8').read()
    m = re.search(r'(<script type="application/json" id="src-ld">)(.*?)(</script>)', h, re.S)
    d = json.loads(m.group(2))
    if '.ldst{' not in d:
        d = d.replace('</style>', CSS + '</style>', 1)
        i = d.rfind('</body>')
        d = d[:i] + '<script>' + JS + '</script>' + d[i:]
    h = h[:m.start(2)] + json.dumps(d, ensure_ascii=False).replace('<', '\\u003c') + h[m.end(2):]
    open(path, 'w', encoding='utf-8').write(h)
    print('ld_tools: đã chèn')

if __name__ == '__main__':
    main(sys.argv[1])
