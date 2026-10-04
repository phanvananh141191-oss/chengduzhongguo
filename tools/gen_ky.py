#!/usr/bin/env python3
"""P5: sinh lại trang bài của ky từ md đã chuẩn hoá (nguon_md_ky/chuan/BaiNN.md).

Dùng: python3 tools/gen_ky.py vào.html ra.html 4 [5 6 ...]
- Hán có ruby theo từng chữ; pinyin lấy theo dòng pinyin trong md khi số âm tiết khớp, nếu không dùng pypinyin.
- Mỗi cặp 中文 / Tiếng Việt thành một khối: Hán (ruby) rồi bản dịch.
- Khối «Ghi chú sắc thái cấu trúc» / «Những từ dễ dịch lệch» gom thành hộp gập «📝 Ghi chú KB (n)».
- Bảng tên nhân vật và Tiêu đề bài thành hộp gập.
"""
import re, sys, os, json, html, collections
from markdown_it import MarkdownIt
from pypinyin import pinyin, Style
from pypinyin.pinyin_dict import pinyin_dict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHUAN = os.path.join(ROOT, 'nguon_md_ky', 'chuan')
md = MarkdownIt('commonmark', {'html': True, 'breaks': False}).enable('table')

HAN = re.compile(r'[\u4e00-\u9fff]')
# ---------------------------------------------------------------- pinyin
SYL = set()
for v in pinyin_dict.values():
    for p in v.split(','): SYL.add(p)
SYL |= {'r', 'er', 'a', 'o', 'e', 'ng', 'n', 'm', 'hm', 'ê', 'hng'}
def toneless(x):
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', x) if not unicodedata.combining(c))
SYL_NT = {toneless(s) for s in SYL}
def split_token(tok):
    t = tok.lower(); n = len(t)
    best = [None] * (n + 1); best[0] = []
    for i in range(n):
        if best[i] is None: continue
        for j in range(i + 1, min(n, i + 7) + 1):
            if t[i:j] in SYL or t[i:j] in SYL_NT:
                cand = best[i] + [t[i:j]]
                if best[j] is None or len(cand) < len(best[j]): best[j] = cand
    return best[n]

PYTOK = re.compile(r"[A-Za-zÜüāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜńňǹḿê]+")
def hint_syllables(pyline, han_text=''):
    s = re.sub(r'🔊.*$', '', pyline).strip()
    if s.startswith('(') and s.endswith(')'): s = s[1:-1]
    s = re.sub(r'\([^)]*\)', ' ', s)
    toks = PYTOK.findall(s)
    for a in re.findall(r'[A-Za-z]+', re.sub(r'🔊.*$', '', re.sub(r'\([^)]*\)', ' ', han_text))):
        for i, tk in enumerate(toks):          # chữ Latin có sẵn trong dòng Hán (A, B, HSK…) không phải âm tiết
            if tk.lower() == a.lower(): del toks[i]; break
    out = []
    for tok in toks:
        seg = split_token(tok)
        if seg is None: return None
        out += seg
    return out

TONE4 = set('àèìòùǜ'); TONE_ANY = set('āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ')
def _tone_of(py):
    for c in py:
        if c in TONE4: return 4
        if c in TONE_ANY: return 1
    return 0
def sandhi(chars, pys):
    """Biến điệu 不 (bù→bú trước thanh 4) và 一 (yī→yí trước thanh 4 / yì trước thanh khác); giữ nguyên khi là số thứ tự/cuối từ."""
    out = list(pys)
    for i, c in enumerate(chars):
        nxt = out[i + 1] if i + 1 < len(out) else ''
        if c == '不' and out[i] == 'bù' and nxt and _tone_of(nxt) == 4: out[i] = 'bú'
        if c == '一' and out[i] == 'yī' and nxt:
            prev = chars[i - 1] if i else ''
            if prev in '第十零二三四五六七八九' and prev: continue
            if i + 1 < len(chars) and chars[i + 1] in '月号日年': continue
            out[i] = 'yí' if _tone_of(nxt) in (4, 0) else 'yì'
    return out

def py_list(text, hint=None):
    """Trả danh sách pinyin cho từng chữ Hán trong text (theo thứ tự)."""
    han = HAN.findall(text)
    if hint and len(hint) == len(han):
        return hint, True
    res = []
    for seg in re.finditer(r'[\u4e00-\u9fff]+', text):
        ps = [x[0] for x in pinyin(seg.group(0), style=Style.TONE, errors='default')]
        res += sandhi(seg.group(0), ps)
    return res, False

