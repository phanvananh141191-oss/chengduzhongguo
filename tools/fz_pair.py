"""fz bài 1, 2: các khối dịch gộp (`.tr`) → từng câu Việt nằm ngay dưới câu Hán tương ứng (`.zu` + `.trs`).
Ngoài ra: khối «🇻🇳 …» gộp (`.lvb`) ở bài 5–8: bỏ khi trùng bản dịch từng mục đã có, hoặc đặt ngay dưới dòng đề.
Dùng: python3 tools/fz_pair.py <html>   (sửa tại chỗ)"""
import re, sys, json, math, os
sys.path.insert(0, os.path.dirname(__file__))

HAN = re.compile(r'[一-鿿]')
TERM = '。！？'
CLOSE = '”’）)」』"\''

def _lh(x): return len(HAN.findall(x)) + .3 * len(re.findall(r'\d+', x))
def _lv(x): return len(re.findall(r'\w+', x))
def _anch(x):
    return {t.lower().replace(',', '').replace('.', '') for t in re.findall(r'\d[\d.,]*|[A-Za-zÀ-ž]{4,}', x)}
def plain(h): return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', h)).strip()
def lead(x):
    m = re.match(r'\s*(\(\d{1,2}\)|（\d{1,2}）|\d{1,2}(?=[\s\.、．]))', x)
    return re.sub(r'[（）]', lambda c: '(' if c.group(0) == '（' else ')', m.group(1)) if m else None

# ---------------------------------------------------------------- tách câu Hán (HTML)
def han_segments(html):
    """-> list[str] HTML; cắt sau 。！？, tại <br/>, <li>, và trước (n) khi n tăng dần."""
    toks = re.split(r'(<[^>]+>)', html); segs = []; buf = ''; last = 0; carry = ''
    def flush():
        nonlocal buf, carry
        if plain(buf): segs.append((carry + buf).strip()); carry = ''
        else: carry += re.sub(r'</?br\s*/?>', '', buf)
        buf = ''
    i = 0
    while i < len(toks):
        t = toks[i]
        if t.startswith('<'):
            name = re.match(r'</?\s*(\w+)', t); name = name.group(1).lower() if name else ''
            if name in ('br',): flush()
            elif name in ('li', 'ol', 'ul', 'p') : flush(); 
            else: buf += t
        else:
            j = 0; s = t
            while j < len(s):
                m = re.compile(r'(?<![\d(（])[（(](\d{1,2})[）)]').match(s, j)
                if m and (int(m.group(1)) == last + 1 or int(m.group(1)) == 1) and plain(buf):
                    flush(); last = int(m.group(1)) - 1
                if m: last = int(m.group(1))
                c = s[j]; buf += c; j += 1
                if c in TERM:
                    while j < len(s) and s[j] in CLOSE: buf += s[j]; j += 1
                    # gắn <sup>..</sup> ngay sau
                    k = i + 1
                    while k + 2 < len(toks) and toks[k] == '' and re.match(r'<sup', toks[k + 1] if k + 1 < len(toks) else ''):
                        break
                    if j >= len(s):
                        # nhìn token kế
                        k = i + 1
                        if k + 2 < len(toks) and toks[k].startswith('<sup'):
                            buf += toks[k] + toks[k + 1] + toks[k + 2]; i += 3
                        elif k < len(toks) and toks[k].startswith('</'):
                            pass
                    if not (j < len(s) and re.match(r'\s*[（(]\d', s[j:])) or True:
                        flush()
        i += 1
    flush()
    if carry:
        if segs: segs[-1] += carry
        else: segs.append(carry)
    return segs

# ---------------------------------------------------------------- tách câu Việt
def vi_segments(text):
    text = re.sub(r'^\s*[IVX]+\.?\s*(?:\([一二三四五六七八九十]\))?\s*', '', text.strip())
    text = re.sub(r'\s+', ' ', text)
    # mốc (n) tăng dần
    cuts = set(); last = 0
    for m in re.finditer(r'(?<![\d(])\((\d{1,2})\)', text):
        n = int(m.group(1))
        if n == last + 1 or n == 1: cuts.add(m.start()); last = n
    # mốc số trần "1 ", "2 " tăng dần (sau khoảng trắng/đầu), kế tiếp là chữ
    last = 0
    for m in re.finditer(r'(?:(?<=\s)|^)(\d{1,2})(?=\s+[^\d\s])', text):
        n = int(m.group(1))
        if n == last + 1: cuts.add(m.start()); last = n
    for m in re.finditer(r'[\.!?…]["”)]?(?=\s+[A-ZÀ-Ỵ“"‘(《\d])', text): cuts.add(m.end())
    pts = sorted(c for c in cuts if 0 < c < len(text))
    out = []; p = 0
    for c in pts: out.append(text[p:c].strip()); p = c
    out.append(text[p:].strip()); out = [x for x in out if x]
    # nhãn đứng riêng ("Thử:" / "Thử viết lại…:") gắn tiếp vào mục sau? giữ riêng
    return out

