"""Thẻ «cách học» của từng giáo trình → Knowledge (trang KB riêng, ảnh webp) + liên kết hai chiều với bài học.
Dùng: python3 tools/add_method.py <html>"""
import re, sys, json, base64, os
ROOT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'cach_hoc')
P = 'categories/00-study-method/'
FILES = {
 'fz': (P + '01-fz-phat-trien-han-ngu.md', 'fz.webp'),
 'ky': (P + '02-ky-khau-ngu-thoi-dai-moi.md', 'ky.webp'),
 'ld': (P + '03-ld-lac-doc.md', 'ld.webp'),
 'mt6': (P + '04-khau-ngu-muc-tieu-moi-6.md', 'ky_muc_tieu_moi_6.webp'),
}
FZ_STEPS = [('Quét bài', 'Tự thử từ và cấu trúc. Phần đã biết đi nhanh; chỉ học sâu chỗ còn hổng.'),
 ('Đọc & nghe bài khóa', 'Nắm ý chính; nghe đoạn mới 3–5 phút trước khi xem lời thoại. Đóng sách kể lại.'),
 ('Chọn từ mới', 'Ưu tiên từ cần dùng hoặc gặp nhiều. Bắt đầu tối đa 12 thẻ mỗi bài trung cấp.'),
 ('Dùng ngữ pháp', 'Tự đặt câu mới với cấu trúc quan trọng; sửa một lỗi dễ nhầm bằng cặp sai–đúng.'),
 ('Làm bài tập', 'Chọn bài nhớ lại, bài nghe ngắn và bài tự nói/viết. Tối đa 20 phút trong giờ học sách.'),
 ('Đóng sách kiểm tra', 'Nói lại ý chính và dùng cấu trúc trong câu của mình; có thể ghi âm tối đa 5 câu.')]
FZ_REV = ('Ôn & kiểm tra', 'Ôn thẻ tối đa 20 phút/ngày. Sau ít nhất 7 ngày, thử dùng lại nội dung cũ. Cứ 5 bài làm 20 câu trộn, hướng tới 16/20.', 'Ngày 60 phút học song song: tối đa 25 phút cho sách này.')
KY_STEPS = [('Xem nhiệm vụ', 'Đọc phần nhiệm vụ (PRODUCE) trước. Gạch 3 ý muốn nói; lập ý tối đa 3 phút.'),
 ('Lấy cụm cần dùng', 'Xem phần chuẩn bị (PREPARE). Nghe hội thoại khi chưa nhìn chữ, rồi kiểm bằng lời thoại.'),
 ('Rút khung diễn đạt', 'Chọn 2–3 khung để nêu ý, giải thích, phản bác hoặc nhượng bộ. Không học thuộc cả hội thoại.'),
 ('Nói và ghi âm', 'Kể lại ngắn, rồi trả lời nhiệm vụ không đọc giấy. Nghe lại và sửa sau khi nói xong.'),
 ('Ôn bằng miệng', 'Nhìn tình huống gợi ý, nói khung phù hợp và đặt thêm một câu mới.')]
KY_REV = ('Ôn & kiểm tra', 'Sau ít nhất 48 giờ, nói lại không nhìn giấy. Mỗi tuần ghi âm 5 phút với câu hỏi mới; kiểm thời lượng, độ tự nhiên và cách dùng khung.', 'Ngày 60 phút: ghi khoảng 90 giây; ngày 90 phút: 2–3 phút. Phần khẩu ngữ tối đa 45 phút khi học song song.')
LD_STEPS = [('Đọc lần đầu', 'Tắt pinyin và audio, bấm giờ, chưa tra từ. Đọc xong tự nêu ý chính.'),
 ('Đọc kỹ', 'Tra từ thực sự cản hiểu. Nói lại tối đa 2 câu khó bằng tiếng Trung đơn giản.'),
 ('Áp dụng kỹ năng', 'Chọn 1–2 kỹ năng trong bài và dùng ngay trên văn bản thực hành.'),
 ('Đóng sách tóm tắt', 'Ghi âm 3–4 câu tiếng Trung nêu ý chính; dùng ít nhất một cấu trúc vừa học.'),
 ('Ôn từ trong câu', 'Từ chỉ cần để đọc thì luyện nhận nghĩa. Từ sắp nói/viết mới tập tự tạo câu.')]