STATS = dict(aligned=0, fallback=0)
def ruby_html(h, hint=None):
    """h là HTML đã render; gắn ruby cho chữ Hán nằm ngoài thẻ."""
    parts = re.split(r'(<[^>]+>)', h)
    plain = ''.join(p for p in parts if not p.startswith('<'))
    plain_text = html.unescape(plain)
    pys, ok = py_list(plain_text, hint)
    STATS['aligned' if ok else 'fallback'] += 1
    it = iter(pys); out = []
    for p in parts:
        if p.startswith('<'): out.append(p); continue
        def rep(m):
            try: py = next(it)
            except StopIteration: py = ''
            return '<ruby>%s<rt>%s</rt></ruby>' % (m.group(0), html.escape(py))
        out.append(re.sub(r'[\u4e00-\u9fff]', rep, p))
    return ''.join(out)

# ---------------------------------------------------------------- Hán-Việt
HV = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hanviet.json'), encoding='utf8'))
HV_MISS = collections.Counter()
def hv_of(word):
    w = re.sub(r'[^\u4e00-\u9fff]', '', word)
    if not w: return ''
    out = []; i = 0
    while i < len(w):
        L = min(8, len(w) - i)
        while L > 1 and w[i:i + L] not in HV['W']: L -= 1
        t = w[i:i + L]
        if t in HV['W']: out.append(HV['W'][t])
        else:
            for c in t:
                if c in HV['C']: out.append(HV['C'][c])
                else: out.append(c); HV_MISS[c] += 1
        i += L
    return ' '.join(out)

def hv_pick(word, meaning):
    """Ưu tiên âm Hán-Việt do người dịch ghi ở đầu ô nghĩa («Âm thị (ám thị): …»), không thì tra từ điển."""
    w = re.sub(r'[^\u4e00-\u9fff]', '', word); d = hv_of(word)
    m = re.sub(r'\*\*', '', meaning).strip()
    mm = re.match(r'^([^:：]{1,40}?)\s*[:：]', m)
    if mm and w:
        head = mm.group(1); cands = []
        pm = re.match(r'^(.*?)\s*\(([^)]*)\)\s*$', head)
        parts = [pm.group(1), pm.group(2)] if pm else [head]
        for x in parts:
            x = x.strip().lower()
            if x and len(x.split()) == len(w) and not re.search(r'[\d,;/]', x): cands.append(x)
        if d in cands: return d
        if cands: return cands[0]
    return d

def split_row(line):
    cells = re.split(r'(?<!\\)\|', line.strip())
    return cells[1:-1] if len(cells) >= 3 else None

def add_hv_column(src):
    """Bảng từ vựng (cột 词语 và Nghĩa): thêm cột Hán Việt đứng ngay trước cột nghĩa."""
    lines = src.split('\n')
    hd = split_row(lines[0]) if lines else None
    if not hd: return src
    names = [x.strip().strip('*').strip() for x in hd]
    wi = next((i for i, x in enumerate(names) if x in ('词语', '词')), None)
    vi_ = next((i for i, x in enumerate(names) if x.startswith('Nghĩa')), None)
    if wi is None or vi_ is None or 'Hán Việt' in names or 'Hán-Việt' in names: return src
    out = []
    for k, l in enumerate(lines):
        cells = split_row(l)
        if not cells: out.append(l); continue
        if k == 0: new = ' Hán Việt '
        elif k == 1: new = ' :-- '
        else:
            new = ' '
            if wi < len(cells):
                wc = re.sub(r'🔊|\*\*', '', cells[wi]); mp = re.search(r'\s*\(([^()\u4e00-\u9fff]+)\)\s*$', wc)
                if mp and re.search(r'[A-Za-zÀ-ỹ]', mp.group(1)):       # «欣欣向荣 (hân hân hướng vinh)»: lấy âm Hán-Việt người dịch ghi, bỏ khỏi ô từ
                    new = ' ' + mp.group(1).strip() + ' '
                    cells[wi] = cells[wi].replace(mp.group(0), '', 1) if mp.group(0) in cells[wi] else wc[:mp.start()]
                else:
                    new = ' ' + hv_pick(wc, cells[vi_] if vi_ < len(cells) else '') + ' '
                hw = re.sub(r'[^\u4e00-\u9fff]', '', wc); L = CUR_LESSON[0]
                kw = next((x for x in KBI.get(L, {}).get('w', []) if re.sub(r'[^\u4e00-\u9fff]', '', x) == hw), None) if hw else None
                if kw:
                    new = new.rstrip() + ' <a id="s%d-w-%s" class="kbl" href="#" data-kb="lessons/%02d.md::kbw-%s" title="Mở mục từ trong KB">🔗</a> ' % (L, kw, L, kw)
                    KYMAP.setdefault(L, {}).setdefault('kbw-' + kw, 's%d-w-%s' % (L, kw))
        cells.insert(vi_, new)
        out.append('|' + '|'.join(cells) + '|')
    return '\n'.join(out)

