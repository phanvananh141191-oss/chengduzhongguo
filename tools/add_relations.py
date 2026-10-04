"""Sơ đồ quan hệ nhân vật (webp) → hộp «Bảng tên nhân vật» của các bài ky + trang KB nhân vật.
Dùng: python3 tools/add_relations.py <html>   (chạy sau add_method.py)"""
import re, sys, json, base64, os
ROOT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'nhan_vat')
IMG = {'rel1': 'quan_he_nhom_ban.webp', 'rel2': 'quan_he_vuong_tinh_tinh.webp', 'rel3': 'quan_he_ly_nham.webp'}
GROUP = {
 'rel1': ('Nhóm bạn cùng lớp', ['井上翔', '朴智慧', '冯尚德', '陈新阳', '马波罗', '爱娜', '田梦', '丁思思', '思思表哥'],
          '马波罗 (trung tâm) là 同学 bạn học của 井上翔, 朴智慧, 冯尚德, 陈新阳 và 爱娜; 朋友 bạn bè với 田梦. 爱娜 và 田梦 cũng là 朋友. 田梦 và 丁思思 là 同屋、同学 (bạn cùng phòng, bạn học); 丁思思 và 思思表哥 là 表兄妹 (anh em họ).'),
 'rel2': ('王晴晴的人物关系 · Quan hệ của Vương Tình Tình', ['王晴晴', '林凯', '王珊珊', '陈武', '陈文'],
          '林凯 là 表哥 (anh họ bên ngoại), 王珊珊 là 姐姐 (chị gái), 陈武 là 男朋友 (bạn trai), 陈文 là 堂哥 (anh họ bên nội) của 王晴晴.'),
 'rel3': ('李岩的家人和朋友 · Gia đình và bạn bè của Lý Nham', ['李岩', '张丽', '李小岩', '王勇'],
          '张丽 là 妻子 (vợ) và 李小岩 là 儿子 (con trai) của 李岩; 王勇 là 朋友 (bạn) của 李岩.'),
}

def lesson_names():
    out = {}
    for n in range(1, 13):
        t = open(os.path.join(os.path.dirname(__file__), '..', 'nguon_md_ky', 'chuan', 'Bai%02d.md' % n), encoding='utf-8').read()
        m = re.search(r'## Bảng tên nhân vật\n(.*?)(?=\n## )', t, re.S)
        out[n] = m.group(1) if m else ''
    return out

CSS = ".relfig{margin:12px 0}.relfig img{display:block;width:min(720px,100%);height:auto;border-radius:12px;box-shadow:0 2px 10px #0002}.relfig figcaption{font-size:.88em;color:var(--mut);margin-top:6px;line-height:1.55}"

def main(path):
    h = open(path, encoding='utf-8').read()
    imgs = {k: 'data:image/webp;base64,' + base64.b64encode(open(os.path.join(ROOT, f), 'rb').read()).decode() for k, f in IMG.items()}
    # ---- ky ----
    m = re.search(r'(<script type="application/json" id="src-ky">)(.*?)(</script>)', h, re.S); d = json.loads(m.group(2))
    names = lesson_names(); cnt = [0]
    if 'class="relfig"' not in d:
        def fig(n):
            parts = []
            for k, (title, who, cap) in GROUP.items():
                if any(w in names[n] for w in who):
                    parts.append('<figure class="relfig"><img data-rel="%s" alt="%s"><figcaption><b>%s.</b> %s</figcaption></figure>' % (k, title, title, cap)); cnt[0] += 1
            return ''.join(parts)
        i = [0]
        def rep(mm):
            i[0] += 1; return mm.group(0)[:-len('</details>')] + fig(i[0]) + '</details>'
        d = re.sub(r'<details class="kbn"><summary>Bảng tên nhân vật</summary>.*?</details>', rep, d, flags=re.S)
        js = "(function(){var R=%s;function f(){document.querySelectorAll('img[data-rel]').forEach(function(i){if(!i.src)i.src=R[i.dataset.rel]})}addEventListener('load',function(){f();setTimeout(f,1500)})})();" % json.dumps(imgs)
        d = d.replace('</style>', CSS + '</style>', 1)
        j = d.rfind('</body>'); d = d[:j] + '<script>' + js + '</script>' + d[j:]
    h = h[:m.start(2)] + json.dumps(d, ensure_ascii=False).replace('<', '\\u003c') + h[m.end(2):]
    # ---- KB ----
    m = re.search(r'(<script type="application/json" id="src-kb">)(.*?)(</script>)', h, re.S); d = json.loads(m.group(2))
    mj = re.search(r'(<script id="kb" type="application/json">)(.*?)(</script>)', d, re.S)
    kb = json.loads(mj.group(2).replace('<\\/', '</'))
    key = 'categories/01-foundation/01-characters.md'
    if '(img:rel1)' not in kb[key]:
        sec = ['', '## Sơ đồ quan hệ nhân vật', '']
        for k, (title, who, cap) in GROUP.items():
            lessons = [n for n in range(1, 13) if any(w in names[n] for w in who)]
            sec += ['### ' + title, '', '![%s](img:%s)' % (title, k), '', cap, '', 'Xuất hiện trong: ' + ' · '.join('[Bài %d](app:ky:l%02d)' % (n, n) for n in lessons), '']
        t = kb[key]; i = t.find('\n## Bài 01')
        kb[key] = t[:i] + '\n' + '\n'.join(sec) + t[i:]
    d = d[:mj.start(2)] + json.dumps(kb, ensure_ascii=False).replace('</', '<\\/') + d[mj.end(2):]
    mi = re.search(r'const IMGS=(\{.*?\});', d, re.S)
    o = json.loads(mi.group(1)) if mi else {}
    if mi and 'rel1' not in o:
        o.update(imgs)
        d = d[:mi.start(1)] + json.dumps(o) + d[mi.end(1):]
    h = h[:m.start(2)] + json.dumps(d, ensure_ascii=False).replace('<', '\\u003c') + h[m.end(2):]
    open(path, 'w', encoding='utf-8').write(h)
    print('add_relations: %d hình gắn vào các bài ky; KB trang nhân vật cập nhật' % cnt[0])

if __name__ == '__main__':
    main(sys.argv[1])
