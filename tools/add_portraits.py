"""Chân dung nhân vật (webp ~220px) → cột 中文 của «Bảng tên nhân vật» trong ky + thư viện ở trang KB nhân vật.
Chạy sau add_relations.py:  python3 tools/add_portraits.py <html>"""
import re, sys, json, base64, os, glob
DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'nhan_vat', 'chan_dung')
def load():
    P = {}
    for f in sorted(glob.glob(os.path.join(DIR, '*.webp'))):
        P[os.path.basename(f)[:-5]] = 'data:image/webp;base64,' + base64.b64encode(open(f, 'rb').read()).decode()
    return P
CSS_KY = ".avt{width:46px;height:46px;border-radius:50%;object-fit:cover;object-position:50% 22%;vertical-align:middle;margin-right:8px;box-shadow:0 1px 5px #0003;cursor:zoom-in;transition:all .15s}.avt.big{width:150px;height:150px;border-radius:14px;object-position:50% 50%;cursor:zoom-out;display:block;margin:4px 0}"
CSS_KB = 'img.mimg[alt^="👤"]{display:inline-block;width:112px;margin:4px;border-radius:50%;box-shadow:0 1px 6px #0003}'
def js(P):
    return ("(function(){var P=%s;function add(){document.querySelectorAll('details.kbn td:first-child').forEach(function(td){if(td.dataset.avt)return;var n=td.textContent.trim();if(!P[n])return;td.dataset.avt='1';"
            "var i=document.createElement('img');i.className='avt';i.alt=n;i.title=n;i.src=P[n];i.onclick=function(){i.classList.toggle('big')};td.insertBefore(i,td.firstChild)})}"
            "new MutationObserver(add).observe(document.body,{childList:true,subtree:true});addEventListener('load',add);add()})();") % json.dumps(P, ensure_ascii=False)
def main(path):
    P = load(); h = open(path, encoding='utf-8').read()
    m = re.search(r'(<script type="application/json" id="src-ky">)(.*?)(</script>)', h, re.S); d = json.loads(m.group(2))
    if 'className=\'avt\'' not in d:
        d = d.replace('</style>', CSS_KY + '</style>', 1)
        j = d.rfind('</body>'); d = d[:j] + '<script>' + js(P) + '</script>' + d[j:]
    h = h[:m.start(2)] + json.dumps(d, ensure_ascii=False).replace('<', '\\u003c') + h[m.end(2):]
    m = re.search(r'(<script type="application/json" id="src-kb">)(.*?)(</script>)', h, re.S); d = json.loads(m.group(2))
    mj = re.search(r'(<script id="kb" type="application/json">)(.*?)(</script>)', d, re.S)
    kb = json.loads(mj.group(2).replace('<\\/', '</')); key = 'categories/01-foundation/01-characters.md'
    keys = {n: 'pt%02d' % (i + 1) for i, n in enumerate(P)}
    if '(img:pt01)' not in kb[key]:
        sec = ['## Chân dung nhân vật', '', 'Bấm vào tên trong bảng của từng bài để phóng to chân dung.', '']
        sec.append(' '.join('![👤%s](img:%s)' % (n, k) for n, k in keys.items())); sec.append('')
        t = kb[key]; i = t.find('## Sơ đồ quan hệ nhân vật')
        kb[key] = t[:i] + '\n'.join(sec) + '\n' + t[i:]
    d = d[:mj.start(2)] + json.dumps(kb, ensure_ascii=False).replace('</', '<\\/') + d[mj.end(2):]
    mi = re.search(r'const IMGS=(\{.*?\});', d, re.S); o = json.loads(mi.group(1))
    if 'pt01' not in o:
        o.update({keys[n]: v for n, v in P.items()}); d = d[:mi.start(1)] + json.dumps(o) + d[mi.end(1):]
        d = d.replace('</style>', CSS_KB + '</style>', 1)
    h = h[:m.start(2)] + json.dumps(d, ensure_ascii=False).replace('<', '\\u003c') + h[m.end(2):]
    open(path, 'w', encoding='utf-8').write(h); print('add_portraits: %d chân dung' % len(P))
if __name__ == '__main__': main(sys.argv[1])