LD_REV = ('Ôn & kiểm tra', 'Ngày 7 và 30: đóng sách nhắc lại ý chính. Sau mỗi 3 bài, thay một buổi bằng bài đọc lạ tối đa 20 phút, tra tối đa 8 từ.', 'Nếu hiểu dưới 3/4 ý chính, chọn bài dễ hơn. Đọc bài lạ ngoài sách 3 lần/tuần, mỗi lần tối đa 15 phút.')

def lesson_links(book, n, anchors=None):
    k = '%s:l%02d' % (book, n); out = ['[Bài %d](app:%s)' % (n, k)]
    return k

def md_fz():
    L = ['# Cách học · 发展汉语 Phát triển Hán ngữ (Trung cấp II)', '', '> Thẻ cách học của giáo trình tổng hợp — «Mở sách → làm gì?». Bấm số bài để mở thẳng bài học.', '', '![Cách học 发展汉语](img:fz)', '', '## Mở sách → làm gì?', '']
    for i, (t, d) in enumerate(FZ_STEPS, 1): L.append('%d. **%s** — %s' % (i, t, d))
    L += ['', '**%s.** %s' % FZ_REV[:2], '', '**Nhớ:** ' + FZ_REV[2], '', '> Một bài học = một đầu ra tự kiểm tra được.', '', '## Áp dụng vào bài học', '',
          'Bấm để mở bài (mỗi bài có đủ 题解 · 词语学习 · 走进课文 · 综合注释 · 综合练习):', '']
    L.append(' · '.join('[Bài %d](app:fz:l%02d)' % (n, n) for n in range(1, 15)))
    L += ['', 'Tra cứu xuyên bài: [Bảng ngữ pháp 语法点总表](app:fz:grammar-index) · [Bảng từ ngữ 词语总表](app:fz:word-index)']
    return '\n'.join(L)

def md_ky():
    L = ['# Cách học · 新时代汉语口语 Khẩu ngữ thời đại mới (准高级·上)', '', '> Thẻ cách học của giáo trình khẩu ngữ — mỗi bài hoàn thành một nhiệm vụ nói bằng lời của mình. Mỗi bước dưới đây liên kết thẳng tới phần tương ứng của bài.', '', '![Cách học 新时代汉语口语](img:ky)', '', '## Mở sách → làm gì?', '']
    for i, (t, d) in enumerate(KY_STEPS, 1): L.append('%d. **%s** — %s' % (i, t, d))
    L += ['', '**%s.** %s' % KY_REV[:2], '', '**Nhớ:** ' + KY_REV[2], '', '> Một bài học = một đầu ra tự kiểm tra được.', '', '## Áp dụng vào từng bài', '',
          '| Bài | 1 · Nhiệm vụ | 2 · Chuẩn bị | 3 · Khung diễn đạt (hội thoại) | 4 · Nói & ghi âm (bài nghe) | 5 · Tự đánh giá |', '|---|---|---|---|---|---|']
    for n in range(1, 13):
        k = 'ky:l%02d' % n
        L.append('| [Bài %d](app:%s) | [PRODUCE](app:%s::s%d-produce) | [PREPARE](app:%s::s%d-prepare) | [Hội thoại](app:%s::s%d-dialog) | [录音文本](app:%s::s%d-appx) | [评价](app:%s::s%d-eval) |' % (n, k, k, n, k, n, k, n, k, n, k, n))
    L += ['', 'Bảng từ tổng hợp: [词语总表](app:ky:word-index)']
    return '\n'.join(L)

