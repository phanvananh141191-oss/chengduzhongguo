#!/usr/bin/env python3
"""P4 (giai đoạn 1): đưa fz bài 5–14 về khung 5 mục chuẩn — chỉ đổi vỏ, không đổi chữ nội dung.
Dùng: python3 tools/sync_fz.py vào.html ra.html"""
import re, sys, json
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf8').read()
m = re.search(r'(<script type="application/json" id="src-fz">)(.*?)(</script>)', s, re.S)
doc = json.loads(m.group(2).replace('\\u003c', '<'))

PG = re.compile(r',\s*((?:tr\.\s*|P)\d+(?:[–-]\d+)?)')
def split_page(t):
    """Tách số trang khỏi tiêu đề → (tiêu đề sạch, nhãn trang|None)."""
    pages = []
    def grab(mm): pages.append(mm.group(1)); return ''
    t = PG.sub(grab, t)
    def paren(mm):
        inner = mm.group(1)
        if re.fullmatch(r'\s*(?:tr\.\s*|P)\d+(?:[–-]\d+)?\s*', inner) or re.search(r'^(?:Giới thiệu bài|Vào bài đọc|Chú thích ngữ pháp tổng hợp|Bài tập tổng hợp)', inner) is None and re.search(r'(?:tr\.\s*|P)\d+', inner):
            pages.append(re.search(r'(?:tr\.\s*|P)\d+(?:[–-]\d+)?', inner).group(0)); return ''
        return mm.group(0)
    t = re.sub(r'\s*[（(]([^()（）]*)[)）]', paren, t)
    return re.sub(r'\s+', ' ', t).strip().replace(' :', ':'), (pages[0] if pages else None)

H2MAP = [  # (regex, nhãn chuẩn, cấp mới)
    (r'^题解', '题解 · Giới thiệu chủ đề', 2),
    (r'^词语学习', '词语学习 · Học từ vựng', 2),
    (r'^走进课文', '走进课文 · Tìm hiểu bài đọc', 2),
    (r'^(边栏问题|Câu hỏi bên lề)', '课文旁问题 · Câu hỏi bên lề', 3),
    (r'^(注释|Chú thích \(注释)', '注释 · Chú thích', 3),
    (r'^综合注释', '综合注释 · Chú giải tổng hợp', 2),
    (r'^综合练习', '综合练习 · Luyện tập tổng hợp', 2),
    (r'^附录', '附录 · Phụ lục', 2),
]
ADDED = {}
DUP = []
BANNER = '<div class="note"><b>Chưa có trong nguồn.</b> Tài liệu gốc không có phần này; không tự bổ sung.</div>'


UANS = '<div class="ansh">✍️ Ô nhập của bạn</div><textarea class="uans" data-k="%s" placeholder="Nhập bài làm của bạn — tự lưu trên trình duyệt."></textarea>'
def add_inputs(sec, n):
    """Mỗi khối .ans chưa có ô nhập → thêm đúng một textarea.uans (khoá mới nối tiếp, không đụng khoá cũ)."""
    keys = [int(x) for x in re.findall(r'ans:fz:l%d:e(\d+)' % n, sec)]
    nxt = (max(keys) + 1) if keys else 0
    out = []; i = 0; added = 0
    while True:
        j = sec.find('<div class="ans"', i)
        if j < 0: out.append(sec[i:]); break
        depth = 0; k = j
        for mm in re.finditer(r'<div\b|</div>', sec[j:]):
            depth += 1 if mm.group(0) == '<div' else -1
            if depth == 0: k = j + mm.start(); break
        block = sec[j:k]
        out.append(sec[i:j])
        if 'class="uans"' not in block:
            block += UANS % ('ans:fz:l%d:e%d' % (n, nxt)); nxt += 1; added += 1
        out.append(block); i = k
    return ''.join(out), added


