#!/usr/bin/env python3
"""P6: chỉnh nhỏ ld — không đổi dữ liệu LES.
Dùng: python3 tools/sync_ld.py vào.html ra.html"""
import re, sys, json
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf8').read()
m = re.search(r'(<script type="application/json" id="src-ld">)(.*?)(</script>)', s, re.S)
d = json.loads(m.group(2).replace('\\u003c', '<'))
log = []
def sub(a, b, count=1):
    global d
    n = d.count(a); assert n >= 1, a
    if count and n != count: raise AssertionError((a, n))
    d = d.replace(a, b); log.append((a[:50], n))

# 1. Nhãn đọc quét bài 1 giống 11 bài còn lại
sub('Tín hiệu &amp; Bẫy cần chú ý', 'Tín hiệu / Bẫy cần chú ý')

# 2. Ẩn dòng/mục fid–pid khi trống
sub("const row=(a,b)=>`<div class=\"lk\"><b>${a}</b>${b}</div>`;",
    "const row=(a,b)=>`<div class=\"lk\"><b>${a}</b>${b}</div>`,rowx=(a,b)=>b==='—'?'':row(a,b);")
sub("${row('Formal ↔ Spoken',fs.map(", "${rowx('Formal ↔ Spoken',fs.map(")
sub("${row('Pattern',ps.map(", "${rowx('Pattern',ps.map(")
sub("[(L.fid||[]).length+(L.pid||[]).length,'formal + pattern']].map(x=>",
    "[(L.fid||[]).length+(L.pid||[]).length,'formal + pattern']].filter(x=>x[1]!=='formal + pattern'||x[0]).map(x=>")
sub('<div class="sec"><h4>（二）常用书面词语 · Formal ↔ Spoken · ${fs.length}</h4>',
    '${fs.length?`<div class="sec"><h4>（二）常用书面词语 · Formal ↔ Spoken · ${fs.length}</h4>')
sub("<i>›</i></button>`).join('')}</div></div><h3 class=\"h3\">（三）常用格式 · Pattern · ${ps.length}</h3>${ps.map(x=>patCard(x,PAT.indexOf(x))).join('')}`",
    "<i>›</i></button>`).join('')}</div></div>`:''}${ps.length?`<h3 class=\"h3\">（三）常用格式 · Pattern · ${ps.length}</h3>${ps.map(x=>patCard(x,PAT.indexOf(x))).join('')}`:''}`")

# 3. Tên trang ngân hàng: Việt là tên, Anh/Hán trong ngoặc; số thứ tự khớp mục lục
V = [('v-for', '03 Formal ↔ Spoken · 常用书面词语', '02 Từ văn viết (Formal ↔ Spoken) · 常用书面词语'),
     ('v-pat', '04 Pattern Bank · 常用格式', '03 Khung câu (Pattern Bank) · 常用格式'),
     ('v-chk', '06 Chunk Bank', '04 Kho cụm từ (Chunk Bank) · 固定搭配'),
     ('v-par', '05 Parsing Lab', '05 Bẻ câu dài (Parsing Lab) · 长句分析'),
     ('v-scn', '07 Scanning Notes · 实况阅读', '06 Đọc quét (Scanning Notes) · 实况阅读'),
     ('v-map', '08 Map 24 技巧', '07 Bản đồ kỹ năng (Map 24) · 技巧地图'),
     ('v-gap', '09 GAP checklist', '08 Khoảng trống (GAP) · 查漏补缺')]
for vid, a, b in V:
    sub('<section class="view" id="%s"><div class="wrap"><div class="vh"><div class="kick">%s</div>' % (vid, a),
        '<section class="view" id="%s"><div class="wrap"><div class="vh"><div class="kick">%s</div>' % (vid, b))
sub('<h1>Chunk <em>Bank</em></h1>', '<h1>Kho <em>cụm từ</em></h1>')
sub('<h1>Parsing <em>Lab</em></h1>', '<h1>Bẻ <em>câu dài</em></h1>')
sub('<h1>7 dạng <em>实况</em></h1>', '<h1>7 dạng <em>đọc quét</em></h1>')
sub('<h1>Hub <em>12 bài</em></h1>', '<h1>Tổng quan <em>12 bài</em></h1>')
sub('<div class="kick">12 Bài · 乐读 5</div>', '<div class="kick">十二课总览 · 乐读 5</div>')

new = json.dumps(d, ensure_ascii=False).replace('<', '\\u003c')
s = s[:m.start(2)] + new + s[m.end(2):]

# 4. Mục lục ở shell
tm = re.search(r'(<script type="application/json" id="toc-data">)(.*?)(</script>)', s, re.S)
toc = tm.group(2)
for a, b in [('Morpheme Bank · 24 ngữ tố', 'Kho ngữ tố (Morpheme Bank) · 24 ngữ tố'),
             ('Từ văn viết ↔ khẩu ngữ', 'Từ văn viết (Formal ↔ Spoken)'),
             ('Pattern Bank · khung câu văn viết', 'Khung câu (Pattern Bank) · văn viết'),
             ('Chunk Bank · cụm cố định', 'Kho cụm từ (Chunk Bank) · cụm cố định'),
             ('Parsing Lab · bẻ câu dài', 'Bẻ câu dài (Parsing Lab)'),
             ('Scanning Notes · 7 dạng đọc quét', 'Đọc quét (Scanning Notes) · 7 dạng'),
             ('Map 24 · 24 kỹ năng × 12 bài', 'Bản đồ kỹ năng (Map 24) · 24 kỹ năng × 12 bài'),
             ('GAP · danh sách khoảng trống', 'Khoảng trống (GAP) · danh sách')]:
    assert toc.count(a) == 1, a; toc = toc.replace(a, b)
s = s[:tm.start(2)] + toc + s[tm.end(2):]
open(dst, 'w', encoding='utf8').write(s)
print('ld: %d thay thế' % len(log))