def md_ld():
    L = ['# Cách học · 乐读 Lạc độc (Đọc hiểu, tập 3–6)', '', '> Thẻ cách học của giáo trình đọc hiểu. Bấm số bài để mở bài; trong bài có các tab 精读 · 泛读 · 实况阅读 · Kỹ năng.', '', '![Cách học 乐读](img:ld)', '', '## Mở sách → làm gì?', '']
    for i, (t, d) in enumerate(LD_STEPS, 1): L.append('%d. **%s** — %s' % (i, t, d))
    L += ['', '**%s.** %s' % LD_REV[:2], '', '**Nhớ:** ' + LD_REV[2], '', '> Một bài học = một đầu ra tự kiểm tra được.', '', '## Áp dụng vào bài học', '',
          'Tổng quan: [十二课总览](app:ld:hub)', '', ' · '.join('[Bài %d](app:ld:l%02d)' % (n, n) for n in range(1, 13)), '',
          'Ngân hàng kiến thức: [常用字](app:ld:bank-morpheme) · [书面词](app:ld:bank-formal) · [格式](app:ld:bank-pattern) · [固定搭配](app:ld:bank-chunk) · [Parsing Lab](app:ld:bank-parsing) · [Scanning](app:ld:bank-scanning)']
    return '\n'.join(L)

def md_mt6():
    return '\n'.join(['# Cách học · Khẩu ngữ Mục tiêu mới 6 (giáo trình khác)', '', '> Thẻ cách học của một giáo trình khẩu ngữ khác (03 / Khẩu ngữ). Giáo trình này **không có bài trong file tổng hợp hiện tại**, chỉ lưu thẻ để tham khảo.', '', '![Cách học Khẩu ngữ Mục tiêu mới 6](img:mt6)', '',
        '**Cách học tương tự** giáo trình đang có: [Khẩu ngữ Thời đại mới](app:kb:' + FILES['ky'][0] + ').'])

CSS = ".mimg{display:block;width:min(560px,100%);height:auto;border-radius:14px;margin:12px auto;box-shadow:0 2px 12px #0002}a.app{color:var(--ac,#a8322b);text-decoration:none;border-bottom:1px dotted currentColor}"
CLICK = "document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a.app');if(!a)return;e.preventDefault();try{parent.postMessage({u3:1,book:'kb',t:'nav',key:a.dataset.nav},'*')}catch(x){}});"

