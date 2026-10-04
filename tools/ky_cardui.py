"""UI đợt 3 cho ky: nút/thanh đọc to (giọng đọc của trình duyệt), checklist 评价, stepper nhiệm vụ 任务一/二/三,
huy hiệu hình thức + đồng hồ cho hoạt động nói. Không đổi nội dung giáo trình.
Dùng: python3 tools/ky_cardui.py <html>"""
import re, sys, json

CSS = r"""
.kspk{display:inline-block;margin-left:.4em;border:1px solid var(--bd);background:var(--card);border-radius:99px;font-size:.7em;line-height:1;padding:2px 7px;cursor:pointer;vertical-align:middle;color:var(--mut)}
.u3.kon{background:#17685c14;outline:2px solid #17685c33;border-radius:6px}
.kbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:6px 0 8px;font-size:.88em}
.kbar button,.kbar select{font:inherit;font-size:.9em;border:1px solid var(--bd);background:var(--card);color:inherit;border-radius:99px;padding:3px 12px;cursor:pointer}
.kbar .kp{background:var(--ac);color:#fff;border-color:var(--ac)}
.kbar small{color:var(--mut)}
.kbadge{font-size:.78em;padding:2px 10px;border-radius:99px;background:#f3e6e4;color:var(--ac);font-weight:600}
.kt{font-variant-numeric:tabular-nums;font-weight:600;min-width:3.2em;text-align:center}
.kt.end{color:#c0392b}
.kstep{margin:12px 0 18px;border:1px solid var(--bd);border-radius:10px;background:var(--card);padding:10px 14px}
.kstep .kh{display:flex;gap:10px;align-items:center;margin-bottom:6px;font-weight:600}
.kstep .kbarp{flex:1;height:6px;border-radius:3px;background:var(--bd);overflow:hidden}.kstep .kbarp>i{display:block;height:100%;width:0;background:var(--ac);transition:width .2s}
.kstep .ks{display:grid;grid-template-columns:auto 1fr;gap:4px 10px;padding:6px 0;border-top:1px dashed var(--bd)}
.kstep .ks label{font-weight:600;white-space:nowrap}
.kstep textarea,.kin,.knote{font:inherit;color:inherit;background:var(--bg,var(--card));border:1px dashed var(--bd);border-radius:8px;padding:5px 8px;box-sizing:border-box}
.kstep textarea{width:100%;min-height:2.6em}.kin{min-width:7em;width:auto;margin:0 3px;padding:1px 6px}
.knote{width:100%;min-height:4.5em;margin:6px 0}
.kprog{font-size:.85em;color:var(--mut);margin:4px 0}
"""