def parse_blocks(sec):
    """Tách bài thành khối: (cấp, tiêu đề, tiền tố mở thẻ, thân). Thẻ <div class="card…"> mở ngay trước heading được gắn vào heading đó."""
    parts = re.split(r'(<h[1-4][^>]*>.*?</h[1-4]>)', sec, flags=re.S)
    head = parts[0]; blocks = []; pre = ''
    OPEN = re.compile(r'<div class="card(?: ex)?">\s*$')
    items = []
    for i in range(1, len(parts), 2):
        mm = re.fullmatch(r'<h([1-4])([^>]*)>(.*?)</h[1-4]>', parts[i], re.S)
        items.append([int(mm.group(1)), mm.group(3), parts[i + 1] if i + 1 < len(parts) else ''])
    cur_pre = [''] * len(items)
    prev_body_owner = None
    for k in range(len(items)):
        body = items[k][2]
        if k + 1 < len(items):
            o = OPEN.search(body)
            if o: cur_pre[k + 1] = o.group(0); items[k][2] = body[:o.start()]
    for k, (lv, t, b) in enumerate(items):
        blocks.append(dict(lv=lv, t=t, pre=cur_pre[k], body=b))
    for b in blocks:
        txt = b['pre'] + b['body']
        assert len(re.findall(r'<div\b', txt)) - len(re.findall(r'</div>', txt)) - (1 if b['pre'] else 0) + (1 if b['pre'] else 0) in (0, -1, 1), b['t']
    return head, blocks

def emit(b, lv, title, page=None, body=True):
    h = f'{b["pre"]}<h{lv}>{title}</h{lv}>' + (f'<p class="py pg">{page}</p>' if page else '')
    return h + (b['body'] if body else '')

def H(lv, title, page=None):
    return f'<h{lv}>{title}</h{lv}>' + (f'<p class="py pg">{page}</p>' if page else '')

def restructure(sec, n):
    head, bl = parse_blocks(sec)
    def find(prefix):
        r = [b for b in bl if b['t'].startswith(prefix)]
        assert len(r) == 1, (n, prefix, len(r)); return r[0]
    out = [head]
    clean = lambda t: split_page(t)[0]
    pg = lambda t: split_page(t)[1]
    def bal(x): return len(re.findall(r'<div\b', x)) - len(re.findall(r'</div>', x))
    if n == 3:
        b = bl[0]; out.append(emit(b, 1, b['t']))
        for pre_, lab, pgx in [('题解', '题解 · Giới thiệu chủ đề', None),
                               ('词语学习', '词语学习 · Học từ vựng', 'P35–P36'),
                               ('走进课文', '走进课文 · Tìm hiểu bài đọc', 'P37–P39')]:
            b = find(pre_); out.append(emit(b, 2, lab, pgx))
        out.append(emit(find('注释'), 3, '注释 · Chú thích'))
        out.append(emit(find('课文思考题'), 3, '课文旁问题 · Câu hỏi bên lề'))
        out.append(emit(find('PHẦN 2'), 3, 'Đáp án câu hỏi bài khóa'))
        out.append(emit(find('综合注释'), 2, '综合注释 · Chú giải tổng hợp', 'P39'))
        for i, pgx in enumerate(['P40', 'P40', 'P41', 'P42', 'P43'], 1):
            b = find('3.%d ' % i); out.append(emit(b, 3, '%d. ' % i + clean(b['t'][4:]), pgx))
        out.append(H(2, '综合练习 · Luyện tập tổng hợp'))
        for pre_ in ['一、字词知识', '二、理解新词语']:
            b = find(pre_); out.append(emit(b, 3, clean(b['t']), pg(b['t'])))
        for pre_ in ['（一）教', '（二）白']:
            b = find(pre_); out.append(emit(b, 4, clean(b['t'])))
        for pre_ in ['三、', '四、', '五、', '六、', '七、', '八、', '九、', '十、']:
            b = find(pre_)
            t = re.sub(r'[，,]?\s*gợi ý', '', b['t']); t = t.replace('（）', '').replace('()', '')
            out.append(emit(b, 3, clean(t), pg(t)))
        # PHẦN 3/4/5: tiêu đề rỗng, bỏ
        for pre_ in ['PHẦN 3', 'PHẦN 4', 'PHẦN 5']:
            assert find(pre_)['body'].strip() == ''
    elif n == 4:
        b = bl[0]; out.append(emit(b, 1, b['t']))
        out.append(emit(find('题解'), 2, '题解 · Giới thiệu chủ đề'))
        out.append(emit(find('词语学习'), 2, '词语学习 · Học từ vựng', 'P52–P53'))
        miss = find('Ghi chú về phần còn thiếu')
        out.append(H(2, '走进课文 · Tìm hiểu bài đọc') + BANNER + miss['body'])
        out.append(emit(find('一、课文问答'), 3, '课文旁问题 · Câu hỏi bên lề', 'P54–P55'))
        out.append(emit(find('二、语法练习'), 2, '综合注释 · Chú giải tổng hợp', 'P56–P60'))
        for i, pgx in enumerate(['P56', 'P57', 'P58', 'P59', 'P60'], 1):
            b = find('2.%d ' % i); out.append(emit(b, 3, '%d. ' % i + clean(b['t'][4:]), pgx))
        out.append(H(2, '综合练习 · Luyện tập tổng hợp'))
        out.append(emit(find('2.6 '), 3, '一、目字旁／目字底填空', 'P60'))
        b3 = find('三、汉字与词语练习'); out.append(b3['body'])
        out.append(emit(find('一、汉字'), 3, '二、汉字', 'P61–P62'))
        for pre_ in ['（一）相', '（二）场']:
            b = find(pre_); out.append(emit(b, 4, b['t']))
        out.append(emit(find('三、连线'), 3, '三、连线'))
        out.append(emit(find('四、选词填空'), 3, '四、选词填空（登、赶忙、迫切、意识、出行、纷纷、打量）') + BANNER)
    r = ''.join(out)
    for a, b in [('<th>词语</th>', '<th>词</th>'), ('<th>Loại từ</th>', '<th>词性</th>'), ('<th>Hán Việt</th>', '<th>Hán-Việt</th>')]:
        r = r.replace(a, b, 1)          # tiêu đề cột bảng từ (bảng đầu tiên)
    assert bal(r) == bal(sec), (n, bal(r), bal(sec))
    assert len(re.findall(r'class="ans"', r)) == len(re.findall(r'class="ans"', sec))
    return r