def main(path):
    h = open(path, encoding='utf-8').read()
    # ---------- KB ----------
    m = re.search(r'(<script type="application/json" id="src-kb">)(.*?)(</script>)', h, re.S)
    d = json.loads(m.group(2))
    mj = re.search(r'(<script id="kb" type="application/json">)(.*?)(</script>)', d, re.S)
    kb = json.loads(mj.group(2).replace('<\\/', '</'))
    mds = {FILES['fz'][0]: md_fz(), FILES['ky'][0]: md_ky(), FILES['ld'][0]: md_ld(), FILES['mt6'][0]: md_mt6()}
    new = {}; ins = False
    for k, v in kb.items():
        if k.startswith('categories/') and not ins: new.update(mds); ins = True
        if k not in mds: new[k] = v
    if not ins: new.update(mds)
    kbs = json.dumps(new, ensure_ascii=False).replace('</', '<\\/')
    d = d[:mj.start(2)] + kbs + d[mj.end(2):]
    imgs = {k: 'data:image/webp;base64,' + base64.b64encode(open(os.path.join(ROOT, f), 'rb').read()).decode() for k, (_, f) in FILES.items()}
    if 'const IMGS=' not in d:
        d = d.replace('const KB=JSON.parse', 'const IMGS=' + json.dumps(imgs) + ';\nconst KB=JSON.parse', 1)
        d = d.replace("  s=s.replace(/\\[([^\\]]+)\\]\\(([^)\\s]+)\\)/g,(m,tx,u)=>{",
            "  s=s.replace(/!\\[([^\\]]*)\\]\\(img:(\\w+)\\)/g,(m,a,k)=>IMGS[k]?'<img class=\"mimg\" alt=\"'+a+'\" src=\"'+IMGS[k]+'\">':'');\n  s=s.replace(/\\[([^\\]]+)\\]\\(app:([^)\\s]+)\\)/g,'<a href=\"#\" class=\"app\" data-nav=\"$2\">$1</a>');\n  s=s.replace(/\\[([^\\]]+)\\]\\(([^)\\s]+)\\)/g,(m,tx,u)=>{", 1)
        assert 'IMGS[k]' in d
        d = d.replace('</style>', CSS + '</style>', 1)
        i = d.rfind('</script>'); d = d[:i] + '\n' + CLICK + '\n' + d[i:]
    h = h[:m.start(2)] + json.dumps(d, ensure_ascii=False).replace('<', '\\u003c') + h[m.end(2):]
    # ---------- TOC ----------
    t = re.search(r'(<script type="application/json" id="toc-data">)(.*?)(</script>)', h, re.S)
    toc = json.loads(t.group(2))
    g0 = toc['parts'][0]['groups']
    if not any(g.get('name') == 'Cách học theo giáo trình' for g in g0):
        items = [dict(key='kb:' + FILES['fz'][0], n='01', zh='发展汉语', vi='Cách học · Phát triển Hán ngữ'),
                 dict(key='kb:' + FILES['ky'][0], n='02', zh='新时代汉语口语', vi='Cách học · Khẩu ngữ thời đại mới'),
                 dict(key='kb:' + FILES['ld'][0], n='03', zh='乐读', vi='Cách học · Lạc độc'),
                 dict(key='kb:' + FILES['mt6'][0], n='04', zh='口语·目标新6', vi='Cách học · Khẩu ngữ Mục tiêu mới 6 (giáo trình khác)')]
        g0.insert(0, {'name': 'Cách học theo giáo trình', 'sub': 'Thẻ 4 giáo trình · liên kết bài học', 'items': items, 'closed': False})
    h = h[:t.start(2)] + json.dumps(toc, ensure_ascii=False).replace('<', '\\u003c') + h[t.end(2):]
    # ---------- fz: liên kết trong từng bài ----------
    m2 = re.search(r'(<script type="application/json" id="src-fz">)(.*?)(</script>)', h, re.S); f = json.loads(m2.group(2))
    link = '<a class="xl" data-go="kb:%s" title="Thẻ cách học của giáo trình">📘 Cách học</a>' % FILES['fz'][0]
    if 'Cách học</a>' not in f:
        f, n1 = re.subn(r'(<h1>第\d+课[^<]*</h1><p class="py">[^<]*)(</p>)', lambda x: x.group(1) + ' · ' + link + x.group(2), f)
    h = h[:m2.start(2)] + json.dumps(f, ensure_ascii=False).replace('<', '\\u003c') + h[m2.end(2):]
    # ---------- ky ----------
    m3 = re.search(r'(<script type="application/json" id="src-ky">)(.*?)(</script>)', h, re.S); k = json.loads(m3.group(2))
    lk = '<p class="kbrow">📘 <a class="xl" data-go="kb:%s">Cách học giáo trình này</a> (thẻ 5 bước: nhiệm vụ → chuẩn bị → khung diễn đạt → nói &amp; ghi âm → ôn)</p>' % FILES['ky'][0]
    n3 = 0
    if 'Cách học giáo trình này' not in k:
        k, n3 = re.subn(r'(<h1>[^\n]*第[^\n]*</h1>\n<p><em>[^<]*</em></p>)', lambda x: x.group(1) + '\n' + lk, k)
    h = h[:m3.start(2)] + json.dumps(k, ensure_ascii=False).replace('<', '\\u003c') + h[m3.end(2):]
    # ---------- ld: chip trong breadcrumb (chạy lúc mở bài) ----------
    m4 = re.search(r'(<script type="application/json" id="src-ld">)(.*?)(</script>)', h, re.S); l = json.loads(m4.group(2))
    js = ("(function(){function add(){var c=document.getElementById('lcr');if(!c||c.dataset.mth)return;c.dataset.mth='1';var a=document.createElement('a');a.href='#';a.className='chip';a.textContent='📘 Cách học';a.style.marginLeft='10px';"
          "a.onclick=function(e){e.preventDefault();try{parent.postMessage({u3:1,book:'ld',t:'nav',key:'kb:%s'},'*')}catch(x){}};c.appendChild(a)}"
          "new MutationObserver(function(){add()}).observe(document.body,{childList:true,subtree:true});addEventListener('load',add)})();" % FILES['ld'][0])
    if 'Cách học' not in l:
        i = l.rfind('</body>'); l = l[:i] + '<script>' + js + '</script>' + l[i:]
    h = h[:m4.start(2)] + json.dumps(l, ensure_ascii=False).replace('<', '\\u003c') + h[m4.end(2):]
    open(path, 'w', encoding='utf-8').write(h)
    print('add_method: KB +4 trang, TOC +1 nhóm, ky liên kết %d bài' % n3)

if __name__ == '__main__':
    main(sys.argv[1])