KBH = {}      # n -> {tên: chỉ số heading trong trang KB của bài}
def load_kb(html_text):
    m = re.search(r'<script id="kb" type="application/json">(.*?)</script>', json.loads(re.search(r'id="src-kb">(.*?)</script>', html_text, re.S).group(1).replace('\\u003c', '<')), re.S)
    K = json.loads(m.group(1).replace('<\\/', '</'))
    _kb_items(K)
    for n in range(1, 13):
        hs = []; fence = False
        for l in K['lessons/%02d.md' % n].split('\n'):
            if re.match(r'^```', l): fence = not fence
            if not fence:
                mm = re.match(r'^(#{1,6})\s+(.*)', l)
                if mm: hs.append(mm.group(2))
        f = lambda pat, start=0: next((i for i in range(start, len(hs)) if re.search(pat, hs[i], re.I)), None)
        plb = f(r'^Phụ lục B')
        KBH[n] = dict(muctieu=f(r'^1\. '), tuvung=f(r'^3\.1 '), dichlech=f(r'^3\.1\.4'), nguphap=f(r'^3\.3 '), cautruc=f(r'^3\.4 '), chucnang=f(r'^3\.5'), plb=plb, pla=f(r'^Phụ lục A'),
                      prepare=f(r'^PREPARE', plb), dialog=f(r'促成 · 对话|对话', plb), ext=f(r'拓展', plb), produce=f(r'^PRODUCE', plb), eval=f(r'^评价', plb), appx=f(r'^附录', plb))

KBI = {}   # n -> dict(w=[từ], d=[từ], s=[(chỉ số, cụm Hán)])
KYMAP = {}  # n -> {id mục KB: id phần tử ky}
def _kb_items(K):
    for n in range(1, 13):
        ctx = ''; w = []; d = []; st = []; rows_k = 0; in_tab = False; fence = False
        lines = K['lessons/%02d.md' % n].split('\n')
        for i, l in enumerate(lines):
            if re.match(r'^```', l): fence = not fence
            if fence: continue
            mm = re.match(r'^(#{1,6})\s+(.*)', l)
            if mm: ctx = mm.group(2); in_tab = False; rows_k = 0; continue
            if not l.startswith('|'): in_tab = False; continue
            if not in_tab:
                in_tab = True; rows_k = 0; kind = 'd' if re.search(r'dễ dịch lệch', ctx, re.I) else 's' if re.search(r'^3\.4|Cấu trúc câu', ctx) else 'w' if re.search(r'^3\.1\.[12]|^3\.2|词语表|Cụm từ', ctx) else None
                continue                      # dòng tiêu đề cột
            if re.match(r'^\|\s*:?-{2,}', l): continue
            rows_k += 1
            cells = split_row(l)
            if not cells or not kind: continue
            if kind == 's':
                st.append((rows_k, re.sub(r'[*_`]', '', cells[0]).strip())); continue
            word = ''
            for c in cells[:3]:
                t = re.sub(r'[➕\s*_`]', '', c)
                if HAN.search(t): word = t; break
            if word: (d if kind == 'd' else w).append(word)
        KBI[n] = dict(w=w, d=d, s=st)

def kbl(n, key, label):
    i = KBH[n].get(key)
    if i is None and key in ('prepare', 'dialog', 'ext', 'produce', 'eval', 'appx'): i = KBH[n].get('plb')
    if i is None: return ''
    return '<a class="kbl" href="#" data-kb="lessons/%02d.md::kbh%d">%s</a>' % (n, i, label)

SECID = {'PREPARE': 'prepare', 'EXPLORE': 'explore', '促成 · 对话': 'dialog', '促成 · 拓展': 'ext', '促成 · 段话': 'dialog', 'PRODUCE': 'produce', '评价': 'eval', '附录': 'appx'}
def sec_key(t):
    for k, v in SECID.items():
        if t.startswith(k): return v
    return None

CUR_LESSON = [0]
EX_STATS = collections.Counter()
def add_example_column(src, lesson):
    """Thêm cột «Ví dụ»: mỗi ô có đủ câu Hán, pinyin, tiếng Việt (ưu tiên trong bài → ky khác → giáo trình khác → tự soạn)."""
    import vi_du
    vi_du.init()
    lines = src.split('\n'); hd = split_row(lines[0]) if lines else None
    if not hd: return src
    names = [x.strip().strip('*').strip() for x in hd]
    wi = next((i for i, x in enumerate(names) if x in ('词语', '词')), None)
    if wi is None or 'Ví dụ' in names: return src
    out = []; used = set()
    for k, l in enumerate(lines):
        cells = split_row(l)
        if not cells: out.append(l); continue
        if k == 0: cells.append(' Ví dụ ')
        elif k == 1: cells.append(' :-- ')
        else:
            cell, lab = vi_du.example_cell(re.sub(r'🔊|\*\*', '', cells[wi]), lesson, used) if wi < len(cells) and HAN.search(cells[wi]) else ('', None)
            EX_STATS[lab or 'none'] += 1
            cells.append(' ' + cell + ' ')
        out.append('|' + '|'.join(cells) + '|')
    return '\n'.join(out)