# ---------------------------------------------------------------- ghép
def align(hs, vs):
    n, m = len(hs), len(vs)
    ht = [plain(x) for x in hs]
    r = max(sum(_lv(x) for x in vs) / max(sum(_lh(x) for x in ht), 1), .1)
    INF = 1e9; best = [[INF] * (m + 1) for _ in range(n + 1)]; back = {}; best[0][0] = 0
    moves = [(1, 1), (1, 2), (2, 1), (2, 2), (1, 3), (3, 1), (3, 2), (2, 3), (1, 4), (4, 1)]
    for i in range(n + 1):
        for j in range(m + 1):
            if best[i][j] >= INF: continue
            for di, dj in moves:
                ni, nj = i + di, j + dj
                if ni > n or nj > m: continue
                H = ''.join(ht[i:ni]); V = ' '.join(vs[j:nj])
                cost = abs(math.log((_lv(V) + 5) / (_lh(H) * r + 5))) + (0.2 if (di, dj) != (1, 1) else 0)
                lh_, lv_ = lead(hs[i]), lead(vs[j])
                if lh_ and lv_: cost += -0.7 if lh_ == lv_ else 0.6
                cost -= 0.4 * min(len(_anch(H) & _anch(V)), 3)
                c = best[i][j] + cost
                if c < best[ni][nj]: best[ni][nj] = c; back[(ni, nj)] = (i, j)
    if best[n][m] >= INF: return None
    out = []; i, j = n, m
    while (i, j) != (0, 0):
        pi, pj = back[(i, j)]; out.append(((pi, i), (pj, j))); i, j = pi, pj
    return out[::-1]

def _alignable(h):
    t = plain(h)
    if 'class="xbl"' in h: return False
    if re.fullmatch(r'[（(][一二三四五六七八九十\d]+[）)]', t): return False
    if re.fullmatch(r'(?:[（(][一二三四五六七八九十\d]+[）)]\s*)?(?:[\u4e00-\u9fff]{1,8}\s+){3,}[\u4e00-\u9fff]{1,8}', t): return False
    return len(HAN.findall(t)) >= 3 or len(t) >= 8

def pair(hs, vs):
    """-> list of (hindices tuple, vi_text). Phân đoạn không phải câu (nhãn, danh sách từ) không tham gia ghép."""
    idx = [i for i, h in enumerate(hs) if _alignable(h)]
    H = [hs[i] for i in idx]
    lead_title = 0
    if H and len(H) == len(vs) + 1 and re.match(r'^\s*<b>[^<]*</b>\s*$', H[0]) and not re.search('[。！？，；]', plain(H[0])): lead_title = 1
    H2 = H[lead_title:]; idx2 = idx[lead_title:]
    if len(H2) > len(vs):
        vs2 = [y.strip() + (';' if k < len(x.split(';')) - 1 else '') for x in vs for k, y in enumerate(x.split(';')) if y.strip()]
        if len(vs2) == len(H2): vs = vs2
    if len(H2) == len(vs): g = [((i, i + 1), (i, i + 1)) for i in range(len(H2))]
    else: g = align(H2, vs)
    if g is None: return None
    out = []
    for (a, b), (c, d) in g:
        if b - a == d - c and b - a > 1:
            out += [((idx2[a + t],), vs[c + t]) for t in range(b - a)]
        else:
            out.append((tuple(idx2[a:b]), ' '.join(vs[c:d])))
    return out

# ---------------------------------------------------------------- áp dụng vào HTML của fz
def block_end(s, i):
    depth = 0
    for m in re.finditer(r'<div\b|</div>', s[i:]):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0: return i + m.end()
    return None

