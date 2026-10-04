#!/usr/bin/env python3
"""P7: sắp lại thứ tự mục trong 12 trang bài KB: 1, 2, 3, 4, …, 10, Phụ lục A, Phụ lục B.
Hiện tại cả 12 file cùng lệch: 1, 2, 3, Phụ lục B, 9, 10, 8, 4, 5, 6, 7, Phụ lục A. Chỉ đổi thứ tự khối, không đổi chữ.
Dùng: python3 tools/reorder_kb.py vào.html ra.html"""
import re, sys, json, collections
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf8').read()
m = re.search(r'(<script type="application/json" id="src-kb">)(.*?)(</script>)', s, re.S)
doc = json.loads(m.group(2).replace('\\u003c', '<'))
km = re.search(r'(<script id="kb" type="application/json">)(.*?)(</script>)', doc, re.S)
K = json.loads(km.group(2).replace('<\\/', '</'))

def rank(title):
    t = title.strip()
    mm = re.match(r'^(\d+)\.\s', t)
    if mm: return int(mm.group(1))
    if t.startswith('Phụ lục A'): return 101
    if t.startswith('Phụ lục B'): return 102
    return None

report = []
for n in range(1, 13):
    key = 'lessons/%02d.md' % n
    lines = K[key].split('\n'); fence = False
    heads = []
    for i, l in enumerate(lines):
        if l.startswith('```'): fence = not fence
        if not fence and l.startswith('## '): heads.append(i)
    pre = lines[:heads[0]]
    blocks = [lines[a:b] for a, b in zip(heads, heads[1:] + [len(lines)])]
    ranks = [rank(b[0][3:]) for b in blocks]
    assert all(r is not None for r in ranks), (n, [b[0][:30] for b, r in zip(blocks, ranks) if r is None])
    assert len(set(ranks)) == len(ranks), (n, ranks)
    order = sorted(range(len(blocks)), key=lambda i: ranks[i])
    before = collections.Counter(l for b in blocks for l in b)
    new = pre + [l for i in order for l in blocks[i]]
    assert collections.Counter(l for b in blocks for l in b) == before and len(new) == len(lines)
    K[key] = '\n'.join(new)
    report.append((n, ranks, [ranks[i] for i in order]))
newjson = json.dumps(K, ensure_ascii=False).replace('</', '<\\/')
doc = doc[:km.start(2)] + newjson + doc[km.end(2):]
enc = json.dumps(doc, ensure_ascii=False).replace('<', '\\u003c')
open(dst, 'w', encoding='utf8').write(s[:m.start(2)] + enc + s[m.end(2):])
print('trước:', report[0][1]); print('sau  :', report[0][2]); print('đã sắp lại', len(report), 'trang bài KB (dòng chữ giữ nguyên)')
