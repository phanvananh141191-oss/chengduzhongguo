#!/usr/bin/env python3
"""P5: sinh lại trang bài của ky từ md đã chuẩn hoá (nguon_md_ky/chuan/BaiNN.md).

Dùng: python3 tools/gen_ky.py vào.html ra.html 4 [5 6 ...]
- Hán có ruby theo từng chữ; pinyin lấy theo dòng pinyin trong md khi số âm tiết khớp, nếu không dùng pypinyin.
- Mỗi cặp 中文 / Tiếng Việt thành một khối: Hán (ruby) rồi bản dịch.
- Khối «Ghi chú sắc thái cấu trúc» / «Những từ dễ dịch lệch» gom thành hộp gập «📝 Ghi chú KB (n)».
- Bảng tên nhân vật và Tiêu đề bài thành hộp gập.
"""
import re, sys, os, json, html
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

def py_list(text, hint=None):
    """Trả danh sách pinyin cho từng chữ Hán trong text (theo thứ tự)."""
    han = HAN.findall(text)
    if hint and len(hint) == len(han):
        return hint, True
    res = []
    for seg in re.finditer(r'[\u4e00-\u9fff]+', text):
        res += [x[0] for x in pinyin(seg.group(0), style=Style.TONE, errors='default')]
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
        if mode == 'vi':
            if l2.strip(): vi.append(l2)
            continue
        if LAB_ZH.match(l2.strip()): l2 = LAB_ZH.sub('', l2.strip())
        if not l2.strip(): continue
        if PYLINE.match(l2.strip()) and not HAN.search(l2): py.append(l2.strip().strip('*').strip()); continue
        han.append(l2)
    return han, py, vi

def render_pair(zh_src, vi_src=None):
    han, py, vi_in = zh_para(zh_src)
    vi = list(vi_in)
    if vi_src is not None:
        for l in vi_src.split('\n'):
            l2 = LAB_VI.sub('', l.strip().rstrip('\\').rstrip())
            if l2.strip(): vi.append(l2)
    spk = ''
    if han:
        ms = re.match(r'^\*\*(.+?)[：:]\*\*\s*(.*)$', han[0].strip())
        if ms: spk = ms.group(1); han = ([ms.group(2)] if ms.group(2).strip() else []) + han[1:]
    hint = hint_syllables(' '.join(py), ' '.join(han)) if py else None
    zh_html = '<br>'.join(inline(x) for x in han)
    h = ruby_html(zh_html, hint)
    if spk: h = '<strong>%s：</strong> %s' % (ruby_html(html.escape(spk)), h)
    v = '<br>'.join(inline(x) for x in vi)
    return '<div class="u3"><div class="zh">%s</div>%s</div>' % (h, ('<div class="vi">%s</div>' % v) if v else '')

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
    if not in_note: src = PY_IN_CELL.sub('', src)      # pinyin trong ô đã có ruby → bỏ dòng pinyin
    h = md.render(src)
    if in_note: return '<div class="tw">%s</div>' % h
    # không gắn ruby cho cột pinyin
    rows = re.split(r'(</tr>)', h); out = []
    for r in rows:
        cells = re.split(r'(<t[dh][^>]*>.*?</t[dh]>)', r, flags=re.S); o = []
        for c in cells:
            m = re.match(r'(<t[dh][^>]*>)(.*?)(</t[dh]>)', c, re.S)
            if m and HAN.search(m.group(2)): c = m.group(1) + ruby_html(m.group(2)) + m.group(3)
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
    text = open(os.path.join(CHUAN, 'Bai%02d.md' % n), encoding='utf8').read()
    secs = parse_sections(text)
    h1 = secs[0]; m = re.match(r'^(第\d+课)\s+(.*?)\s*·\s*(Bài\s*\d+:\s*.*)$', h1['t'])
    zh_title = '%s %s' % (m.group(1), m.group(2)); vi_title = m.group(3)
    out = ['<h1>%s</h1>' % ruby_html(html.escape(zh_title)), '<p><em>%s</em></p>' % html.escape(vi_title)]
    box = None; nnote = 0; k = 1
    def close_box():
        nonlocal box, nnote
        if box is not None:
            out.append('<details class="kbn"><summary>%s</summary>%s</details>' % (box[0] % nnote if '%d' in box[0] else box[0], ''.join(box[1])))
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
        out.append('<h%d>%s</h%d>' % (lv, ht, lv))
        if body.strip(): out.append(render_blocks(strip_echo(t, split_blocks(body))))
    close_box()
    if META_BUF:
        out.append('<details class="kbn"><summary>📝 Ghi chú của dịch giả (%d)</summary><div class="kbn-i">%s</div></details>' % (len(META_BUF), render_blocks([('paragraph', x) for x in META_BUF], True)))
        META_BUF.clear()
    out.append('<hr/>')
    return '\n'.join(out), zh_title

CSS = '''/*ky-gen*/
.u3{margin:.7em 0;padding:.1em 0 .1em .8em;border-left:3px solid var(--bd)}
.u3 .zh{font-size:1.02em}
.u3 .vi{color:var(--mut);font-size:.9em;line-height:1.6;margin-top:.15em}
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
    for n in lessons:
        body, zh = gen_lesson(n)
        pat = re.compile(r'(<section data-t="[^"]*" id="s%d">)(.*?)(</section>)' % n, re.S)
        assert pat.search(ky), n
        ky = pat.sub(lambda mm: mm.group(1) + body + mm.group(3), ky, count=1)
        print('bài %d: %d ký tự HTML' % (n, len(body)))
    print('ruby: khớp pinyin md %(aligned)d khối, dùng pypinyin %(fallback)d khối' % STATS)
    new = json.dumps(ky, ensure_ascii=False).replace('<', '\\u003c')
    open(dst, 'w', encoding='utf8').write(s[:m.start(2)] + new + s[m.end(2):])

if __name__ == '__main__':
    main()
