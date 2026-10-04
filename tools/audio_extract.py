"""Trích từ vựng + bài khoá (chỉ chữ Hán) của fz/ky/ld từ v4.html → assets/audio/manifest.json.
Dùng: python3 tools/audio_extract.py [html]   (chỉ đọc, không gọi API)"""
import re, sys, json, os, html, hashlib
HTML = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'Tong_hop_3_giao_trinh_D1_D2_KY_v4.html')
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'audio', 'manifest.json')
SUP = '¹²³⁴⁵⁶⁷⁸⁹⁰①②③④⑤⑥⑦⑧⑨⑩'

def clean(s):
    s = re.sub(r'<a [^>]*class="[^"]*\bkb[mg]\b[^"]*"[^>]*>.*?</a>', '', s, flags=re.S)      # bỏ ký hiệu ghi chú 📝 và mã họ ngữ pháp (A1, E3…)
    s = re.sub(r'<a [^>]*class="[^"]*\bxl\b[^"]*"[^>]*>.*?</a>', '', s, flags=re.S)
    s = re.sub(r'<rt[^>]*>.*?</rt>', '', s, flags=re.S)
    s = re.sub(r'<sup[^>]*>.*?</sup>', '', s, flags=re.S)
    s = html.unescape(re.sub(r'<[^>]+>', '', s))
    s = re.sub('[' + SUP + ']', '', s)
    s = re.sub(r'[（(][^）)]*[A-Za-z][^）)]*[）)]', '', s)          # chú giải latin trong ngoặc
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'(?<=[一-鿿，。！？、；：”“]) (?=[一-鿿，。！？、；：”“])', '', s)
    return s
def hz(s): return len(re.findall(r'[一-鿿]', s))

def src(h, b):
    return json.loads(re.search(r'<script type="application/json" id="src-%s">(.*?)</script>' % b, h, re.S).group(1))

def fz(h):
    t = src(h, 'fz'); out = []
    for m in re.finditer(r'<section class="les[^"]*" id="l(\d+)"(.*?)(?=<section class="les|\Z)', t, re.S):
        n = int(m.group(1)); s = m.group(2)
        for r in re.finditer(r'<tr id="l\d+-w-([^"]*)"', s):
            w = clean(r.group(1))
            if hz(w): out.append((n, 'w', w))
        a = s.find('走进课文')
        if a < 0: continue
        body = s[a:]
        e = re.search(r'<h2[ >]', body[10:]); body = body[: 10 + e.start()] if e else body
        e = re.search(r'<h3[^>]*>[^<]*(?:注释|课文旁问题|Đáp án|Chú thích)', body)
        if e: body = body[:e.start()]
        for p in re.findall(r'<div class="ln lz">(.*?)</div>|<p>(.*?)</p>|<div class="zu">(.*?)</div>', body, re.S):
            p = clean(p[0] or p[1] or p[2])
            if hz(p) > 4: out.append((n, 't', p))
    return out

def ky(h):
    t = src(h, 'ky'); out = []
    for m in re.finditer(r'<section data-t="[^"]*" id="s(\d+)">(.*?)(?=<section data-t=|\Z)', t, re.S):
        n = int(m.group(1)); s = m.group(2)
        if n < 1 or n > 12: continue
        seen = set()
        for tb in re.findall(r'<table>.*?</table>', s, re.S):
            hd = re.search(r'<tr>(.*?)</tr>', tb, re.S)
            if not hd or '词' not in clean(hd.group(1)) or '拼' not in clean(hd.group(1)): continue
            for tr in re.findall(r'<tr>(.*?)</tr>', tb, re.S)[1:]:
                tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)
                if len(tds) > 1:
                    w = clean(tds[1])
                    if hz(w) and w not in seen: seen.add(w); out.append((n, 'w', w))
        seen = set(); starts = [x.start() for x in re.finditer(r'<div class="u3"', s)]
        import bisect
        for zm in re.finditer(r'<div class="zh">(.*?)</div>', s, re.S):
            z = clean(zm.group(1))
            if hz(z) > 2 and z not in seen: seen.add(z); out.append((n, 't', z, bisect.bisect_right(starts, zm.start())))
    return out

