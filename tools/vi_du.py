#!/usr/bin/env python3
"""Kho câu ví dụ cho bảng từ vựng ky: ưu tiên (1) trong chính bài, (2) các bài khác của ky,
(3) giáo trình khác (fz, ld), (4) tự soạn (tools/vi_du_tu_soan.json).
Mỗi ví dụ có đủ Hán, pinyin, Việt."""
import re, os, sys, json, html, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_ky as G
from pypinyin import pinyin, Style

HAN = G.HAN
ROOT = G.ROOT

def plain(x):
    x = re.sub(r'<rt>[^<]*</rt>', '', x); x = re.sub(r'<[^>]+>', '', x)
    x = html.unescape(x); x = re.sub(r'[*_`]', '', x)
    return re.sub(r'\s+', ' ', x).strip()

def py_text(zh, hint=None, override=None):
    """Chuỗi pinyin tách âm tiết cho một câu Hán (dùng hint từ md nếu số âm tiết khớp, có biến điệu 不/一)."""
    if override: return override
    han = HAN.findall(zh)
    if hint and len(hint) == len(han): sy = list(hint)
    else:
        sy = G.sandhi(han, [p[0] for p in pinyin(''.join(han), style=Style.TONE)]) if han else []
    it = iter(sy); out = []; pre = ''
    for ch in zh:
        if HAN.match(ch): out.append(pre + next(it, '')); pre = ''
        elif ch in '“‘（(《「『': pre += ch
        elif ch.isspace(): continue
        elif ch.isalnum():
            if out and out[-1].startswith('\x00'): out[-1] += ch
            else: out.append('\x00' + ch)
        elif out: out[-1] += ch
    return ' '.join(x.replace('\x00', '') for x in out if x)

CORPUS = {'ky': [], 'fz': [], 'ld': []}   # mỗi phần tử: (bài, zh, py, vi)

def add_ky():
    for n in range(1, 13):
        text = open(os.path.join(G.CHUAN, 'Bai%02d.md' % n), encoding='utf8').read()
        secs = G.parse_sections(text)
        for s in secs:
            if s['t'] in ('Tiêu đề bài', 'Bảng tên nhân vật') or s['t'].startswith('📝'): continue
            blocks = G.split_blocks('\n'.join(s['body']))
            i = 0
            while i < len(blocks):
                typ, src = blocks[i]
                nxt_vi = i + 1 < len(blocks) and blocks[i + 1][0] == 'paragraph' and G.is_vi_para(blocks[i + 1][1])
                if typ == 'paragraph' and G.is_zh_para(src) and (nxt_vi or G.zh_para(src)[2]):
                    han, py, vi_in = G.zh_para(src); vi = list(vi_in)
                    if not vi_in and nxt_vi:
                        for l in blocks[i + 1][1].split('\n'):
                            l2 = G.LAB_VI.sub('', l.strip().rstrip('\\').rstrip())
                            if l2.strip(): vi.append(l2)
                    if len(vi) > 1 and re.match(r'^\*\*[^*]{1,40}[:：]\*\*$', vi[0].strip()): vi = [vi[0].strip() + ' ' + vi[1].strip()] + vi[2:]
                    if han:
                        ms = re.match(r'^\*\*(.+?)[：:]\*\*\s*(.*)$', han[0].strip())
                        if ms: han = ([ms.group(2)] if ms.group(2).strip() else []) + han[1:]
                    hint = G.hint_syllables(' '.join(py), ' '.join(han)) if py else None
                    if hint is not None and len(hint) != len(HAN.findall(' '.join(han))): hint = None
                    pairs = G.pair_up(han, vi) if vi else None
                    if pairs:
                        pos = 0
                        for hz, vz in pairs:
                            n_h = len(HAN.findall(hz)); sl = hint[pos:pos + n_h] if hint is not None else None; pos += n_h
                            z = plain(hz); v = plain(vz)
                            v = re.sub(r'^[A-ZÀ-Ỹa-zà-ỹ ]{1,30}:\s+(?=[A-ZÀ-Ỹ])', '', v)   # bỏ nhãn người nói
                            z = re.sub(r'^[一-鿿]{1,6}[：:]\s*', '', z)
                            if HAN.search(z) and v: CORPUS['ky'].append((n, z, py_text(z, sl), v))
                    i += 2 if (nxt_vi and not vi_in) else 1; continue
                if typ == 'table':
                    rows = [G.split_row(l) for l in src.split('\n')]
                    rows = [r for r in rows if r]
                    if rows and any('中文' in c for c in rows[0]) and any('Tiếng Việt' in c for c in rows[0]):
                        zi = next(k for k, c in enumerate(rows[0]) if '中文' in c); vi_i = next(k for k, c in enumerate(rows[0]) if 'Tiếng Việt' in c)
                        for r in rows[2:]:
                            if len(r) <= max(zi, vi_i): continue
                            zc = re.split(r'<br\s*/?>', r[zi])[0]; vc = re.split(r'<br\s*/?>', r[vi_i])[0]
                            z = plain(zc); v = plain(vc); z = re.sub(r'^\d+[\.．]\s*', '', z); v = re.sub(r'^\d+[\.．]\s*', '', v)
                            if HAN.search(z) and v and not HAN.search(v):
                                for hz, vz in (G.pair_up([z], [v]) or [(z, v)]):
                                    if HAN.search(hz) and vz: CORPUS['ky'].append((n, hz, py_text(hz), vz))
                i += 1

