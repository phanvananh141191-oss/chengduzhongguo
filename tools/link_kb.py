#!/usr/bin/env python3
"""Nối ky ↔ KB hai chiều (chạy sau gen_ky): vá khung ky, khung KB và shell.
Dùng: python3 tools/link_kb.py file.html   (ghi đè tại chỗ)"""
import re, sys, json
f = sys.argv[1]
s = open(f, encoding='utf8').read()
enc = lambda d: json.dumps(d, ensure_ascii=False).replace('<', '\\u003c')
def patch_doc(book, fn):
    global s
    m = re.search(r'(<script type="application/json" id="src-%s">)(.*?)(</script>)' % book, s, re.S)
    d = json.loads(m.group(2).replace('\\u003c', '<')); d = fn(d)
    s = s[:m.start(2)] + enc(d) + s[m.end(2):]

# ------------------------------------------------------------------ khung ky
KY_JS = r'''<script>/*kb-link*/
(function(){
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a.kbl');if(!a)return;e.preventDefault();
  try{window.parent.postMessage({u3:1,book:'ky',t:'nav',key:'kb:'+a.getAttribute('data-kb')},'*')}catch(x){}});
window.addEventListener('message',function(e){var m=e.data;if(!m||!m.u3)return;
  if((m.t==='go'||m.t==='init')&&typeof m.go==='string'&&m.go.indexOf('::')>0){
    var p=m.go.split('::'),c={};for(var k in m)c[k]=m[k];c.go=p[0];
    e.stopImmediatePropagation();                       // bỏ thông điệp có «::», phát lại thông điệp sạch cho bộ xử lý gốc
    window.dispatchEvent(new MessageEvent('message',{data:c,source:e.source,origin:e.origin}));
    setTimeout(function(){var el=document.getElementById(p[1]);if(el){el.scrollIntoView({block:'start'});el.classList.add('u-flash');setTimeout(function(){el.classList.remove('u-flash')},1800)}},m.t==='init'?900:300)}
},true);
})();
</script>'''
def ky_fn(d):
    if '/*kb-link*/' in d: return d
    i = d.rfind('</body>'); return d[:i] + KY_JS + d[i:]
patch_doc('ky', ky_fn)

# ------------------------------------------------------------------ khung KB
KB_JS = r'''<script>/*kb-link*/
(function(){
var SEC=[['prepare','PREPARE'],['dialog','促成 · 对话'],['ext','促成 · 拓展'],['produce','PRODUCE'],['eval','评价'],['appx','附录']];
var og=go;go=function(){og.apply(this,arguments);try{
  var d=document.getElementById('doc');if(!d)return;
  var hs=d.querySelectorAll('h1,h2,h3,h4,h5,h6');for(var i=0;i<hs.length;i++)hs[i].id='kbh'+i;
  var h=(window.__H||decodeURIComponent(location.hash.slice(1)))||'';var a=h.split('::')[1];
  var m=/^lessons\/(\d\d)\.md$/.exec(CUR||'');
  if(m&&!d.querySelector('.kykbar')){var n=+m[1];
    var bar=document.createElement('p');bar.className='kykbar';
    bar.innerHTML='📖 <b>Mở trong sách (汉语口语)</b>: <a href="#" class="kyl" data-ky="s'+n+'">第'+n+'课 · toàn bài</a>'+SEC.map(function(x){return ' · <a href="#" class="kyl" data-ky="s'+n+'::s'+n+'-'+x[0]+'">'+x[1]+'</a>'}).join('');
    var h1=d.querySelector('h1');if(h1)h1.after(bar);else d.prepend(bar)}
  if(a){var e=document.getElementById(a);if(e)e.scrollIntoView({block:'start'})}
}catch(x){}};
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a.kyl');if(!a)return;e.preventDefault();
  try{window.parent.postMessage({u3:1,book:'kb',t:'nav',key:'ky:'+a.getAttribute('data-ky')},'*')}catch(x){}},true);
go();
})();
</script><style>.kykbar{font-size:13px;color:var(--mut);margin:.2em 0 .8em}.kykbar a{color:var(--ac);text-decoration:none;border-bottom:1px dotted var(--ac)}.kykbar a:hover{background:var(--ac2)}</style>'''
def kb_fn(d):
    if '/*kb-link*/' in d: return d
    i = d.rfind('</body>'); return d[:i] + KB_JS + d[i:]
patch_doc('kb', kb_fn)

# ------------------------------------------------------------------ shell: nhận thông điệp «nav» từ khung
NAV = ("if(m.t==='nav'&&m.key){var kk=String(m.key).split('::'),itn=BYKEY[kk[0]];if(itn){var tg=kk[0].slice(kk[0].indexOf(':')+1)+(kk[1]?'::'+kk[1]:''),bk=itn.book;frame(bk);"
       "for(var bb in frames)frames[bb].classList.toggle('on',bb===bk);if(ready[bk])send(bk,{t:'go',go:tg});else pend[bk]=tg;setCur(itn,true);"
       "document.body.classList.remove('nav','srch','more','opt-open')}}\n  ")
MARK = "if(m.t==='searchdone'){$('q').value='';document.body.classList.remove('srch')}"
if "m.t==='nav'" not in s:
    assert s.count(MARK) == 1
    s = s.replace(MARK, NAV + MARK)
open(f, 'w', encoding='utf8').write(s)
print('đã nối ky ↔ KB')
