"""In gọn các thẻ bài tập của fz bài N (để soạn đáp án).  python3 tools/fz_dump_cards.py N [html]"""
import re, sys, json, html as H
n = int(sys.argv[1]); p = ([a for a in sys.argv[2:] if not a.startswith('--')] or [None])[0] or 'Tong_hop_3_giao_trinh_D1_D2_KY_v4.html'
h = open(p, encoding='utf-8').read()
f = json.loads(re.search(r'<script type="application/json" id="src-fz">(.*?)</script>', h, re.S).group(1))
i = f.find('id="l%d"' % n); j = f.find('<section class="les', i + 10); s = f[i:j]
cards = re.findall(r'<div class="card ex.*?(?=<div class="card ex|\Z)', s, re.S)
NA = '--na' in sys.argv
for k, c in enumerate(cards):
    if NA and 'Chưa có đáp án' not in c: continue
    m = re.search(r'<h3[^>]*>(.*?)</h3>', c, re.S); t = re.sub(r'<[^>]+>', '', m.group(1)) if m else '(no h3)'
    body = re.sub(r'<div class="(?:uin|ans|wr)[ "].*', '', c, flags=re.S)
    body = re.sub(r'<div class="ln lv[^"]*">.*?</div>', '', body, flags=re.S)       # bỏ dòng Việt
    body = re.sub(r'<div class="trs">.*?</div>', '', body, flags=re.S)
    body = re.sub(r'<input[^>]*data-a="([^"]*)"[^>]*>', lambda m: '〔%s〕' % m.group(1), body)
    body = re.sub(r'<input[^>]*>', '＿＿', body)
    body = re.sub(r'<li>', '\n ● ', body); body = re.sub(r'<br\s*/?>|</div>|</tr>', '\n', body)
    body = H.unescape(re.sub(r'<[^>]+>', '', body)); body = re.sub(r'\n\s*\n+', '\n', body).strip()
    body = body.replace('📑', '')
    print('### [%d] %s  (ans: %s)\n%s\n' % (k, t[:60], 'sẵn' if 'Chưa có đáp án' not in c else 'THIẾU', body[:(9000 if "--full" in sys.argv else 2400)]))