# ---------------------------------------------------------------- md → khối
LAB_ZH = re.compile(r'^\*\*中文[:：]\*\*\s*')
LAB_VI = re.compile(r'^\*\*Tiếng Việt:\*\*\s*')
PYLINE = re.compile(r'^\*[^*].*\*\s*\\?$')

MARK = re.compile(r'(?:(?<=^)|(?<=[\s：:。！？；;)）”"、,，]))(\d{1,2})[\.．](?=\s|[\u4e00-\u9fffA-ZÀ-Ỹ“"(（])')
def itemize(s):
    """Câu có nhiều mục đánh số «1. … 2. …» hoặc bullet «•» trên cùng một dòng → xuống dòng trước mỗi mục."""
    if '<br' in s and s.count('<br') >= 2: return s
    ok = []; exp = 1
    for m in MARK.finditer(s):
        if int(m.group(1)) == exp: ok.append(m.start()); exp += 1
    if len(ok) >= 2:
        out = []; last = 0
        for pos in ok:
            out.append(s[last:pos].rstrip())
            if pos > 0: out.append('<br>')
            last = pos
        out.append(s[last:]); s = ''.join(out)
    s = re.sub(r'(?<=\S)\s*[•●▪]\s*', '<br>• ', s)
    return s

def inline(s):
    return md.renderInline(itemize(s))

def split_blocks(text):
    """Chia thân thành khối cấp cao bằng markdown-it, mỗi khối giữ nguyên dòng nguồn."""
    # nhãn đứng một mình («**中文：**\» / «**Tiếng Việt:**\») dính với dòng kế để danh sách «1.» không tách khỏi nhãn
    text = re.sub(r'^(\*\*(?:中文[:：]|Tiếng Việt:)\*\*)\\\n(?=\S)', r'\1 ', text, flags=re.M)
    toks = md.parse(text)
    lines = text.split('\n'); blocks = []
    for t in toks:
        if t.level != 0 or t.map is None: continue
        if t.nesting == -1: continue
        blocks.append((t.type[:-5] if t.type.endswith('_open') else t.type, '\n'.join(lines[t.map[0]:t.map[1]])))
    return blocks

def zh_para(src):
    """Tách đoạn Hán: (hán_html_lines, pinyin_lines, vi_lines nếu nhãn Tiếng Việt nằm cùng đoạn)."""
    ls = src.split('\n'); han = []; py = []; vi = []; mode = 'zh'
    for l in ls:
        l2 = l.rstrip().rstrip('\\').rstrip()
        if LAB_VI.match(l2.strip()):
            mode = 'vi'; l2 = LAB_VI.sub('', l2.strip())
        elif mode == 'zh' and han and re.match(r'^\*\*[^*]{1,40}[:：]\*\*\s*\S', l2.strip()) and not HAN.search(l2):
            mode = 'vi'                    # «**Tên người nói:** lời dịch» nằm cùng đoạn với lời Hán
        if mode == 'vi':
            if l2.strip(): vi.append(l2)
            continue
        if LAB_ZH.match(l2.strip()): l2 = LAB_ZH.sub('', l2.strip())
        if not l2.strip(): continue
        if PYLINE.match(l2.strip()) and not HAN.search(l2): py.append(l2.strip().strip('*').strip()); continue
        han.append(l2)
    return han, py, vi

SPLIT_ZH = re.compile(r'(?<=[。！？!?])(?=[^”’」』）)\s])')
SPLIT_VI = re.compile(r'(?<=[.!?…])\s+(?=[A-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ“"(\d])')

def _merge_unbalanced(parts):
    out = []
    for x in parts:
        if out and (out[-1].count('**') % 2 or out[-1].count('*') % 2 and False): out[-1] += ' ' + x
        else: out.append(x)
    return out

def sent_zh(t):
    return _merge_unbalanced([x for x in SPLIT_ZH.split(t) if x.strip()]) or [t]

def sent_vi(t):
    return _merge_unbalanced([x for x in SPLIT_VI.split(t) if x.strip()]) or [t]

def items_of(lines):
    out = []
    for l in lines: out += [x for x in itemize(l).split('<br>') if x.strip()]
    return out