def add_other():
    s = open(os.path.join(ROOT, 'Tong_hop_3_giao_trinh_D1_D2_KY_v4.html'), encoding='utf8').read()
    doc = lambda i: json.loads(re.search(r'id="src-%s">(.*?)</script>' % i, s, re.S).group(1).replace('\\u003c', '<'))
    fz = doc('fz')
    for m in re.finditer(r'<section class="les[^"]*" id="l(\d+)">(.*?)(?=<section class="les|\Z)', fz, re.S):
        n = int(m.group(1)); sec = re.sub(r'<table.*?</table>', '', m.group(2), flags=re.S)
        units = re.findall(r'<div class="ln([^"]*)">(.*?)</div>(?=<)', sec, re.S)
        for k, (c, h) in enumerate(units):
            if 'lz' in c and HAN.search(plain(h)):
                z = plain(h)
                v = next((plain(x[1]) for x in units[k + 1:k + 3] if 'lv' in x[0]), '')
                if v and not HAN.search(v) and 8 <= len(HAN.findall(z)) <= 90:
                    pairs = G.pair_up([z], [v]) or [(z, v)]
                    for hz, vz in pairs:
                        if HAN.search(hz) and vz: CORPUS['fz'].append((n, hz, py_text(hz), vz))
    ld = doc('ld')
    for m in re.finditer(r'"h":"((?:[^"\\]|\\.)*)","p":"(?:[^"\\]|\\.)*","v":"((?:[^"\\]|\\.)*)"', ld):
        try: z = plain(json.loads('"%s"' % m.group(1))); v = plain(json.loads('"%s"' % m.group(2)))
        except Exception: continue
        if not HAN.search(z) or '（Vault' in z or 'biên soạn' in z: continue
        pairs = G.pair_up([z], [v]) or [(z, v)]
        for hz, vz in pairs:
            if HAN.search(hz) and vz: CORPUS['ld'].append((0, hz, py_text(hz), vz))

SELF = {}
_sp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vi_du_tu_soan.json')
if os.path.exists(_sp): SELF = json.load(open(_sp, encoding='utf8'))

def score(z, w):
    n = len(HAN.findall(z))
    if n < 6 or n > 45: return None
    if re.search(r'[＿_]{2,}|\.{3}|…|\?\?', z): return None
    if not re.search(r'[。！？][”’」）)]?$', z): return None               # phải là câu hoàn chỉnh
    if len(re.findall(r'(?<=[\u4e00-\u9fff]) (?=[\u4e00-\u9fff])', z)) >= 2: return None   # dòng liệt kê từ, không phải câu
    s = abs(n - 18)
    if '：' in z or ':' in z: s += 3
    if re.match(r'^\d+[\.．]', z): s += 2
    if z.count(w) > 1: s += 2
    if re.search(r'[A-Za-z]{3,}', z): s += 6
    return s

def find_example(word, lesson, used=None):
    ws = [x for x in re.split(r'[/／、]', re.sub(r'[（(][^）)]*[）)]', '', word)) if HAN.search(x)]
    cands = [re.sub(r'[^一-鿿]', '', x) for x in ws]
    cands = [c for c in cands if c]
    if not cands: return None
    def pick(src, pred, avoid=True):
        best = None
        for (n, z, py, vi) in CORPUS[src]:
            if not pred(n): continue
            for c in cands:
                if c in z.replace(' ', ''):
                    sc = score(z, c)
                    if sc is None: continue
                    if avoid and used is not None and z in used: sc += 50      # tránh trùng câu ví dụ trong cùng bảng
                    if best is None or sc < best[0]: best = (sc, c, z, py, vi, n)
        return best
    for label, src, pred in (('ky-same', 'ky', lambda n: n == lesson), ('ky-other', 'ky', lambda n: n != lesson), ('fz', 'fz', lambda n: True), ('ld', 'ld', lambda n: True)):
        b = pick(src, pred)
        if b:
            if used is not None: used.add(b[2])
            return label, b[1], b[2], b[3], b[4], b[5]
    for c in [word.strip()] + cands:
        if c in SELF:
            z, vi, *ov = SELF[c]
            return 'self', c, z, py_text(z, override=(ov[0] if ov else None)), vi, 0
    return None

def example_cell(word, lesson, used=None):
    r = find_example(word, lesson, used)
    if not r: return '', None
    label, c, z, py, vi, n = r
    z = re.sub(r'^\d+[\.．]\s*', '', z); vi = re.sub(r'^\d+[\.．]\s*', '', vi)
    if label != 'self': py = py_text(z)
    zh = html.escape(z).replace(c, '<mark>%s</mark>' % c, 1)
    tag = {'ky-same': 'trong bài', 'ky-other': 'ky bài %d' % n, 'fz': '发展汉语 bài %d' % n, 'ld': '乐读 5', 'self': 'tự soạn'}[label]
    cell = ('<span class="ex-zh" data-nopy>%s</span><br><span class="ex-py">%s</span><br><span class="ex-vi">%s</span>'
            '<br><span class="ex-src">%s</span>') % (zh, html.escape(py), html.escape(vi), tag)
    return cell, label

def init():
    if not CORPUS['ky']: add_ky(); add_other()

if __name__ == '__main__':
    init(); print({k: len(v) for k, v in CORPUS.items()})
    from collections import Counter
    tot = Counter(); miss = {}
    for n in range(1, 13):
        text = open(os.path.join(G.CHUAN, 'Bai%02d.md' % n), encoding='utf8').read()
        for line in text.split('\n'):
            m = re.match(r'^\|\s*\d+\s*\|\s*([^|]+?)\s*\|', line)
            if not m: continue
            w = re.sub(r'🔊|\*\*', '', m.group(1)).strip()
            r = find_example(w, n); tot[r[0] if r else 'none'] += 1
            if not r: miss.setdefault(n, []).append(w)
    print(dict(tot)); 
    for n, ws in miss.items(): print(n, len(ws), ws)
