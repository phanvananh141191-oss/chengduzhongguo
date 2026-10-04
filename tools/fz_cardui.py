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
function go(){setTimeout(function(){run();try{framesAll()}catch(e){}},900);setTimeout(function(){run();try{framesAll()}catch(e){}},2500)}
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