def _len_h(x): return len(HAN.findall(x)) or len(re.sub(r'\W', '', x))
def _len_v(x): return len(re.sub(r'\W', '', x))

def align(hs, vs):
    """Ghép các câu Hán và câu Việt khi số câu khác nhau: quy hoạch động theo tỉ lệ độ dài, cho phép gộp 1–3 câu."""
    n, m = len(hs), len(vs)
    r = max(sum(_len_v(x) for x in vs) / max(sum(_len_h(x) for x in hs), 1), .1)
    INF = 1e9; best = [[INF] * (m + 1) for _ in range(n + 1)]; back = {}
    best[0][0] = 0
    moves = [(1, 1), (1, 2), (2, 1), (2, 2), (1, 3), (3, 1)]
    for i in range(n + 1):
        for j in range(m + 1):
            if best[i][j] >= INF: continue
            for di, dj in moves:
                ni, nj = i + di, j + dj
                if ni > n or nj > m: continue
                H = ''.join(hs[i:ni]); V = ''.join(vs[j:nj])
                lh, lv = _len_h(H) * r, _len_v(V)
                cost = abs(__import__('math').log((lv + 6) / (lh + 6))) + (0.25 if (di, dj) != (1, 1) else 0)
                if H.count('？') + H.count('?') != V.count('?'): cost += 0.7
                c = best[i][j] + cost
                if c < best[ni][nj]: best[ni][nj] = c; back[(ni, nj)] = (i, j)
    if best[n][m] >= INF: return None
    out = []; i, j = n, m
    while (i, j) != (0, 0):
        pi, pj = back[(i, j)]
        out.append((''.join(hs[pi:i]), ' '.join(vs[pj:j]))); i, j = pi, pj
    return out[::-1]

def pair_up(han, vi):
    """Ghép Hán–Việt ở mức nhỏ nhất khớp được: câu → mục → khối. Trả list (hán, việt) hoặc None."""
    hi, vv = items_of(han), items_of(vi)
    if hi and vv and len(hi) == len(vv):
        out = []
        for h, v in zip(hi, vv):
            hs, vs = sent_zh(h), sent_vi(v)
            if len(hs) == len(vs) and len(hs) > 1: out += list(zip(hs, vs))
            elif len(hs) > 1 and len(vs) > 1 and (al := align(hs, vs)): out += al
            else: out.append((h, v))
        return out
    hs = [x for h in hi for x in sent_zh(h)]; vs = [x for v in vv for x in sent_vi(v)]
    if hs and len(hs) == len(vs): return list(zip(hs, vs))
    if len(hs) > 1 and len(vs) > 1: return align(hs, vs)
    return None

UCNT = [0]
def wrap_word(h, word, cls, kb):
    """Bọc các chữ ruby liên tiếp của `word` thành liên kết sang KB (lần xuất hiện đầu tiên)."""
    pat = ''.join(r'<ruby>%s<rt>[^<]*</rt></ruby>' % re.escape(c) for c in word)
    m = re.search(pat, h)
    if not m: return h, False
    return h[:m.start()] + '<a class="kbl %s" href="#" data-kb="%s">%s</a>' % (cls, kb, m.group(0)) + h[m.end():], True

def decorate(h, plain_zh, n):
    """Gắn liên kết KB vào câu Hán: từ dễ dịch lệch (gạch chấm) và cấu trúc có ghi chú sắc thái (📝 cuối câu)."""
    if n not in KBI: return h, []
    ids = []; marks = []
    for wd in KBI[n]['d']:
        c = re.sub(r'[^\u4e00-\u9fff]', '', wd)
        if len(c) >= 1 and c in plain_zh:
            h, ok = wrap_word(h, c, 'kbw', 'lessons/%02d.md::kbd-%s' % (n, wd))
            if ok: ids.append('kbd-' + wd)
    for idx, phrase in KBI[n]['s']:
        segs = [x for x in re.split(r'[^\u4e00-\u9fff]+', phrase) if len(x) >= 2]
        if not segs or sum(len(x) for x in segs) < 4: continue
        if all(x in plain_zh for x in segs):
            marks.append('<a class="kbl kbm" href="#" data-kb="lessons/%02d.md::kbs-%d" title="Ghi chú sắc thái trong KB: %s">📝</a>' % (n, idx, html.escape(phrase[:40], quote=True)))
            ids.append('kbs-%d' % idx)
        if len(marks) >= 3: break
    return h + ''.join(marks), ids