OPAQUE_DIV = re.compile(r'<div class="(?:uin|ans|wr|uxp|w|ln)[ "]')
STRUCT = re.compile(r'</?(?:ol|ul|li|blockquote)\b[^>]*>')
def split_parts(main):
    """-> list[(kind, html)] với kind 'raw' (giữ nguyên) hoặc 'run' (đoạn chữ cần tách câu)."""
    main = re.sub(r'<p(\s[^>]*)?>', lambda m_: '<div class="pp"%s>' % (m_.group(1) or ''), main).replace('</p>', '</div>')
    out = []; pos = 0; buf = ''
    def put_run(x):
        if x.strip(): out.append(('run', x))
    i = 0
    while i < len(main):
        m = OPAQUE_DIV.match(main, i)
        if m and main.startswith('<div', i):
            e = block_end(main, i)
            if e: put_run(buf); buf = ''; out.append(('raw', main[i:e])); i = e; continue
        mt = re.match(r'<table\b.*?</table>', main[i:], re.S) if main.startswith('<table', i) else None
        if mt: put_run(buf); buf = ''; out.append(('raw', mt.group(0))); i += len(mt.group(0)); continue
        mh = re.match(r'<h[1-6]\b.*?</h[1-6]>', main[i:], re.S) if main.startswith('<h', i) and re.match(r'<h[1-6]\b', main[i:]) else None
        if mh: put_run(buf); buf = ''; out.append(('raw', mh.group(0))); i += len(mh.group(0)); continue
        ms = STRUCT.match(main, i)
        if ms: put_run(buf); buf = ''; out.append(('raw', ms.group(0))); i += len(ms.group(0)); continue
        mp = re.match(r'<div class="pp"[^>]*>', main[i:]) if main.startswith('<div class="pp"', i) else None
        if mp:
            put_run(buf); buf = ''; out.append(('raw', mp.group(0))); i += len(mp.group(0)); continue
        buf += main[i]; i += 1
    put_run(buf)
    return out

TRAIL = re.compile(r'$^')

def split_card(card_html):
    m = re.match(r'<div[^>]*>', card_html); op = m.group(0)
    return op, card_html[m.end():-6], '</div>'

def rebuild(parts, groups_by_seg):
    """parts: list[(kind, html, [seg indices global])]; groups_by_seg: {global_seg_index: vi_text}"""
    out = []
    for kind, html, idxs, segs in parts:
        if kind == 'raw': out.append(html); continue
        for gi, sg in zip(idxs, segs):
            out.append('<div class="zu">%s</div>' % sg)
            if gi in groups_by_seg: out.append('<div class="trs">%s</div>' % groups_by_seg[gi])
    return ''.join(out)

def apply_entries(S, entries):
    ok = fb = 0
    for key, vi in entries:
        vs = vi_segments(vi)
        pos = None
        for m in re.finditer(r'<div class="(?:card|note)[^"]*"[^>]*>', S):
            e = block_end(S, m.start())
            if e and key in plain(S[m.start():e]): pos = (m.start(), e); break
        regions = []
        if pos: regions = [pos]
        else:
            hm = None
            for m in re.finditer(r'<h3[^>]*>(.*?)</h3>', S, re.S):
                if plain(m.group(1)).startswith(key): hm = m; break
            if not hm: continue
            def region_after(m):
                nxt = re.search(r'<h[23][ >]', S[m.end():])
                end = m.end() + (nxt.start() if nxt else len(S) - m.end())
                out = []; p = m.end()
                for c in re.finditer(r'<div class="card[^"]*"[^>]*>', S[m.end():end]):
                    s0 = m.end() + c.start()
                    if s0 < p: continue
                    e = block_end(S, s0)
                    if e and e <= end: out.append((s0, e)); p = e
                return out, end
            regions, end = region_after(hm)
            if re.search(r'\bIX\.', vi):
                h2m = re.compile(r'<h3[^>]*>九').search(S, end)
                if h2m:
                    r2, _ = region_after(h2m); regions += r2
        if not regions: continue
        card_parts = []; flat = []
        for (a, b) in regions:
            op, main, close = split_card(S[a:b])
            parts = []
            for kind, html in split_parts(main):
                if kind == 'raw': parts.append((kind, html, [], []))
                else:
                    segs = han_segments(html); idxs = list(range(len(flat), len(flat) + len(segs))); flat += segs
                    parts.append((kind, html, idxs, segs))
            card_parts.append((a, b, op, parts, close))
        g = pair(flat, vs) if flat and vs else None
        if g is None:
            a, b, op, parts, close = card_parts[0]; fb += 1
            S = S[:a] + S[a:b][:-6] + '<div class="trs">%s</div></div>' % vi + S[b:]; continue
        by = {hi[-1]: v for hi, v in g}
        pieces = []
        for a, b, op, parts, close in card_parts:
            pieces.append((a, b, op + rebuild(parts, by) + close))
        for a, b, new in sorted(pieces, reverse=True): S = S[:a] + new + S[b:]
        ok += 1
    return S, ok, fb

def _tok(x): return set(re.findall(r'[^\W\d_]{3,}', x.lower()))