def ld(h):
    t = src(h, 'ld'); i = t.find('const LES=') + len('const LES=')
    L, _ = json.JSONDecoder().raw_decode(t[i:]); out = []
    for l in L:
        n = l['n']
        for w in l['V']:
            w = clean(w)
            if hz(w): out.append((n, 'w', w))
        for r in l['reads']:
            for p in r['p']:
                for x in (p.get('sn') or [{'h': p['h']}]):
                    x = clean(x['h'])
                    if hz(x) > 2: out.append((n, 't', x))
    return out

LONG = 8                      # câu bài khoá chỉ gọi là «trùng» khi dài hơn 8 chữ Hán
WORD_VOICES = ['nam1', 'nu1', 'nam2']   # từ vựng: xoay vòng các giọng
TEXT_VOICES = ['nu1', 'nam1', 'nam2']  # bài khoá: một giọng cho mỗi bài (hoặc nhóm bài chung câu dài)

def assign_voices(items):
    sys.path.insert(0, os.path.dirname(__file__))
    import audio_voices
    for i in items:
        if i['kind'] == 'w': i['voice'] = WORD_VOICES[int(i['hash'], 16) % len(WORD_VOICES)]
    audio_voices.assign(items)          # bài khoá: nam + nữ trong mỗi bài, hội thoại ghép theo nhân vật
    return []

def main():
    h = open(HTML, encoding='utf-8').read(); items = []; stat = {}
    for b, f in (('fz', fz), ('ky', ky), ('ld', ld)):
        cnt = {}
        for row in f(h):
            n, k, txt = row[:3]; blk = row[3] if len(row) > 3 else 0
            key = (b, n, k); cnt[key] = cnt.get(key, 0) + 1
            items.append({'id': '%s/l%02d/%s%03d' % (b, n, k, cnt[key]), 'book': b, 'lesson': n, 'kind': k, 'text': txt,
                          'hash': hashlib.sha1(txt.encode()).hexdigest()[:10], 'blk': blk})
            it = items[-1]
            if k == 'w': it['file'] = 'words/' + it['hash']                       # từ trùng → dùng chung một file mp3
            elif hz(txt) > LONG: it['file'] = 'sents/' + it['hash']               # câu dài (>8 chữ Hán) trùng → dùng chung
            else: it['file'] = it['id']                                           # câu ngắn: không coi là trùng
        stat[b] = (sum(1 for i in items if i['book'] == b and i['kind'] == 'w'), sum(1 for i in items if i['book'] == b and i['kind'] == 't'),
                   sum(len(i['text']) for i in items if i['book'] == b))
    groups = assign_voices(items)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(items, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    for b, (w, t, c) in stat.items(): print('%s: %d từ · %d đoạn bài khoá · %d ký tự' % (b, w, t, c))
    uniq = {}
    for i in items: uniq.setdefault(i['file'], i)
    for kind, nm in (('w', 'từ vựng'), ('t', 'câu bài khoá')):
        a = [i for i in items if i['kind'] == kind]; u = [i for i in uniq.values() if i['kind'] == kind]
        print('%s: %d mục → %d file duy nhất (bỏ %d trùng) · %d → %d ký tự' % (nm, len(a), len(u), len(a) - len(u), sum(len(i['text']) for i in a), sum(len(i['text']) for i in u)))
    w = {}
    for i in items:
        if i['kind'] == 'w': w.setdefault(i['text'], set()).add(i['book'])
    print('từ có ở ≥2 giáo trình: %d (3 giáo trình: %d)' % (sum(len(v) > 1 for v in w.values()), sum(len(v) == 3 for v in w.values())))
    import collections
    print('giọng bài khoá:', dict(collections.Counter(i['voice'] for i in uniq.values() if i['kind'] == 't')), '· giọng từ vựng:', dict(collections.Counter(i['voice'] for i in uniq.values() if i['kind'] == 'w')))
    print('Tổng duy nhất: %d file · %d ký tự' % (len(uniq), sum(len(i['text']) for i in uniq.values())))
    print('Tổng: %d file · %d ký tự' % (len(items), sum(len(i['text']) for i in items)))
main()