def render_pair(zh_src, vi_src=None):
    han, py, vi_in = zh_para(zh_src)
    vi = list(vi_in)
    if vi_src is not None:
        for l in vi_src.split('\n'):
            l2 = LAB_VI.sub('', l.strip().rstrip('\\').rstrip())
            if l2.strip(): vi.append(l2)
    if len(vi) > 1 and re.match(r'^\*\*[^*]{1,40}[:：]\*\*$', vi[0].strip()):   # nhãn người nói đứng riêng một dòng → dính với dòng sau
        vi = [vi[0].strip() + ' ' + vi[1].strip()] + vi[2:]
    spk = ''
    if han:
        ms = re.match(r'^\*\*(.+?)[：:]\*\*\s*(.*)$', han[0].strip())
        if ms: spk = ms.group(1); han = ([ms.group(2)] if ms.group(2).strip() else []) + han[1:]
    hint = hint_syllables(' '.join(py), ' '.join(han)) if py else None
    if hint is not None and len(hint) != len(HAN.findall(' '.join(han))): hint = None
    pairs = pair_up(han, vi) if vi else None
    L = CUR_LESSON[0]; UCNT[0] += 1; uid = 's%d-u%d' % (L, UCNT[0])
    def note(ids):
        for i_ in ids: KYMAP.setdefault(L, {}).setdefault(i_, uid)
    if pairs is None:
        h = ruby_html('<br>'.join(inline(x) for x in han), hint)
        h, ids = decorate(h, re.sub(r'[*_`]', '', ' '.join(han)), L); note(ids)
        if spk: h = '<strong>%s：</strong> %s' % (ruby_html(html.escape(spk)), h)
        v = '<br>'.join(inline(x) for x in vi)
        return '<div class="u3" id="%s"><div class="zh">%s</div>%s</div>' % (uid, h, ('<div class="vi">%s</div>' % v) if v else '')
    out = []; pos = 0; first = True
    for hz, vz in pairs:
        nh = len(HAN.findall(hz))
        h = ruby_html(inline(hz), hint[pos:pos + nh] if hint is not None else None); pos += nh
        h, ids = decorate(h, re.sub(r'[*_`]', '', hz), L); note(ids)
        if first and spk: h = '<strong>%s：</strong> %s' % (ruby_html(html.escape(spk)), h)
        first = False
        out.append('<div class="zh">%s</div><div class="vi">%s</div>' % (h, inline(vz)))
    return '<div class="u3" id="%s">%s</div>' % (uid, ''.join(out))

def is_zh_para(src):
    s = src.strip()
    if LAB_ZH.match(s): return True
    return bool(HAN.search(s)) and any(PYLINE.match(l.strip()) and not HAN.search(l) for l in s.split('\n'))

def is_vi_para(src):
    s = src.strip()
    if LAB_VI.match(s): return True
    first = s.split('\n')[0]
    return bool(re.match(r'^\*\*[^*：:]{1,40}[:：]\*\*\\?$', first.strip())) and not HAN.search(s)

def _key(x): return re.sub(r'[^A-Za-z0-9\u4e00-\u9fff]', '', x)

def strip_echo(title, blocks):
    """Bỏ cặp 中文/Việt đầu mục nếu chỉ lặp lại tiêu đề mục."""
    if not blocks or blocks[0][0] != 'paragraph' or not is_zh_para(blocks[0][1]): return blocks
    han, py, vi = zh_para(blocks[0][1]); hk = _key(' '.join(han)); tk = _key(title)
    if not hk or not HAN.search(hk) or hk not in tk and tk not in hk: return blocks
    if len(hk) > len(tk) + 4: return blocks
    k = 1
    if not vi and len(blocks) > 1 and blocks[1][0] == 'paragraph' and is_vi_para(blocks[1][1]): k = 2
    return blocks[k:]

META = re.compile(r'^(\*\*(Các mục đã dịch|Lưu ý văn bản|Không có|Lưu ý)|Tên nhân vật dùng theo|Xưng hô dùng nhất quán như Phần|\*Lưu ý văn bản)')
META_BUF = []

def render_blocks(blocks, in_note=False):
    out = []; i = 0
    while i < len(blocks):
        typ, src = blocks[i]
        if not in_note and typ == 'hr': i += 1; continue
        if not in_note and typ == 'paragraph' and META.match(src.strip()):
            META_BUF.append(src); i += 1; continue
        if typ == 'paragraph' and not in_note and is_zh_para(src):
            if i + 1 < len(blocks) and blocks[i + 1][0] == 'paragraph' and is_vi_para(blocks[i + 1][1]) and not zh_para(src)[2]:
                out.append(render_pair(src, blocks[i + 1][1])); i += 2; continue
            out.append(render_pair(src)); i += 1; continue
        if typ == 'paragraph' and not in_note and HAN.search(src) and not PYLINE.match(src.strip()):
            out.append(ruby_para(src)); i += 1; continue
        if typ == 'table':
            out.append(render_table(src, in_note)); i += 1; continue
        h = md.render('\n'.join(itemize(l) for l in src.split('\n')) if typ == 'paragraph' else src)
        if not in_note and HAN.search(src): h = ruby_html(h)
        out.append(h); i += 1
    return '\n'.join(out)