VT = json.load(open(__import__('os').path.join(__import__('os').path.dirname(__file__), 'vt_baked.json'), encoding='utf8'))
HDR = {'<th>词</th>': '<th>词</th>', '<th>Hán Việt</th>': '<th>Hán-Việt</th>', '<th>Nghĩa</th>': '<th>Nghĩa tiếng Việt</th>'}
def bake_vt(n):
    """Bảng từ bài 1–2: ghi sẵn vào HTML (M6), thêm cột #, chuẩn tên cột; cột English chỉ có ở bài 1 (nguồn có dữ liệu)."""
    t = VT['l%d' % n].replace(' class="u-pyc"', '')
    for a, b in HDR.items(): t = t.replace(a, b)
    rows = re.findall(r'<tr>.*?</tr>', t, re.S)
    out = ['<tr><th>#</th>' + rows[0][4:]]
    for i, r in enumerate(rows[1:], 1): out.append('<tr><td>%d</td>' % i + r[4:])
    return '<table class="vt">' + ''.join(out) + '</table>'

def restructure12(sec, n):
    def bal(x): return len(re.findall(r'<div\b', x)) - len(re.findall(r'</div>', x))
    r = sec
    # bảng từ: ghi sẵn
    assert '<table class="vt"></table>' in r
    r = r.replace('<table class="vt"></table>', bake_vt(n), 1)
    if n == 1:
        sub = [('<h2>题解 · Giới thiệu</h2>', '<h2>题解 · Giới thiệu chủ đề</h2>'),
               ('<h2>词语学习 · Từ vựng</h2>', '<h2>词语学习 · Học từ vựng</h2>'),
               ('<h2>走进课文 · Bài khóa</h2>', '<h2>走进课文 · Tìm hiểu bài đọc</h2>'),
               ('<h2>综合注释 · Chú thích ngữ pháp</h2>', '<h2>综合注释 · Chú giải tổng hợp</h2>'),
               ('<h2>综合注释 · Ví dụ &amp; bài tập</h2>', '<h3>Ví dụ &amp; bài tập</h3>'),
               ('<h2>综合练习 · Bài tập (có đáp án)</h2>', '<h2>综合练习 · Luyện tập tổng hợp</h2>')]
        for a, b in sub:
            assert r.count(a) == 1, a; r = r.replace(a, b)
        # 课文问题与注释补充 → hai h3 trong 走进课文
        h = '<h2>课文问题与注释补充</h2>'; i = r.index(h); j = r.index('<h2>', i + len(h))
        body = r[i + len(h):j]; k = body.index('<div class="card l1n">')
        a, b = body[:k], body[k:]
        assert bal(a) == 0 and bal(b) == 0, (bal(a), bal(b))
        r = r[:i] + H(3, '课文旁问题 · Câu hỏi bên lề') + a + H(3, '注释 · Chú thích') + b + r[j:]
    else:
        r = r.replace('<h1>第2课 ', '<h1>第2课　', 1)
        # 题解: thiếu nguồn
        h = '<h2>词语学习 · Từ vựng</h2>'; assert r.count(h) == 1
        r = r.replace(h, '<h2>题解 · Giới thiệu chủ đề</h2>' + BANNER + '<h2>词语学习 · Học từ vựng</h2>')
        sub = [('<h2>课文 · Bài khóa (kèm ghi chú của cô)</h2>', '<h2>走进课文 · Tìm hiểu bài đọc</h2>'),
               ('<h2>Ghi chú của cô (lời giảng trên lớp)</h2>', '<h3>Lời cô · Ghi chú của cô (lời giảng trên lớp)</h3>'),
               ('<h2>综合注释 · Chú thích ngữ pháp</h2>', '<h2>综合注释 · Chú giải tổng hợp</h2>'),
               ('<h2>综合练习 · Bài tập (có đáp án)</h2>', '<h2>综合练习 · Luyện tập tổng hợp</h2>')]
        for a, b in sub:
            assert r.count(a) == 1, a; r = r.replace(a, b)
    assert bal(r) == bal(sec) , (n, bal(r), bal(sec))
    return r