JS = r"""
(function(){
var SS=window.speechSynthesis,K='ky:ui:',ls=null;
function store(){try{if(window.UEX&&UEX.ls)return UEX.ls}catch(e){}return null}
function get(k){try{var s=store();var v=s?s.getItem(K+k):localStorage.getItem(K+k);return v?JSON.parse(v):null}catch(e){return null}}
function put(k,v){try{var s=store();if(s)s.setItem(K+k,JSON.stringify(v));else localStorage.setItem(K+k,JSON.stringify(v))}catch(e){}}
function ht(h){var c=h.cloneNode(true);c.querySelectorAll('rt').forEach(function(x){x.remove()});return c.textContent.replace(/\s+/g,' ').trim()}
function zhOf(el){var c=el.cloneNode(true);c.querySelectorAll('rt,.kspk,sup,.kbi').forEach(function(x){x.remove()});var t=c.textContent.replace(/\s+/g,' ').trim();t=t.replace(/^[^：:]{1,10}[：:]\s*/,'');return t}
/* ---------- đọc to ---------- */
var T={sp:1,loop:false,run:0,voice:null};
function pickVoice(){if(!SS)return;var v=SS.getVoices().filter(function(x){return /^zh/i.test(x.lang)});T.voice=v[0]||null}
if(SS){pickVoice();SS.onvoiceschanged=pickVoice}
function stop(){T.run++;if(SS)SS.cancel();document.querySelectorAll('.u3.kon').forEach(function(x){x.classList.remove('kon')})}
function say(list,i,run){
  if(run!==T.run)return;document.querySelectorAll('.u3.kon').forEach(function(x){x.classList.remove('kon')});
  if(i>=list.length){if(T.loop&&list.length){say(list,0,run)}return}
  var it=list[i],t=zhOf(it.querySelector('.zh')||it);if(!t){say(list,i+1,run);return}
  var p=it.classList.contains('u3')?it:it.closest('.u3');if(p){p.classList.add('kon');try{p.scrollIntoView({block:'nearest'})}catch(e){}}
  var u=new SpeechSynthesisUtterance(t);u.lang='zh-CN';u.rate=T.sp;if(T.voice)u.voice=T.voice;
  u.onend=function(){say(list,i+1,run)};u.onerror=function(){};SS.speak(u)}
function readList(list){stop();var r=T.run;say(list,0,r)}
function sectionUnits(h){var o=[],e=h.nextElementSibling;while(e&&!/^H[1-4]$/.test(e.tagName)){if(e.classList&&e.classList.contains('u3'))o.push(e);e=e.nextElementSibling}return o}
function speakers(){
  if(!SS||document.body.dataset.kspk)return;document.body.dataset.kspk='1';
  document.querySelectorAll('.u3').forEach(function(u){var z=u.querySelector('.zh');if(!z||!/[一-鿿]/.test(z.textContent))return;
    var b=document.createElement('button');b.type='button';b.className='kspk';b.title='Nghe câu này (giọng đọc của trình duyệt)';b.textContent='🔊';
    b.onclick=function(e){e.stopPropagation();readList([u])};u.insertBefore(b,u.firstChild.nextSibling?u.firstChild:null);z.appendChild(b)});
  document.querySelectorAll('h4').forEach(function(h){
    if(!/🎧|朗读/.test(ht(h)))return;var us=sectionUnits(h);if(us.length<1)return;
    var bar=document.createElement('div');bar.className='kbar';
    bar.innerHTML='<button type="button" class="kp">▶ Đọc cả đoạn</button><button type="button">■ Dừng</button><select><option value="0.75">0.75×</option><option value="1" selected>1×</option></select><label><input type="checkbox"> Lặp</label><small>Giọng đọc của trình duyệt, không phải bản ghi âm của giáo trình.</small>';
    bar.children[0].onclick=function(){readList(us)};bar.children[1].onclick=stop;
    bar.children[2].onchange=function(){T.sp=+this.value};bar.children[3].querySelector('input').onchange=function(){T.loop=this.checked};
    h.parentNode.insertBefore(bar,h.nextSibling)})}
/* ---------- checklist 评价 ---------- */
function evals(){
  document.querySelectorAll('h3[id$="-eval"]').forEach(function(h){
    if(h.dataset.ev)return;h.dataset.ev='1';var tb=null,e=h.nextElementSibling;while(e&&!/^H[1-3]$/.test(e.tagName)){if(e.querySelector&&e.querySelector('table')){tb=e.querySelector('table');break}e=e.nextElementSibling}
    if(!tb)return;var rows=[].slice.call(tb.querySelectorAll('tbody tr')).filter(function(r){return /☐/.test(r.cells[0].textContent)});if(rows.length<2)return;
    var st=get('ev:'+h.id)||{c:[],t:{}},prog=document.createElement('div');prog.className='kprog';tb.parentNode.insertBefore(prog,tb.nextSibling);
    function upd(){var n=rows.filter(function(r){return r.querySelector('input[type=checkbox]').checked}).length;prog.textContent='Đã tự đánh giá: '+n+'/'+rows.length}
    rows.forEach(function(r,i){var c0=r.cells[0],w=document.createTreeWalker(c0,NodeFilter.SHOW_TEXT),n,list=[];while((n=w.nextNode()))list.push(n);
      var cb=document.createElement('input');cb.type='checkbox';cb.checked=!!st.c[i];cb.onchange=function(){st.c[i]=cb.checked;put('ev:'+h.id,st);upd()};
      var first=list[0];if(first)first.nodeValue=first.nodeValue.replace(/^\s*☐\s*/,'');c0.insertBefore(cb,c0.firstChild);c0.insertBefore(document.createTextNode(' '),cb.nextSibling);
      var k=0;list.forEach(function(n){var m=n.nodeValue.split(/＿{2,}/);if(m.length<2)return;var par=n.parentNode,fr=document.createDocumentFragment();
        m.forEach(function(s,j){fr.appendChild(document.createTextNode(s));if(j<m.length-1){var inp=document.createElement('input');inp.className='kin';var key=i+'_'+(k++);inp.value=st.t[key]||'';inp.oninput=function(){st.t[key]=inp.value;put('ev:'+h.id,st)};fr.appendChild(inp)}});par.replaceChild(fr,n)});
      if(r.cells[1])r.cells[1].innerHTML=r.cells[1].innerHTML.replace(/^\s*☐\s*/,'')});
    upd()})}
/* ---------- stepper nhiệm vụ ---------- */
function steps(){
  document.querySelectorAll('h4').forEach(function(h,idx){
    if(h.dataset.st||!/^任务/.test(ht(h)))return;h.dataset.st='1';
    var last=h,e=h.nextElementSibling;while(e&&!/^H[1-4]$/.test(e.tagName)){last=e;e=e.nextElementSibling}
    var id='t'+idx,st=get('st:'+id)||{d:[0,0,0],n:['','','']};
    var p=document.createElement('div');p.className='kstep';
    p.innerHTML='<div class="kh"><span>Tiến độ nhiệm vụ</span><span class="kbarp"><i></i></span><small class="kc"></small></div>';
    var names=['Chuẩn bị','Thực hiện','Trình bày'],ph=['Từ cần dùng, ý chính…','Kết quả, số liệu, câu nói…','Điều muốn nói với lớp…'];
    names.forEach(function(nm,i){var s=document.createElement('div');s.className='ks';s.innerHTML='<label><input type="checkbox"> '+nm+'</label><textarea placeholder="'+ph[i]+'"></textarea>';
      var cb=s.querySelector('input'),ta=s.querySelector('textarea');cb.checked=!!st.d[i];ta.value=st.n[i]||'';
      cb.onchange=function(){st.d[i]=cb.checked?1:0;put('st:'+id,st);upd()};ta.oninput=function(){st.n[i]=ta.value;put('st:'+id,st)};p.appendChild(s)});
    function upd(){var n=st.d.reduce(function(a,b){return a+b},0);p.querySelector('i').style.width=(100*n/3)+'%';p.querySelector('.kc').textContent=n+'/3'}
    last.parentNode.insertBefore(p,last.nextSibling);upd()})}
/* ---------- huy hiệu hình thức + đồng hồ ---------- */
function forms(t){
  if(/头脑风暴/.test(t))return 'Động não';if(/角色扮演/.test(t))return 'Đóng vai';if(/看图说话/.test(t))return 'Nhìn hình nói';
  if(/结果展示/.test(t))return 'Trình bày';if(/两人|双人/.test(t))return 'Cặp đôi';if(/[三四五六][至到]?[四五六]?人|小组|多人/.test(t))return 'Nhóm';return null}
function act(){
  document.querySelectorAll('h4').forEach(function(h,idx){
    if(h.dataset.ac||/🎧|^任务|词语表|📝/.test(ht(h)))return;var f=forms(ht(h));if(!f)return;h.dataset.ac='1';
    var bar=document.createElement('div');bar.className='kbar';bar.innerHTML='<span class="kbadge"></span><button type="button" class="kp">⏱ Bắt đầu</button><select><option value="60">1 phút</option><option value="120" selected>2 phút</option><option value="180">3 phút</option><option value="300">5 phút</option></select><span class="kt">2:00</span>';
    bar.firstChild.textContent=f;var go=bar.querySelector('button'),sel=bar.querySelector('select'),tv=bar.querySelector('.kt'),left=120,iv=null;
    function show(){tv.textContent=Math.floor(left/60)+':'+('0'+left%60).slice(-2);tv.classList.toggle('end',left===0)}
    sel.onchange=function(){left=+sel.value;show()};
    go.onclick=function(){if(iv){clearInterval(iv);iv=null;go.textContent='⏱ Tiếp tục';return}if(left<=0){left=+sel.value}go.textContent='⏸ Tạm dừng';iv=setInterval(function(){left--;show();if(left<=0){clearInterval(iv);iv=null;go.textContent='⏱ Bắt đầu'}},1000)};
    h.parentNode.insertBefore(bar,h.nextSibling);
    if(/头脑风暴/.test(ht(h))){var ta=document.createElement('textarea');ta.className='knote';ta.placeholder='Ghi nhanh ý tưởng (mỗi ý một dòng)…';var kk='bs:'+idx,sv=get(kk);ta.value=sv||'';ta.oninput=function(){put(kk,ta.value)};bar.parentNode.insertBefore(ta,bar.nextSibling)}})}
function all(){try{speakers()}catch(e){console.error(e)}try{evals()}catch(e){console.error(e)}try{steps()}catch(e){console.error(e)}try{act()}catch(e){console.error(e)}}
function go(){setTimeout(all,800);setTimeout(all,2600)}
if(document.readyState==='complete')go();else addEventListener('load',go);
})();
"""

def main(path):
    h = open(path, encoding='utf-8').read()
    m = re.search(r'(<script type="application/json" id="src-ky">)(.*?)(</script>)', h, re.S)
    d = json.loads(m.group(2))
    # dọn thẻ <a> lồng nhau do bước liên kết KB
    d, n = re.subn(r'(<a class="kbl[^>]*>)\1(.*?)</a></a>', r'\1\2</a>', d, flags=re.S)
    if '.kspk{' not in d:
        d = d.replace('</style>', CSS + '</style>', 1)
        i = d.rfind('</body>')
        d = d[:i] + '<script>' + JS + '</script>' + d[i:]
    h = h[:m.start(2)] + json.dumps(d, ensure_ascii=False).replace('<', '\\u003c') + h[m.end(2):]
    open(path, 'w', encoding='utf-8').write(h)
    print('ky_cardui: đã chèn; gỡ %d thẻ <a> lồng nhau' % n)

if __name__ == '__main__':
    main(sys.argv[1])