def ruby_para(src):
    return ruby_html(md.render('\n'.join(itemize(l) for l in src.split('\n'))))

PY_IN_CELL = re.compile(r'(?:<br\s*/?>)\s*\*[^*|]*\*(?=\s*(?:\||$))', re.M)
def render_table(src, in_note):
    if not in_note: src = add_example_column(add_hv_column(PY_IN_CELL.sub('', src)), CUR_LESSON[0])      # pinyin trong ô đã có ruby → bỏ dòng pinyin; thêm cột Hán Việt
    h = md.render(src)
    if in_note: return '<div class="tw">%s</div>' % h
    # không gắn ruby cho cột pinyin
    rows = re.split(r'(</tr>)', h); out = []
    for r in rows:
        cells = re.split(r'(<t[dh][^>]*>.*?</t[dh]>)', r, flags=re.S); o = []
        for c in cells:
            m = re.match(r'(<t[dh][^>]*>)(.*?)(</t[dh]>)', c, re.S)
            if m and HAN.search(m.group(2)) and 'ex-zh' not in m.group(2): c = m.group(1) + ruby_html(m.group(2)) + m.group(3)
            o.append(c)
        out.append(''.join(o))
    return '<div class="tw">%s</div>' % ''.join(out)

# ---------------------------------------------------------------- toàn bài
def parse_sections(text):
    lines = text.split('\n'); secs = []; cur = None; fence = False
    for l in lines:
        if l.strip().startswith('```'): fence = not fence
        m = None if fence else re.match(r'^(#{1,6})\s+(.*?)\s*$', l)
        if m:
            cur = dict(lv=len(m.group(1)), t=m.group(2), body=[]); secs.append(cur)
        elif cur is not None: cur['body'].append(l)
    return secs

def gen_lesson(n):
    CUR_LESSON[0] = n; UCNT[0] = 0
    text = open(os.path.join(CHUAN, 'Bai%02d.md' % n), encoding='utf8').read()
    secs = parse_sections(text)
    h1 = secs[0]; m = re.match(r'^(第\d+课)\s+(.*?)\s*·\s*(Bài\s*\d+:\s*.*)$', h1['t'])
    zh_title = '%s %s' % (m.group(1), m.group(2)); vi_title = m.group(3)
    out = ['<h1>%s</h1>' % ruby_html(html.escape(zh_title)), '<p><em>%s</em></p>' % html.escape(vi_title)]
    row = ' · '.join(x for x in (kbl(n, 'muctieu', 'Mục tiêu'), kbl(n, 'tuvung', 'Từ vựng'), kbl(n, 'nguphap', 'Ngữ pháp'), kbl(n, 'cautruc', 'Cấu trúc câu'), kbl(n, 'chucnang', 'Chức năng giao tiếp'), kbl(n, 'plb', 'Toàn văn song ngữ'), kbl(n, 'pla', 'Lưu ý văn bản')) if x)
    if row: out.append('<p class="kbrow">📚 <b>Knowledge Base</b> của bài: %s</p>' % row)
    box = None; nnote = 0; k = 1; cur_sec = ['prepare']
    def close_box():
        nonlocal box, nnote
        if box is not None:
            lk = ' · '.join(x for x in (kbl(n, 'cautruc', 'Cấu trúc câu (mục 3.4)'), kbl(n, 'dichlech', 'Từ dễ dịch lệch (mục 3.1.4)'), kbl(n, cur_sec[0] if cur_sec[0] in ('prepare', 'dialog', 'ext', 'produce', 'eval', 'appx') else 'plb', 'Toàn văn phần này')) if x)
            out.append('<details class="kbn"><summary>%s</summary>%s%s</details>' % (box[0] % nnote if '%d' in box[0] else box[0], ''.join(box[1]), ('<div class="kbn-i kblinks">Mở trong KB: %s</div>' % lk) if lk else ''))
            box = None; nnote = 0
    while k < len(secs):
        s = secs[k]; k += 1; t = s['t']; body = '\n'.join(s['body']).strip('\n')
        is_note = t.startswith('📝') and 'Ghi chú sắc thái' in t or t.startswith('📝') and 'dễ dịch lệch' in t
        if is_note:
            if box is None: box = ['📝 Ghi chú KB (%d)', []]
            nnote += 1
            box[1].append('<div class="kbn-i"><h5>%s</h5>%s</div>' % (html.escape(t[2:].strip()), render_blocks(split_blocks(body), True)))
            continue
        close_box()
        if t in ('Tiêu đề bài', 'Bảng tên nhân vật'):
            lab = {'Tiêu đề bài': 'Tiêu đề bài (bản dịch)', 'Bảng tên nhân vật': 'Bảng tên nhân vật'}[t]
            out.append('<details class="kbn"><summary>%s</summary>%s</details>' % (lab, render_blocks(split_blocks(body), True)))
            continue
        lv = s['lv']
        ht = html.escape(t)
        if HAN.search(t): ht = ruby_html(ht)
        sk = sec_key(t)
        if sk: cur_sec[0] = sk
        out.append('<h%d%s>%s</h%d>' % (lv, (' id="s%d-%s"' % (n, sk)) if sk else '', ht, lv))
        if body.strip(): out.append(render_blocks(strip_echo(t, split_blocks(body))))
    close_box()
    if META_BUF:
        out.append('<details class="kbn"><summary>📝 Ghi chú của dịch giả (%d)</summary><div class="kbn-i">%s</div><div class="kbn-i kblinks">Mở trong KB: %s</div></details>' % (len(META_BUF), render_blocks([('paragraph', x) for x in META_BUF], True), kbl(n, 'pla', 'Phụ lục A · Lưu ý văn bản')))
        META_BUF.clear()
    out.append('<hr/>')
    return '\n'.join(out), zh_title

