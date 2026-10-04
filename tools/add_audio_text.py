"""Nút ▶ nghe từng câu/đoạn bài khoá (fz, ky, ld). Audio nạp theo bài từ assets/audio/pack/<sách>-l<NN>.js qua shell
(shell nạp <script> rồi gửi blob URL cho khung bài học → chạy được cả khi mở file từ máy).
Dùng: python3 tools/add_audio_text.py <html>   (chạy cuối build_v4.sh, sau add_audio_buttons.py)"""
import re, sys, json, os
ROOT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'audio')
CSS = ".aud.s{width:1.7em;height:1.7em;font-size:.7em;margin:0 .3em;opacity:.8}.aud.s:hover{opacity:1}"
SHELL_ADD = r"""var PK={};function b64blob(u){var s=atob(u.slice(u.indexOf(',')+1)),a=new Uint8Array(s.length);for(var i=0;i<s.length;i++)a[i]=s.charCodeAt(i);return new Blob([a],{type:'audio/mpeg'})}
function loadPack(b,n,cb){var k=b+'-l'+('0'+n).slice(-2);if(PK[k]){cb(PK[k]);return}
 var s=document.createElement('script');s.src=new URL('assets/audio/pack/'+k+'.js',location.href).href;
 s.onload=function(){var u=(window.__AP||{})[k]||{};PK[k]=u;try{delete window.__AP[k]}catch(e){}cb(u)};
 s.onerror=function(){cb({})};document.head.appendChild(s)}
"""
SHELL_MSG = "if(m.t==='aud'&&m.lesson){loadPack(m.book,m.lesson,function(u){try{frames[m.book].contentWindow.postMessage({u3a:'pack',book:m.book,lesson:m.lesson,urls:u},'*')}catch(e){}})}\n  "
SEL = {
 'fz': ("document.querySelectorAll('section.les .zu,section.les .ln.lz,section.les .card.txt p').forEach(function(e){var s=e.closest('section.les');var n=s&&/^l(\\d+)$/.test(s.id)?+RegExp.$1:0;put(e,n)});"),
 'ky': ("document.querySelectorAll('section div.zh').forEach(function(e){var s=e.closest('section');var n=s&&/^s(\\d+)$/.test(s.id)?+RegExp.$1:0;put(e,n)});"),
 'ld': ("document.querySelectorAll('#lbody .ptx.han').forEach(function(e){put(e,0)});"),
}
def js(book, M):
    return ("(function(){var M=%s,U={},W={},BOOK=%s;"
      "function norm(el){var c=el.cloneNode(true);c.querySelectorAll('rt,sup,button.aud,a.kbm,a.kbg,a.xl,script,.tag').forEach(function(x){x.remove()});"
      "var s=c.textContent.replace(/[¹²³⁴⁵⁶⁷⁸⁹⁰①②③④⑤⑥⑦⑧⑨⑩]/g,'').replace(/[（(][^）)]*[A-Za-z][^）)]*[）)]/g,'').replace(/\\s+/g,' ').trim();"
      "return s.replace(/([\\u4e00-\\u9fff，。！？、；：”“]) (?=[\\u4e00-\\u9fff，。！？、；：”“])/g,'$1')}"
      "var cur=null,cb=null;function stop(){if(cur){cur.pause();cur=null}if(cb){cb.textContent='▶';cb.classList.remove('on');cb=null}}"
      "function playUrl(b,u){stop();var a=new Audio(u);cur=a;cb=b;b.textContent='⏸';b.classList.add('on');a.onended=a.onerror=function(){if(cb===b)stop()};a.play().catch(function(){if(cb===b)stop()})}"
      "function click(b){if(cb===b){stop();return}var n=+b.dataset.l,id=b.dataset.id;if(U[n]){if(U[n][id])playUrl(b,U[n][id]);return}"
      "b.textContent='…';(W[n]=W[n]||[]).push(b);if(W[n].length===1)parent.postMessage({u3:1,book:BOOK,t:'aud',lesson:n},'*')}"
      "addEventListener('message',function(e){var m=e.data;if(!m||m.u3a!=='pack')return;U[m.lesson]=m.urls||{};(W[m.lesson]||[]).forEach(function(b){b.textContent='▶'});var w=W[m.lesson]||[];W[m.lesson]=[];if(w.length&&U[m.lesson][w[0].dataset.id])playUrl(w[0],U[m.lesson][w[0].dataset.id])});"
      "function put(e,n){if(e.querySelector(':scope > button.aud.s, :scope > .zh-aud'))return;var k=norm(e);var v=M[k];if(!v)return;var l=n&&v[n]?n:+Object.keys(v)[0];var id=v[l];if(!id)return;"
      "var b=document.createElement('button');b.type='button';b.className='aud s';b.textContent='▶';b.title='Nghe đọc';b.setAttribute('aria-label','Nghe đọc');b.dataset.l=l;b.dataset.id=id;b.onclick=function(ev){ev.preventDefault();ev.stopPropagation();click(b)};e.appendChild(b)}"
      "var t=null;function run(){%s}function sched(){clearTimeout(t);t=setTimeout(run,200)}"
      "new MutationObserver(sched).observe(document.body,{childList:true,subtree:true});addEventListener('load',run);run()})();") % (json.dumps(M, ensure_ascii=False), json.dumps(book), SEL[book])

def main(path):
    man = json.load(open(os.path.join(ROOT, 'manifest.json'), encoding='utf-8'))
    h = open(path, encoding='utf-8').read(); done = {}
    for b in ('fz', 'ky', 'ld'):
        M = {}
        for i in man:
            if i['kind'] == 't' and i['book'] == b: M.setdefault(i['text'], {}).setdefault(str(i['lesson']), i['id'])
        m = re.search(r'(<script type="application/json" id="src-%s">)(.*?)(</script>)' % b, h, re.S); d = json.loads(m.group(2))
        if "b.className='aud s'" not in d:
            d = d.replace('</style>', CSS + '</style>', 1)
            i = d.rfind('</body>'); d = d[:i] + '<script>' + js(b, M) + '</script>' + d[i:]; done[b] = len(M)
        h = h[:m.start(2)] + json.dumps(d, ensure_ascii=False).replace('<', '\\u003c') + h[m.end(2):]
    if 'function loadPack(' not in h:
        key = "window.addEventListener('message',function(e){var m=e.data;if(!m||!m.u3||!m.book)return;"
        assert h.count(key) == 1, h.count(key)
        h = h.replace(key, SHELL_ADD + key + "\n  " + SHELL_MSG, 1)
    open(path, 'w', encoding='utf-8').write(h); print('add_audio_text: số câu có audio', done)
if __name__ == '__main__': main(sys.argv[1])
