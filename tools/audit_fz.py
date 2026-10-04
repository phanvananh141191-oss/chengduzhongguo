#!/usr/bin/env python3
"""Báo cáo «trước/sau» cho nguồn fz (S1, S2, S3, S5, S10 trong kế hoạch).
Dùng: python3 tools/audit_fz.py [file.html] > reports/fz_truoc.md"""
import re, sys, json, hashlib
from html.parser import HTMLParser

SRC = sys.argv[1] if len(sys.argv) > 1 else 'Tong_hop_3_giao_trinh_D1_D2_KY.html'
s = open(SRC, encoding='utf8').read()
m = re.search(r'<script type="application/json" id="src-fz">(.*?)</script>', s, re.S)
doc = json.loads(m.group(1).replace('\\u003c', '<'))

CANON = {2: ['题解 · Giới thiệu chủ đề', '词语学习 · Học từ vựng', '走进课文 · Tìm hiểu bài đọc',
             '综合注释 · Chú giải tổng hợp', '综合练习 · Luyện tập tổng hợp', '附录 · Phụ lục']}
PAGE = re.compile(r'P\d+|tr\.\s*\d+|Trang\s*\d+')

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack = []; self.les = None; self.out = {}; self.cur = None; self.buf = ''; self.pg = False
    def lesson(self, k):
        return self.out.setdefault(k, dict(h=[], ans=0, uans=0, text=[], body=[]))
    def handle_starttag(self, t, a):
        a = dict(a); cls = a.get('class', '')
        if t == 'section' and 'les' in cls.split() and a.get('id'):
            self.les = a['id']; self.lesson(self.les)
        if self.les:
            L = self.lesson(self.les)
            if t in ('h1', 'h2', 'h3', 'h4'): self.cur = t; self.buf = ''
            self.pg = (t == 'p' and 'pg' in cls.split()) or (t == 'div' and 'note' in cls.split() and False)
            if t == 'div' and 'ans' in cls.split(): L['ans'] += 1
            if t == 'textarea' and 'uans' in cls.split(): L['uans'] += 1
    def handle_endtag(self, t):
        if t == 'p': self.pg = False
        if self.les and self.cur == t:
            self.lesson(self.les)['h'].append((t, self.buf.strip())); self.cur = None
    def handle_data(self, d):
        if self.les:
            self.lesson(self.les)['text'].append(d)
            if not self.cur and not self.pg: self.lesson(self.les)['body'].append(d)
            if self.cur: self.buf += d

p = P(); p.feed(doc)
print('# Báo cáo đo fz (script tools/audit_fz.py)\n')
print('| Bài | h2 | h3 | .ans | .uans | S5 | Heading có số trang (S10) | Hash toàn bài | Hash thân (không heading) |\n|---|---|---|---|---|---|---|---|---|')
tot10 = 0; labels = {}
for k, L in p.out.items():
    h2 = [x for t, x in L['h'] if t == 'h2']; h3 = [x for t, x in L['h'] if t == 'h3']
    pg = [x for t, x in L['h'] if PAGE.search(x)]; tot10 += len(pg)
    txt = re.sub(r'\s+', '', ''.join(L['text']))
    hz = hashlib.sha1(txt.encode()).hexdigest()[:10]
    bh = hashlib.sha1(re.sub(r'\s+','',''.join(L['body'])).encode()).hexdigest()[:10]
    for x in h2: labels.setdefault(x, []).append(k)
    print(f"| {k} | {len(h2)} | {len(h3)} | {L['ans']} | {L['uans']} | {'khớp' if L['ans']==L['uans'] else 'lệch %d'%abs(L['ans']-L['uans'])} | {len(pg)} | {hz} | {bh} |")
print(f'\nS10 tổng heading có số trang: **{tot10}**\n')
print('## S3 — nhãn h2 ngoài bảng chuẩn\n')
for x, ks in labels.items():
    if x not in CANON[2]: print(f'- `{x}` — {", ".join(ks)}')
print('\n## S2 — thứ tự h2 từng bài\n')
for k, L in p.out.items():
    print(f"- {k}: " + ' → '.join(x for t, x in L['h'] if t == 'h2'))