CSS = '''/*ky-gen*/
.u3{margin:.7em 0;padding:.1em 0 .1em .8em;border-left:3px solid var(--bd)}
.u3 .zh{font-size:1.02em}
.u3 .vi{color:var(--mut);font-size:.9em;line-height:1.6;margin-top:.15em}
.u3 .vi+.zh{margin-top:.55em}
.ex-zh{font-size:.95em;color:var(--fg);line-height:2.1} .ex-zh mark{background:var(--hl);color:inherit;border-radius:3px;padding:0 1px}
.ex-vi{font-size:.85em;color:var(--mut)}
.ex-src{font-size:.68em;color:var(--ac);opacity:.8}
.kbrow{font-size:.85em;color:var(--mut);margin:.4em 0 1em} a.kbl{color:var(--ac);text-decoration:none;border-bottom:1px dotted var(--ac)} a.kbl:hover{background:var(--hl)}
.kbm{font-size:.7em;vertical-align:super;margin-left:.2em;text-decoration:none;border:0}
a.kbw{border-bottom:1px dotted var(--ac);color:inherit;text-decoration:none}
.kblinks{font-size:.82em;color:var(--mut);padding-bottom:.6em}
details.kbn{margin:1em 0;border:1px solid var(--bd);border-radius:8px;background:var(--card)}
details.kbn>summary{cursor:pointer;padding:6px 12px;color:var(--ac);font-size:.92em}
details.kbn[open]>summary{border-bottom:1px solid var(--bd)}
details.kbn .kbn-i{padding:4px 14px}
details.kbn h5{margin:.8em 0 .2em;font-size:.95em;color:var(--mut)}
details.kbn p,details.kbn li,details.kbn td,details.kbn th{font-size:.88em;line-height:1.65}
h4{margin:1.2em 0 .3em;font-size:1em;color:var(--ac)}
'''

def main():
    src, dst = sys.argv[1], sys.argv[2]; lessons = [int(x) for x in sys.argv[3:]] or [4]
    s = open(src, encoding='utf8').read()
    m = re.search(r'(<script type="application/json" id="src-ky">)(.*?)(</script>)', s, re.S)
    ky = json.loads(m.group(2).replace('\\u003c', '<'))
    if '/*ky-gen*/' not in ky:
        ky = ky.replace('</style>', CSS + '</style>', 1)
    load_kb(s)
    for n in lessons:
        body, zh = gen_lesson(n)
        pat = re.compile(r'(<section data-t="[^"]*" id="s%d">)(.*?)(</section>)' % n, re.S)
        assert pat.search(ky), n
        ky = pat.sub(lambda mm: mm.group(1) + body + mm.group(3), ky, count=1)
        print('bài %d: %d ký tự HTML' % (n, len(body)))
    if HV_MISS: print('Hán-Việt: chữ chưa có trong từ điển:', ''.join(HV_MISS))
    print('Ví dụ trong bảng từ:', dict(EX_STATS))
    print('ruby: khớp pinyin md %(aligned)d khối, dùng pypinyin %(fallback)d khối' % STATS)
    json.dump({str(k): v for k, v in KYMAP.items()}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_kymap.json'), 'w', encoding='utf8'), ensure_ascii=False)
    new = json.dumps(ky, ensure_ascii=False).replace('<', '\\u003c')
    open(dst, 'w', encoding='utf8').write(s[:m.start(2)] + new + s[m.end(2):])

if __name__ == '__main__':
    main()
