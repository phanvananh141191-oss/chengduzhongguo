"""Nút ▶ nghe từ vựng (mp3 trong assets/audio/words) cho fz, ky, ld. Chạy cuối build_v4.sh.
Dùng: python3 tools/add_audio_buttons.py <html>   (cần assets/audio/manifest.json + file mp3)"""
import re, sys, json, os, base64
ROOT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'audio')
CSS = ".aud{border:1px solid var(--bd,#0003);background:var(--card,#fff);color:var(--acc,#17685c);border-radius:99px;width:1.9em;height:1.9em;padding:0;font-size:.78em;line-height:1;margin-left:.5em;cursor:pointer;vertical-align:middle;font-family:inherit}.aud:hover{background:var(--u-hl,#e8efe9)}.aud.on{background:var(--acc,#17685c);color:#fff}"
SEL = {  # (chọn phần tử chứa từ, lấy từ, ô để gắn nút)
 'fz': "var R=document.querySelectorAll('tr[id*=\"-w-\"]');R.forEach(function(r){put(r.id.split('-w-').pop(),r.querySelector('td.c-w')||r.children[1])});",
 'ky': "document.querySelectorAll('a[id*=\"-w-\"]').forEach(function(a){var r=a.closest('tr');if(r)put(a.id.split('-w-').pop(),r.children[1])});",
 'ld': "document.querySelectorAll('#lbody table.std td.w,#lbody table.vtb td.c-w').forEach(function(td){put(td.textContent.trim(),td)});",
}
def js(book, M, D):
    return ("(function(){var M=%s,D=%s;function url(h){if(D[h])return D[h];var p='assets/audio/words/'+h+'.mp3';try{return new URL(p,parent.location.href).href}catch(e){return new URL(p,document.baseURI).href}}"
            "function norm(s){return s.replace(/[（(][^）)]*[A-Za-z][^）)]*[）)]/g,'').replace(/[¹²³⁴⁵⁶⁷⁸⁹⁰]/g,'').replace(/\\s+/g,' ').trim()}"
            "var cur=null,cb=null;function stop(){if(cur){cur.pause();cur=null}if(cb){cb.textContent='▶';cb.classList.remove('on');cb=null}}"
            "function play(b){var same=cb===b;stop();if(same)return;var a=new Audio(url(b.dataset.h));cur=a;cb=b;b.textContent='⏸';b.classList.add('on');a.onended=a.onerror=function(){if(cb===b)stop()};a.play().catch(function(){if(cb===b)stop()})}"
            "function put(w,cell){if(!cell||cell.dataset.aud)return;var h=M[w]||M[norm(w)];if(!h)return;cell.dataset.aud='1';var b=document.createElement('button');b.type='button';b.className='aud';b.textContent='▶';b.title='Nghe đọc';b.setAttribute('aria-label','Nghe đọc '+w);b.dataset.h=h;"
            "b.onclick=function(e){e.preventDefault();e.stopPropagation();play(b)};cell.appendChild(b)}"
            "var t=null;function run(){%s}function sched(){clearTimeout(t);t=setTimeout(run,150)}"
            "new MutationObserver(sched).observe(document.body,{childList:true,subtree:true});addEventListener('load',run);run()})();") % (json.dumps(M, ensure_ascii=False), json.dumps(D), SEL[book])

def main(path):
    man = json.load(open(os.path.join(ROOT, 'manifest.json'), encoding='utf-8'))
    h = open(path, encoding='utf-8').read(); done = {}
    for b in ('fz', 'ky', 'ld'):
        M = {i['text']: i['hash'] for i in man if i['kind'] == 'w' and i['book'] == b and os.path.exists(os.path.join(ROOT, i['file'] + '.mp3'))}
        D = {i['hash']: 'data:audio/mpeg;base64,' + base64.b64encode(open(os.path.join(ROOT, i['file'] + '.mp3'), 'rb').read()).decode()
             for i in man if i['kind'] == 'w' and i['book'] == b and i['text'] in M}   # nhúng thẳng mp3 → chạy được cả khi mở file từ máy
        m = re.search(r'(<script type="application/json" id="src-%s">)(.*?)(</script>)' % b, h, re.S); d = json.loads(m.group(2))
        if 'className=\'aud\'' not in d:
            d = d.replace('</style>', CSS + '</style>', 1)
            i = d.rfind('</body>'); d = d[:i] + '<script>' + js(b, M, D) + '</script>' + d[i:]; done[b] = len(M)
        h = h[:m.start(2)] + json.dumps(d, ensure_ascii=False).replace('<', '\\u003c') + h[m.end(2):]
    open(path, 'w', encoding='utf-8').write(h); print('add_audio_buttons: số từ có audio', done)
if __name__ == '__main__': main(sys.argv[1])
