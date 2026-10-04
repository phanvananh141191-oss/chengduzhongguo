"""Liệt kê các ô trống (input) của thẻ N trong bài L cùng ngữ cảnh và data-a hiện có.  python3 tools/fz_dump_inputs.py L N"""
import re, sys, json, html as H
n, k = int(sys.argv[1]), int(sys.argv[2])
h = open('Tong_hop_3_giao_trinh_D1_D2_KY_v4.html', encoding='utf-8').read()
f = json.loads(re.search(r'<script type="application/json" id="src-fz">(.*?)</script>', h, re.S).group(1))
i = f.find('id="l%d"' % n); j = f.find('<section class="les', i + 10); s = f[i:j]
cards = re.findall(r'<div class="card ex.*?(?=<div class="card ex|\Z)', s, re.S); c = cards[k]
pos = 0
for t, m in enumerate(re.finditer(r'<input[^>]*>', c)):
    pre = H.unescape(re.sub(r'<[^>]+>', '', c[max(0, m.start() - 160):m.start()]))[-22:].replace('\n', ' ')
    post = H.unescape(re.sub(r'<[^>]+>', '', c[m.end():m.end() + 80]))[:14].replace('\n', ' ')
    a = re.search(r'data-a="([^"]*)"', m.group(0))
    print('%2d  …%s ▢ %s…   [%s]' % (t, pre, post, a.group(1) if a else '-'))
