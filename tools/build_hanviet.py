#!/usr/bin/env python3
"""Dựng từ điển Hán-Việt (từ → âm Hán-Việt, chữ → âm) từ các bảng từ vựng đã có trong file v3:
fz (cột Hán-Việt), ky (cột hv của các bài có bảng), ld (HZC/HZW). Ghi tools/hanviet.json."""
import re, json, os, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(ROOT, 'Tong_hop_3_giao_trinh_D1_D2_KY_v3_Bai11_day_du.html'), encoding='utf8').read()
doc = lambda i: json.loads(re.search(r'id="src-%s">(.*?)</script>' % i, s, re.S).group(1).replace('\\u003c', '<'))
HAN = re.compile(r'[一-鿿]'); strip = lambda h: re.sub(r'\s+', ' ', re.sub('<[^>]+>', '', re.sub(r'<rt>[^<]*</rt>', '', h))).strip()
W = {}; src = collections.Counter()
# fz
fz = doc('fz')
for tb in re.findall(r'<table>.*?</table>', fz, re.S):
    rows = re.findall(r'<tr>(.*?)</tr>', tb, re.S)
    if not rows: continue
    heads = [strip(x) for x in re.findall(r'<th[^>]*>(.*?)</th>', rows[0], re.S)]
    hv = next((i for i, h in enumerate(heads) if h.replace(' ', '').lower() in ('hánviệt', 'hán-việt')), None)
    wi = next((i for i, h in enumerate(heads) if h in ('词语', '词')), None)
    if hv is None or wi is None: continue
    for r in rows[1:]:
        c = [strip(x) for x in re.findall(r'<td[^>]*>(.*?)</td>', r, re.S)]
        if len(c) > max(hv, wi) and HAN.search(c[wi]) and c[hv]: W.setdefault(re.sub(r'[^一-鿿]', '', c[wi]), c[hv].lower()); src['fz'] += 1
# ky
ky = doc('ky')
for m in re.finditer(r'<tr><td>\d+</td><td>(.*?)</td><td[^>]*>.*?</td><td class="hv">(.*?)</td>', ky, re.S):
    w = re.sub(r'[^一-鿿]', '', strip(m.group(1))); h = strip(m.group(2)).lower()
    if w and h: W.setdefault(w, h); src['ky'] += 1
# ld
ld = doc('ld')
def grab(name):
    i = ld.index('const %s=' % name) + len('const %s=' % name); depth = 0
    for j in range(i, len(ld)):
        if ld[j] == '{': depth += 1
        elif ld[j] == '}':
            depth -= 1
            if depth == 0: return json.loads(ld[i:j + 1])
HZC = grab('HZC'); HZW = grab('HZW')
for w, v in HZW.items():
    if len(v) > 2 and v[2]: W.setdefault(w, v[2].lower()); src['ld'] += 1
C = {k: v[0].split(' / ')[0].lower() for k, v in HZC.items()}
# chữ từ các từ có số âm tiết = số chữ
cnt = collections.defaultdict(collections.Counter)
for w, h in W.items():
    sy = h.split()
    if len(sy) == len(w) and all(HAN.match(c) for c in w):
        for c, y in zip(w, sy): cnt[c][y] += 1
for c, cc in cnt.items(): C.setdefault(c, cc.most_common(1)[0][0])
C.update(json.load(open(os.path.join(ROOT, 'tools', 'hanviet_bosung.json'), encoding='utf8')))   # chữ bổ sung tay
json.dump({'W': W, 'C': C}, open(os.path.join(ROOT, 'tools', 'hanviet.json'), 'w', encoding='utf8'), ensure_ascii=False)
print('từ:', len(W), 'chữ:', len(C), dict(src))
