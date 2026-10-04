#!/usr/bin/env python3
"""Đo chỗ thiếu dịch/thiếu Hán trong HTML. Dùng: python3 tools/audit_gaps.py [file.html]"""
import re, sys, json
f = sys.argv[1] if len(sys.argv) > 1 else 'Tong_hop_3_giao_trinh_D1_D2_KY_v4.html'
s = open(f, encoding='utf8').read()
doc = lambda i: json.loads(re.search(r'id="src-%s">(.*?)</script>' % i, s, re.S).group(1).replace('\\u003c', '<'))
CJK = re.compile(r'[一-鿿]'); VIET = re.compile(r'[àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ]', re.I)
def txt(h): return re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', h)).strip()
def lessons(h):
    for m in re.finditer(r'<section class="les[^"]*" id="(l\d+)">(.*?)(?=<section class="les|\Z)', h, re.S): yield m.group(1), m.group(2)
fz = doc('fz'); out = {}
for lid, sec in lessons(fz):
    # đơn vị = các khối .ln (div); gộp thành chuỗi, bỏ bảng
    sec2 = re.sub(r'<table.*?</table>', '', sec, flags=re.S)
    units = re.findall(r'<div class="ln([^"]*)">(.*?)</div>(?=<)', sec2, re.S)
    han_only = []; vi_only = []
    for i, (c, h) in enumerate(units):
        t = txt(h)
        has_c = len(CJK.findall(t)); has_v = bool(VIET.search(t))
        win = ' '.join(txt(x[1]) for x in units[i + 1:i + 4])
        if 'lz' in c and has_c >= 6 and not has_v and not VIET.search(win.split('Hán')[0] if False else win[:400]):
            han_only.append(t[:60])
        if 'lv' in c and has_v and not has_c:
            prev = ' '.join(txt(x[1]) for x in units[max(0, i - 3):i])
            if not CJK.search(prev): vi_only.append(t[:60])
    out[lid] = (len(han_only), len(vi_only), han_only[:3], vi_only[:3])
for k, v in out.items(): print('fz', k, 'Hán không Việt:', v[0], '| Việt không Hán:', v[1], v[2][:2], v[3][:2])
ld = doc('ld'); print('ld: placeholder thiếu Hán:', ld.count('Vault chưa có nguyên văn Hán ngữ'))
