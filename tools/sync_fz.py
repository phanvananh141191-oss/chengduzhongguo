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
    return mm.group(1) + fix_lesson(mm.group(3), n) if 5 <= n <= 14 else mm.group(0)
doc = re.sub(r'(<section class="les[^"]*" id="l(\d+)">)(.*?)(?=</section>)', sub, doc, flags=re.S)

new = json.dumps(doc, ensure_ascii=False).replace('<', '\\u003c')
open(dst, 'w', encoding='utf8').write(s[:m.start(2)] + new + s[m.end(2):])

print('Ô nhập thêm:', {k: v for k, v in sorted(ADDED.items()) if v})
print('Khoá trùng đã tách:', DUP)