def lvb_clean(d):
    """Khối «🇻🇳 …» gộp (.lvb) ở bài 5–8: bỏ nếu bản dịch từng mục đã có ngay trong thẻ, ngược lại đặt ngay dưới dòng đề."""
    removed = moved = 0; pos = 0
    while True:
        i = d.find('<div class="ln lv lvb">', pos)
        if i < 0: break
        e = block_end(d, i)
        lump = d[i:e]; c = d.rfind('<div class="card', 0, i)
        prev = plain(d[c:i]); t = _tok(plain(lump))
        cov = len(t & _tok(prev)) / max(len(t), 1)
        if cov >= .7 or ('<table' in lump and '<table' in d[c:i]):
            d = d[:i] + d[e:]; removed += 1; pos = i; continue
        # đặt dưới dòng đề của thẻ
        m = re.match(r'<div[^>]*>', d[c:])
        k = c + m.end()
        if d.startswith('<h3', k): k = d.find('</h3>', k) + 5
        else:
            k = block_end(d, k) if d.startswith('<div', k) else k
        # bỏ qua dòng pinyin/dịch ngay sau tiêu đề
        while d.startswith('<div class="ln lp"', k) or d.startswith('<div class="ln lv"', k):
            k = block_end(d, k)
        if k and k < i:
            d = d[:i] + d[e:]; d = d[:k] + lump + d[k:]; moved += 1; pos = k + len(lump)
        else: pos = e
    return d, removed, moved


# ---------------------------------------------------------------- chú thích (注释) của 走进课文
import html as _html

def _lesson_span(d, n):
    i = d.find('id="l%d"' % n)
    if i < 0: return None
    s0 = d.find('<section class="les', max(0, i - 40))
    s1 = d.find('<section class="les', s0 + 10); s1 = len(d) if s1 < 0 else s1
    return s0, s1

def _notes_region(S):
    m = re.search(r'<h3[^>]*>\s*注释[^<]*</h3>', S)
    if not m: return None
    start = m.end()
    pg = re.match(r'(?:\s*<div class="ln lv">[^<]*</div>)*\s*(?:<p class="py pg">[^<]*</p>)?', S[start:])
    e = re.search(r'<h[23][ >]', S[start:])
    return m, start, (start + e.start() if e else len(S))

def notes_han(d):
    """bài 5–7: dựng lại chú thích với Hán biên soạn + Việt từng câu."""
    from fz_notes_han import NOTES
    cnt = 0
    for n, notes in NOTES.items():
        sp = _lesson_span(d, n)
        if not sp: continue
        s0, s1 = sp; S = d[s0:s1]
        reg = _notes_region(S)
        if not reg: continue
        m, start, end = reg
        old = S[start:end]
        heads = {int(x.group(1)): x.group(2).strip().rstrip(':：').strip() for x in re.finditer(r'<b>(\d+)\. ([^<]*?)</b>', old)}
        out = ['<div class="ntag">ℹ️ Nguồn chỉ có bản dịch tiếng Việt kèm pinyin; phần chữ Hán của chú thích được biên soạn lại theo nghĩa tiếng Việt.</div>']
        for num in sorted(notes):
            head = heads.get(num, '')
            out.append('<div class="zu nh"><b>%d. %s</b></div>' % (num, _html.escape(head, quote=False)))
            for hz, vi in notes[num]:
                out.append('<div class="zu">%s</div><div class="trs">%s</div>' % (_html.escape(hz, quote=False), _html.escape(vi, quote=False)))
                cnt += 1
        d = d[:s0] + S[:start] + ''.join(out) + S[end:] + d[s1:]
    return d, cnt

def _vi_head_split(vi):
    m = re.match(r'^(\S*[一-鿿][^:：]{0,40}[:：])\s*(.*)$', vi)
    if m: return m.group(1), m.group(2)
    m = re.search(r'(?<=[a-zà-ỹ\)”])\s+(?=[A-ZÀ-Ỵ“])', vi)
    if m and m.start() < 90: return vi[:m.start()], vi[m.end():]
    return None, vi

