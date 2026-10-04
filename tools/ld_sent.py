"""Tách đoạn đọc của ld thành các câu (Hán, pinyin, Việt) và ghép Việt vào đúng câu Hán."""
import re, math

def _len_h(x): return len(re.findall(r'[一-鿿]', x)) + .3 * len(re.findall(r'\d+', x))
def _len_v(x): return len(re.findall(r'\w+', x))

TERM = r'[^。！？!?]+[。！？!?]*[”」』）)]*'
def sent_zh(x): return [s.strip() for s in re.findall(TERM, x) if s.strip()]
def sent_vi(x):
    out = []; pos = 0
    for m in re.finditer(r'[\.!?…]["”)]?(?=\s+[A-ZÀ-Ỵ“"‘(《\d])', x):
        out.append(x[pos:m.end()].strip()); pos = m.end()
    out.append(x[pos:].strip())
    return [t for t in out if t]

def _anchors(x):
    return {t.lower().replace(',', '').replace('.', '') for t in re.findall(r'\d[\d.,]*|[A-Za-zÀ-ž]{4,}', x)}

def align(hs, vs):
    n, m = len(hs), len(vs)
    r = max(sum(_len_v(x) for x in vs) / max(sum(_len_h(x) for x in hs), 1), .1)
    INF = 1e9; best = [[INF] * (m + 1) for _ in range(n + 1)]; back = {}; best[0][0] = 0
    moves = [(1, 1), (1, 2), (2, 1), (2, 2), (1, 3), (3, 1), (1, 4), (4, 1)]
    for i in range(n + 1):
        for j in range(m + 1):
            if best[i][j] >= INF: continue
            for di, dj in moves:
                ni, nj = i + di, j + dj
                if ni > n or nj > m: continue
                H = ''.join(hs[i:ni]); V = ' '.join(vs[j:nj])
                lh, lv = _len_h(H) * r, _len_v(V)
                cost = abs(math.log((lv + 6) / (lh + 6))) + (0.25 if (di, dj) != (1, 1) else 0)
                if H.count('？') + H.count('?') != V.count('?'): cost += 0.7
                if ('《' in H) != ('《' in V): cost += 0.4
                ah, av = _anchors(H), _anchors(V); cost -= 0.45 * min(len(ah & av), 3)
                c = best[i][j] + cost
                if c < best[ni][nj]: best[ni][nj] = c; back[(ni, nj)] = (i, j)
    if best[n][m] >= INF: return None
    out = []; i, j = n, m
    while (i, j) != (0, 0):
        pi, pj = back[(i, j)]
        out.append(((pi, i), ' '.join(vs[pj:j]))); i, j = pi, pj
    return out[::-1], r

def pair_para(p):
    """-> list of dict(h,p,v,flag). Mỗi câu Hán có pinyin riêng; Việt gắn vào câu cuối của nhóm (nhóm gộp = 1 khối)."""
    hs = sent_zh(p['h']); ps = sent_zh(p['p']); vs = sent_vi(p['v'])
    if len(ps) != len(hs): ps = [''] * len(hs)
    if len(hs) == len(vs): g = [((i, i + 1), vs[i]) for i in range(len(hs))]; r = None
    else:
        a = align(hs, vs)
        if a is None: g = [((0, len(hs)), ' '.join(vs))]
        else: g, r = a
    out = []
    for (a_, b_), v in g:
        out.append(dict(h=''.join(hs[a_:b_]), p=' '.join(ps[a_:b_]).strip(), v=v))
    return out