def fix_lesson(sec, n):
    parts = re.split(r'(<h[1-4][^>]*>.*?</h[1-4]>)', sec, flags=re.S)
    out = []; demote = False
    for p in parts:
        mm = re.fullmatch(r'<(h[1-4])([^>]*)>(.*?)</h[1-4]>', p, re.S)
        if not mm: out.append(p); continue
        tag, attr, inner = mm.groups(); lvl = int(tag[1]); txt = re.sub('<[^>]+>', '', inner)
        if lvl == 1: out.append(p); continue
        new = None
        if lvl == 2:
            demote = False
            if txt.strip() == 'Trang 100':
                out.append(''); continue          # chỉ chứa ghi chú nguồn, bỏ tiêu đề
            for rx, lab, nl in H2MAP:
                if re.match(rx, txt):
                    new = (nl, lab, split_page(txt)[1]); break
            if new is None:                        # 十 / 十一 … → h3 trong 综合练习
                clean, pg = split_page(txt); new = (3, clean, pg); demote = True
        elif lvl == 3 and demote:
            clean, pg = split_page(txt); new = (4, clean, pg)
        else:
            clean, pg = split_page(txt)
            if clean == txt.strip(): out.append(p); continue
            new = (lvl, clean, pg)
        nl, lab, pg = new
        out.append(f'<h{nl}{attr}>{lab}</h{nl}>' + (f'<p class="py pg">{pg}</p>' if pg else ''))
    r = ''.join(out)
    r, added = add_inputs(r, n); ADDED[n] = added
    seen = set()   # khoá trùng có sẵn (l5:k5, l6:k5): tách khoá của ô thứ hai trở đi
    def uniq(mm):
        k = mm.group(1)
        if k in seen:
            i = 2
            while '%s_%d' % (k, i) in seen: i += 1
            k = '%s_%d' % (k, i); DUP.append(k)
        seen.add(k); return 'data-k="%s"' % k
    r = re.sub(r'data-k="(ans:fz:[^"]+)"', uniq, r)
    if n == 8:  # thiếu nguồn: 题解, 走进课文 (D2)
        r = r.replace('<h2>词语学习 · Học từ vựng</h2>', '<h2>题解 · Giới thiệu chủ đề</h2>' + BANNER + '<h2>词语学习 · Học từ vựng</h2>', 1)
        r = r.replace('<h2>综合注释 · Chú giải tổng hợp</h2>', '<h2>走进课文 · Tìm hiểu bài đọc</h2>' + BANNER + '<h2>综合注释 · Chú giải tổng hợp</h2>', 1)
    return r

def sub(mm):
    n = int(mm.group(2))
    if n in (3, 4): return mm.group(1) + restructure(mm.group(3), n)
    if n in (1, 2):
        r, added = add_inputs(restructure12(mm.group(3), n), n); ADDED[n] = added
        return mm.group(1) + r
    return mm.group(1) + fix_lesson(mm.group(3), n) if 5 <= n <= 14 else mm.group(0)
doc = re.sub(r'(<section class="les[^"]*" id="l(\d+)">)(.*?)(?=</section>)', sub, doc, flags=re.S)

i0 = doc.index('{const t=$("#l1 .vt");tb(t,'); j0 = doc.index('tb($("#l2 .vt")'); j1 = doc.index('\n', j0)
doc = doc[:i0] + doc[j1:]   # bảng bài 1–2 đã ghi sẵn vào HTML
new = json.dumps(doc, ensure_ascii=False).replace('<', '\\u003c')
open(dst, 'w', encoding='utf8').write(s[:m.start(2)] + new + s[m.end(2):])

print('Ô nhập thêm:', {k: v for k, v in sorted(ADDED.items()) if v})
print('Khoá trùng đã tách:', DUP)
