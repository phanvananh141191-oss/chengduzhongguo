"""Thẻ «Cách học» (webp) gập/mở ngay đầu mỗi bài fz/ky/ld. Chạy sau add_method.py."""
import re, sys, json, base64, os
A = os.path.join(os.path.dirname(__file__), '..', 'assets', 'cach_hoc_bai')
BOOK = {'fz': 'fz.webp', 'ky': 'ky.webp', 'ld': 'ld.webp'}
KBK = {'fz': 'categories/00-study-method/01-fz-phat-trien-han-ngu.md', 'ky': 'categories/00-study-method/02-ky-khau-ngu-thoi-dai-moi.md', 'ld': 'categories/00-study-method/03-ld-lac-doc.md'}
CSS = ".mth{margin:10px 0;border:1px solid var(--bd,#0002);border-radius:10px;padding:6px 12px;background:var(--card,#fff8)}.mth>summary{cursor:pointer;font-weight:600}.mth img{display:block;width:min(460px,100%);height:auto;margin:10px auto;border-radius:12px}.mth .mk{font-size:.88em}"
SEL = {'fz': "h1", 'ky': "p.kbrow", 'ld': "#lcr"}
def js(b, data):
    return ("(function(){var D=%s,K=%s;function box(){var d=document.createElement('details');d.className='mth';d.dataset.mth='1';"
            "d.innerHTML='<summary>🧭 Cách học giáo trình này (thẻ 1 trang)</summary><img alt=\"Cách học\" src=\"'+D+'\"><p class=\"mk\"><a href=\"#\" class=\"mkl\">📘 Mở trang Cách học trong Knowledge Base</a></p>';"
            "d.querySelector('.mkl').onclick=function(e){e.preventDefault();try{parent.postMessage({u3:1,book:'%s',t:'nav',key:'kb:'+K},'*')}catch(x){}};return d}"
            "function add(){document.querySelectorAll('%s').forEach(function(e){if(e.tagName=='H1'&&!/第\\d+课/.test(e.textContent))return;var n=e.nextElementSibling;if(n&&n.dataset&&n.dataset.mth)return;if(e.dataset.mthd)return;e.dataset.mthd='1';e.insertAdjacentElement('afterend',box())})}"
            "new MutationObserver(add).observe(document.body,{childList:true,subtree:true});addEventListener('load',add);add()})();") % (json.dumps(data), json.dumps(KBK[b]), b, SEL[b])
def main(path):
    h = open(path, encoding='utf-8').read(); n = {}
    for b, f in BOOK.items():
        m = re.search(r'(<script type="application/json" id="src-%s">)(.*?)(</script>)' % b, h, re.S); d = json.loads(m.group(2))
        if 'class="mth"' not in d and 'd.className=\'mth\'' not in d:
            data = 'data:image/webp;base64,' + base64.b64encode(open(os.path.join(A, f), 'rb').read()).decode()
            d = d.replace('</style>', CSS + '</style>', 1)
            i = d.rfind('</body>'); d = d[:i] + '<script>' + js(b, data) + '</script>' + d[i:]; n[b] = 1
        h = h[:m.start(2)] + json.dumps(d, ensure_ascii=False).replace('<', '\\u003c') + h[m.end(2):]
    open(path, 'w', encoding='utf-8').write(h); print('add_method_inline:', list(n))
if __name__ == '__main__': main(sys.argv[1])