def notes_ol(d):
    """bài 9–14: mỗi mục <li> gồm Hán + Việt gộp → ghép từng câu."""
    cnt = 0
    for n in range(9, 15):
        sp = _lesson_span(d, n)
        if not sp: continue
        s0, s1 = sp; S = d[s0:s1]
        reg = _notes_region(S)
        if not reg: continue
        m, start, end = reg
        old = S[start:end]
        def fix(mm):
            nonlocal cnt
            hz_html, vi_html = mm.group(1), mm.group(2)
            vi = plain(vi_html)
            k = hz_html.find('：')
            if k < 0: return mm.group(0)
            head_h, rest_h = hz_html[:k + 1], hz_html[k + 1:]
            head_v, rest_v = _vi_head_split(vi)
            hs = han_segments(rest_h); vs = vi_segments(rest_v)
            g = pair(hs, vs) if hs and vs else None
            if g is None: return mm.group(0)
            by = {hi[-1]: v for hi, v in g}
            out = ['<div class="zu nh">%s</div>' % head_h]
            if head_v and re.search(r'[a-zà-ỹ]{2,}', re.sub(r'\([^)]*\)', '', head_v)): out.append('<div class="trs">%s</div>' % _html.escape(head_v, quote=False))
            for i, sg in enumerate(hs):
                out.append('<div class="zu">%s</div>' % sg)
                if i in by: out.append('<div class="trs">%s</div>' % _html.escape(by[i], quote=False))
            cnt += 1
            return '<li>' + ''.join(out) + '</li>'
        new = re.sub(r'<li><div class="ln lz">(.*?)</div><div class="ln lv">(.*?)</div></li>', fix, old, flags=re.S)
        d = d[:s0] + S[:start] + new + S[end:] + d[s1:]
    return d, cnt

CSS = (".zu{margin:.3em 0}.trs{border-left:3px solid var(--bd);padding-left:8px;opacity:.92;margin:2px 0 .7em;"
       "font-size:.92rem;line-height:1.7}main.novi .trs{display:none}.xc.novi .trs{display:none!important}")

def main(path):
    h = open(path, encoding='utf-8').read()
    m = re.search(r'(<script type="application/json" id="src-fz">)(.*?)(</script>)', h, re.S)
    d = json.loads(m.group(2))
    dec = json.JSONDecoder(); stats = []
    for sec in ('l1', 'l2'):
        call = 'TR("#%s",' % sec
        i = d.find(call)
        if i < 0: continue
        j = i + len(call)
        a, k = dec.raw_decode(d, j); k = d.index(',', k) + 1
        while d[k] in ' \n': k += 1
        b, k2 = dec.raw_decode(d, k)
        assert d[k2] == ')', 'TR call khác dạng'
        end = k2 + 1
        if d[end:end + 1] == ';': end += 1
        # vùng HTML của bài
        s0 = d.find('<section class="les', d.find('id="%s"' % sec) - 40)
        s1 = d.find('<section class="les', s0 + 10); s1 = len(d) if s1 < 0 else s1
        # xoá lệnh TR (không dựng .tr lúc chạy nữa) — thực hiện sau khi sửa HTML để chỉ số không lệch
        S = d[s0:s1]
        S2, ok, fb = apply_entries(S, [(x[0], x[1]) for x in b])
        # bài 1 八/九 (HTML nguồn không cân thẻ): chèn tay theo hai nửa của bản dịch
        for x in b:
            if x[0] == '八、课本剧' and ' IX. ' in x[1]:
                v8, v9 = x[1].split(' IX. ', 1)
                v8 = re.sub(r'^\s*VIII\.\s*', '', v8); v9 = re.sub(r'^\s*', '', v9)
                a8 = '根据课文2—5自然段的内容，编写小剧本，并分角色表演。<br/>'
                if a8 in S2: S2 = S2.replace(a8, '<div class="zu">%s</div><div class="trs">%s</div>' % (a8[:-5], v8), 1); ok += 1
                a9 = '鼓励自选。'
                k9 = S2.find(a9, S2.find('九、写一写'))
                if k9 > 0:
                    k9 += len(a9); S2 = S2[:k9] + '<div class="trs">%s</div>' % v9 + S2[k9:]
        stats.append((sec, ok, fb, len(b)))
        d = d[:s0] + S2 + d[s1:]
        i = d.find(call); j = i + len(call)
        a, k = dec.raw_decode(d, j); k = d.index(',', k) + 1
        while d[k] in ' \n': k += 1
        b2, k2 = dec.raw_decode(d, k); end = k2 + 1
        if d[end:end + 1] == ';': end += 1
        d = d[:i] + d[end:]
    d, rm, mv = lvb_clean(d); stats.append(('lvb', rm, mv))
    d, c1 = notes_han(d); d, c2 = notes_ol(d); stats.append(('notes', c1, c2))
    if '.zu{margin' not in d: d = d.replace('</style>', CSS + '</style>', 1)
    h = h[:m.start(2)] + json.dumps(d, ensure_ascii=False).replace('<', '\\u003c') + h[m.end(2):]
    open(path, 'w', encoding='utf-8').write(h)
    print('fz_pair:', stats)

if __name__ == '__main__':
    main(sys.argv[1])
