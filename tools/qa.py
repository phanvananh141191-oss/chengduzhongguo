#!/usr/bin/env python3
"""QA S1–S12 (kế hoạch §13). Dùng: python3 tools/qa.py [v4.html] [v3.html] > reports/QA_S1_S12.md"""
import re, sys, json, collections, glob, hashlib, os
from html.parser import HTMLParser

V4 = sys.argv[1] if len(sys.argv) > 1 else 'Tong_hop_3_giao_trinh_D1_D2_KY_v4.html'
V3 = sys.argv[2] if len(sys.argv) > 2 else 'Tong_hop_3_giao_trinh_D1_D2_KY_v3_Bai11_day_du.html'
CJK = re.compile(r'[一-鿿]')
PAGE = re.compile(r'P\d+|tr\.\s*\d+|Trang\s*\d+')

def load(path):
    h = open(path, encoding='utf-8').read()
    src = {}
    for b in ('fz', 'ky', 'ld', 'kb'):
        m = re.search(r'<script type="application/json" id="src-%s">(.*?)</script>' % b, h, re.S)
        src[b] = json.loads(m.group(1)) if m else ''
    toc = json.loads(re.search(r'id="toc-data">(.*?)</script>', h, re.S).group(1))
    return h, src, toc
H4, S4, T4 = load(V4)
H3, S3, T3 = load(V3)

def kbmd(src):
    m = re.search(r'<script id="kb" type="application/json">(.*?)</script>', src, re.S)
    return json.loads(m.group(1).replace('<\\/', '</'))
KB4, KB3 = kbmd(S4['kb']), kbmd(S3['kb'])

class Doc(HTMLParser):
    """Gom theo section (fz: section.les#id; ky: h1 chia bài) các heading/văn bản/ruby/ans."""
    def __init__(s, mode):
        super().__init__(convert_charrefs=True); s.mode = mode; s.cur = None; s.d = collections.OrderedDict()
        s.hb = None; s.bn = []; s.inrt = 0; s.skip = 0; s.rubies = []; s.rt_buf = None; s.ru = None; s.bad = []
    def L(s, k): return s.d.setdefault(k, dict(h=[], text=[], ans=0, uans=0, ruby=0, rubybad=0, tbl=[], ids=set()))
    def handle_starttag(s, t, a):
        a = dict(a); cls = a.get('class', '').split()
        if t == 'section' and 'les' in cls and a.get('id'): s.cur = a['id']; s.L(s.cur)
        if t == 'h1' and s.mode == 'ky': s.cur = 'ky#%d' % (len(s.d) + 1); s.L(s.cur)
        if s.cur is None: return
        L = s.L(s.cur)
        if a.get('id'): L['ids'].add(a['id'])
        if t in ('h1', 'h2', 'h3', 'h4'): s.hb = [t, '']
        if t == 'rt': s.inrt += 1; s.rt_buf = ''
        if t == 'ruby': L['ruby'] += 1
        if t == 'div' and 'ans' in cls: L['ans'] += 1
        if t == 'textarea' and 'uans' in cls: L['uans'] += 1
        if t == 'div' and 'wr' in cls: L['uans'] += 1
        if t == 'table': L['tbl'].append([])
        if t in ('script', 'style'): s.skip += 1
    def handle_endtag(s, t):
        if s.cur is None: return
        L = s.L(s.cur)
        if s.hb and s.hb[0] == t: L['h'].append((t, re.sub(r'\s+', ' ', s.hb[1]).strip())); L['text_h'] = L.get('text_h', []) + [s.hb[1]]; s.hb = None
        if t == 'rt': s.inrt -= 1; (L.__setitem__('rubybad', L['rubybad'] + (0 if (s.rt_buf or '').strip() else 1)))
        if t in ('script', 'style'): s.skip -= 1
        if t == 'th' and L['tbl']: pass
    def handle_data(s, d):
        if s.cur is None or s.skip: return
        L = s.L(s.cur)
        if s.inrt: s.rt_buf = (s.rt_buf or '') + d; return
        if s.hb: s.hb[1] += d
        else: L['text'].append(d)
        if d.strip().startswith('Chưa có trong nguồn'): s.bn.append((s.cur, (L['h'][-1][1] if L['h'] else '')))

BN = []
def parse(html, mode):
    p = Doc(mode); p.feed(html); BN.extend(p.bn) if mode == 'fz' else None; return p.d
def norm(x): return re.sub(r'\s+', '', x)
def hz(L): return ''.join(CJK.findall(''.join(L['text'])))

out = []
def P(*a): out.append(' '.join(str(x) for x in a))
def table(head, rows):
    P('| ' + ' | '.join(head) + ' |'); P('|' + '---|' * len(head))
    for r in rows: P('| ' + ' | '.join(str(x) for x in r) + ' |')
    P('')

fz3 = parse(S3['fz'], 'fz'); BN.clear(); fz4 = parse(S4['fz'], 'fz'); BN_V4 = list(BN)
ky4 = parse(S4['ky'], 'ky'); ld3, ld4 = parse(S3['ld'], 'ld'), parse(S4['ld'], 'ld')
verdict = {}

# ---------- S1 hash-text (fz, ld: v3 ↔ v4) ----------
P('# QA S1–S12 · bản v4\n')
P('## S1 · hash-text (chữ Hán/Việt không đổi so với v3)\n')
P('Đo bằng so đa tập ký tự Hán và đa tập từ (chữ Việt) giữa v3 và v4 cho từng bài. «Mất» = có ở v3 mà không còn ở v4; «Thêm» = chỉ có ở v4 (banner, nhãn mới, 5 đoạn 《家庭学校》 của ld, bảng baked…).\n')
def words(L): return collections.Counter(re.findall(r'[^\W\d_]+', ''.join(L['text']).lower()))
rows = []; s1bad = 0
for k in fz3:
    a, b = fz3[k], fz4.get(k)
    if not b: rows.append((k, '—', '—', 'THIẾU BÀI')); s1bad += 1; continue
    ha, hb = collections.Counter(hz(a)), collections.Counter(hz(b))
    wa, wb = words(a), words(b)
    lh = sum((ha - hb).values()); ah = sum((hb - ha).values()); lw = sum((wa - wb).values()); aw = sum((wb - wa).values())
    top = ', '.join('%s×%d' % kv for kv in (wa - wb).most_common(6)); lostzh = ''.join((ha - hb).elements())
    top = ('Hán mất: ' + lostzh + ' · ' if lostzh else '') + top
    rows.append((k, 'Hán −%d/+%d' % (lh, ah), 'từ −%d/+%d' % (lw, aw), top))
    if lh: s1bad += 1
table(['fz bài', 'Hán mất/thêm', 'Việt mất/thêm', 'từ mất nhiều nhất'], rows)
rows = []
for k in ld3:
    a, b = ld3[k], ld4.get(k)
    if not b: rows.append((k, 'THIẾU', '')); continue
    lh = sum((collections.Counter(hz(a)) - collections.Counter(hz(b))).values()); lw = sum((words(a) - words(b)).values())
    rows.append((k, 'Hán mất %d' % lh, 'từ mất %d' % lw)); s1bad += (lh > 0)
if ld3: table(['ld mục', 'Hán', 'Việt'], rows[:40])
# ld là một tài liệu dữ liệu JS: so cả khối
la = collections.Counter(CJK.findall(S3['ld'])); lb = collections.Counter(CJK.findall(S4['ld']))
P('ld toàn khối: Hán mất %d, Hán thêm %d (chủ yếu do bản sao theo câu `sn` của bài đọc, và 5 đoạn 《家庭学校》 biên soạn).\n' % (sum((la - lb).values()), sum((lb - la).values())))
la = collections.Counter(CJK.findall(S3['fz'])); lb = collections.Counter(CJK.findall(S4['fz']))
verdict['S1'] = 'fz: Hán mất %d ký tự toàn khối' % sum((la - lb).values())
P('fz toàn khối: Hán mất **%d**, thêm %d.\n' % (sum((la - lb).values()), sum((lb - la).values())))
S1_ld_loss = sum((la - lb).values())
# kb: so md từng file
kbl = [k for k in KB3 if k in KB4 and KB3[k] != KB4[k]]
kbg = [k for k in KB3 if k not in KB4]
P('kb: %d/%d file đổi nội dung/thứ tự (sắp lại mục + liên kết); %d file mất; so đa tập dòng: ' % (len(kbl), len(KB3), len(kbg)), end='') if False else None
lost_lines = 0
for k in KB3:
    a = collections.Counter(l.strip() for l in KB3[k].split('\n') if l.strip())
    b = collections.Counter(l.strip() for l in KB4.get(k, '').split('\n') if l.strip())
    lost_lines += sum((a - b).values())
P('kb: %d/%d file khác bản v3 (sắp lại mục, liên kết); **dòng md bị mất: %d**; file bị mất: %d.\n' % (len(kbl), len(KB3), lost_lines, len(kbg)))
verdict['S1kb'] = lost_lines

# ---------- S2/S3 ----------
P('## S2 · thứ tự heading / S3 · bảng nhãn\n')
CANON_FZ = ['题解', '词语学习', '走进课文', '综合注释', '综合练习', '附录']
rows = []; bad2 = 0; bad3 = []
for k, L in fz4.items():
    if k in ('lg', 'lv'): continue
    h2 = [x for t, x in L['h'] if t == 'h2']
    keys = [next((c for c in CANON_FZ if x.startswith(c)), None) for x in h2]
    odd = [x for x, kk in zip(h2, keys) if kk is None]
    ks = [kk for kk in keys if kk]
    ok = ks == sorted(ks, key=CANON_FZ.index)
    miss = [c for c in CANON_FZ[:5] if c not in ks]
    rows.append((k, ' → '.join(x.split(' · ')[0] for x in h2), 'đúng' if ok and not miss and not odd else 'LỆCH: thiếu %s lạ %s' % (miss, odd)))
    if not (ok and not miss and not odd): bad2 += 1
table(['fz bài', 'h2', 'S2/S3'], rows)
verdict['S2fz'] = bad2
KY_CANON = ['PREPARE', 'EXPLORE', 'PRODUCE', '附录']
rows = []; bad2k = 0
for k, L in ky4.items():
    if not k.startswith('ky#'): continue
    h1 = ' '.join(x for t, x in L['h'] if t == 'h1')[:20]
    if not re.match(r'第\s*\d+\s*课', h1): continue
    h2 = [x for t, x in L['h'] if t == 'h2']
    ks = [next((c for c in KY_CANON if x.startswith(c)), None) for x in h2]
    ok = ks == [c for c in KY_CANON if c in ks] and None not in ks and len(ks) >= 4
    rows.append((h1, ' → '.join(x.split(' ')[0] for x in h2), 'đúng' if ok else 'LỆCH'))
    bad2k += (not ok)
table(['ky bài', 'h2', 'S2'], rows)
verdict['S2ky'] = bad2k
# nhãn bài tập ky A–G: Hán trước
exl = []
for k, L in ky4.items():
    for t, x in L['h']:
        if t == 'h4' and re.match(r'^[A-H]\s', x) and not CJK.search(x): exl.append((k, x))
P('ky: nhãn bài tập A–H không có Hán: %d %s\n' % (len(exl), exl[:5]))
verdict['S3ky'] = len(exl)
# kb thứ tự mục
kbbad = []
for i in range(1, 13):
    t = KB4.get('lessons/%02d.md' % i, '')
    nums = [m.group(1) for m in re.finditer(r'^## (\d+)\. ', t, re.M)]
    ap = [m.group(1) for m in re.finditer(r'^## (Phụ lục [AB])', t, re.M)]
    if nums != [str(n) for n in range(1, 11)] or ap != ['Phụ lục A', 'Phụ lục B']: kbbad.append((i, nums, ap))
P('kb lessons: thứ tự 1…10 → Phụ lục A → Phụ lục B: %s\n' % ('đúng 12/12' if not kbbad else 'LỆCH %s' % kbbad))
verdict['S2kb'] = len(kbbad)

# ---------- S4 vocab-schema ----------
P('## S4 · vocab-schema (fz)\n')
class TH(HTMLParser):
    def __init__(s): super().__init__(); s.les = None; s.tabs = []; s.cur = None; s.th = None; s.rows = 0; s.row = None
    def handle_starttag(s, t, a):
        a = dict(a)
        if t == 'section' and 'les' in a.get('class', '').split(): s.les = a.get('id')
        if t == 'table': s.cur = dict(les=s.les, th=[], rows=0, cells=collections.Counter(), cls=a.get('class', ''))
        if t == 'th' and s.cur: s.th = ''
        if t == 'tr' and s.cur: s.cur['rows'] += 1
    def handle_endtag(s, t):
        if t == 'th' and s.cur is not None and s.th is not None: s.cur['th'].append(s.th.strip()); s.th = None
        if t == 'table' and s.cur: s.tabs.append(s.cur); s.cur = None
    def handle_data(s, d):
        if s.th is not None: s.th += d
th = TH(); th.feed(S4['fz'])
STD = ['#', '词', 'Pinyin', '词性', 'Hán-Việt', 'Nghĩa', 'English', '例句']
def idx(h):
    h = h.lower()
    for i, k in enumerate(['#', '词性', 'pinyin', '词', 'hán', 'nghĩa', 'english', '例']):
        if h.startswith(k.lower()) or (k == '词' and h.startswith('từ')): return {'#':0,'词':1,'pinyin':2,'词性':3,'hán':4,'nghĩa':5,'english':6,'例':7}[k]
    return 99
rows = []; bad4 = 0
for t in th.tabs:
    if len(t['th']) >= 4 and any('Pinyin' in x for x in t['th']):
        ix = [idx(x) for x in t['th']]
        ok = ix == sorted(ix) and 99 not in ix
        if not ok: bad4 += 1; rows.append((t['les'], ' | '.join(t['th'])))
P('Bảng từ nhận diện: %d; sai thứ tự cột/nhãn lạ: **%d**\n' % (sum(1 for t in th.tabs if len(t['th']) >= 4 and any('Pinyin' in x for x in t['th'])), bad4))
if rows: table(['bài', 'cột'], rows[:30])
empty_cols = 0
verdict['S4'] = bad4

# ---------- S5 ----------
P('## S5 · answers-coverage (fz)\n')
rows = []; bad5 = 0
for k, L in fz4.items():
    if k == 'l1' and L['uans'] - L['ans'] == 1: P('l1: lệch 1 có lý do — khung viết 八 课本剧 (`.wr`, ghi bài viết riêng) không có khối đáp án.\n'); continue
    if L['ans'] != L['uans']: bad5 += 1; rows.append((k, L['ans'], L['uans'], 'lệch %d' % abs(L['ans'] - L['uans'])))
P('Bài có số `.ans` ≠ `.uans`: **%d** / %d\n' % (bad5, len(fz4)))
if rows: table(['bài', '.ans', '.uans', ''], rows)
tot_ans = sum(L['ans'] for L in fz4.values()); tot_u = sum(L['uans'] for L in fz4.values())
P('Tổng .ans %d · .uans %d\n' % (tot_ans, tot_u)); verdict['S5'] = bad5

# ---------- S6 ruby ----------
P('## S6 · ruby-valid\n')
rows = []; tot_bad = 0
for nm, dd in (('fz', fz4), ('ky', ky4), ('ld', ld4)):
    r = sum(L['ruby'] for L in dd.values()); b = sum(L['rubybad'] for L in dd.values()); tot_bad += b
    rows.append((nm, r, b))
table(['sách', '<ruby> tĩnh', '<rt> rỗng'], rows)
# ruby: số chữ Hán vs số âm tiết ở ky
bad_len = 0; ex = []
for m in re.finditer(r'<ruby>([^<]*)<rt>([^<]*)</rt></ruby>', S4['ky']):
    zh, py = m.group(1), m.group(2)
    if len(zh) > 1 and CJK.search(zh) and len(py.split()) not in (1, len(zh)): bad_len += 1; ex.append((zh, py))
P('ky: ruby có nhiều chữ nhưng số âm tiết lệch: %d %s\n' % (bad_len, ex[:5])); verdict['S6'] = tot_bad + bad_len
# ruby lồng nhau / chữ Hán không ruby trong ky
nested = len(re.findall(r'<ruby>[^<]*<rt>[^<]*<ruby>', S4['ky']))
P('ky: ruby lồng nhau: %d\n' % nested); verdict['S6'] += nested

# ---------- S7 md ↔ ky ----------
P('## S7 · md-html-diff (md chuẩn ↔ ky)\n')
def ky_lesson_text(n):
    L = ky4.get('ky#%d' % (n + 2))  # h1 mở đầu + 2 h3? tìm theo h1 chứa 第n课
    for k, L in ky4.items():
        h1 = ' '.join(x for t, x in L['h'] if t == 'h1')
        if re.match(r'第\s*%d\s*课' % n, h1): return norm(''.join(L['text']) + ''.join(L.get('text_h', [])))
    return ''
rows = []; tot_miss = 0
for n in range(1, 13):
    md = open('nguon_md_ky/chuan/Bai%02d.md' % n, encoding='utf-8').read()
    # bỏ lớp ghi chú KB
    md = re.split(r'\n#{2,4}\s*(?:Ghi chú sắc thái|Những từ dễ dịch)', md)[0] if False else md
    htm = ky_lesson_text(n)
    segs = []
    for line in md.split('\n'):
        if re.match(r'\s*\|?\s*[-:| ]+\|?\s*$', line) or line.startswith('#'): continue
        if re.search(r'Ghi chú sắc thái|dễ dịch lệch|📝', line): continue
        for part in re.split(r'[，。！？；：、,.!?;:\s“”"‘’（）()《》—…·|*_`>\-]+', line):
            z = ''.join(CJK.findall(part))
            if len(z) >= 5: segs.append(z)
    htmz = ''.join(CJK.findall(htm))
    miss = [z for z in segs if z not in htmz]
    rows.append((n, len(segs), len(miss), ' / '.join(miss[:2])[:60]))
    tot_miss += len(miss)
table(['bài', 'đoạn Hán ≥5 trong md', 'không thấy trong ky', 'ví dụ'], rows)
verdict['S7'] = tot_miss

# ---------- S8 note-hash ----------
P('## S8 · note-hash (ghi chú md chuẩn ↔ KB)\n')
rows = []; bad8 = 0
for n in range(1, 13):
    md = open('nguon_md_ky/chuan/Bai%02d.md' % n, encoding='utf-8').read()
    kb = KB4.get('lessons/%02d.md' % n, '')
    kbn = norm(kb)
    blocks = re.findall(r'^#{2,6}\s*(?:📝\s*)?(?:Ghi chú sắc thái[^\n]*|Những từ dễ dịch lệch[^\n]*)\n(.*?)(?=^#{1,6}\s|\Z)', md, re.S | re.M)
    miss = 0
    for b in blocks:
        for line in b.split('\n'):
            l = norm(re.sub(r'[*_`>|-]', '', line))
            if len(l) >= 12 and l[:40] not in re.sub(r'[*_`>|-]', '', kbn): miss += 1
    rows.append((n, len(blocks), miss)); bad8 += miss
table(['bài', 'khối ghi chú trong md', 'dòng không thấy trong KB'], rows)
P('(Ghi chú chỉ ở KB, ky chỉ liên kết sang KB theo quyết định mục 7; không dựng hộp gập nên so khối md chuẩn với KB.)\n'); verdict['S8'] = bad8

# ---------- S9 key audit ----------
P('## S9 · key-audit\n')
M = {}
sys.path.insert(0, 'tools')
from rekey import mapping
M = mapping()
keys_new = set(); keys_all = []
def walk(o):
    if isinstance(o, dict):
        if 'key' in o and isinstance(o['key'], str): keys_all.append(o['key'])
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(T4)
bad_old = [k for k in M if k in keys_all and M[k] != k]
P('Key mục lục: %d; còn key cũ trong mục lục: %d; alias đủ: %d/%d.\n' % (len(keys_all), len(bad_old), sum(1 for v in M.values() if v in keys_all), len(M)))
# liên kết nội bộ → key + anchor
ids = {'fz': set(), 'ky': set(), 'ld': set()}
for nm, dd in (('fz', fz4), ('ky', ky4)):
    for L in dd.values(): ids[nm] |= L['ids']
kbids = set()
refs = collections.Counter(); unresolved = collections.Counter(); badanchor = collections.Counter()
allkeys = set(keys_all) | set(M)
for nm in ('fz', 'ky'):
    for m in re.finditer(r'(?:data-(?:go|href|k|xl|kb)|href)="(?:#)?((?:fz|ky|kb|ld):[^"]+)"', S4[nm]):
        refs[m.group(1)] += 1
for nm in ('fz', 'ky', 'kb', 'ld'):
    for m in re.finditer(r'"((?:fz|ky|kb|ld):[A-Za-z0-9_\-./]+)(?:::([^"]+))?"', S4[nm]): refs[m.group(1) + ('::' + m.group(2) if m.group(2) else '')] += 1
for r, c in refs.items():
    key, _, an = r.partition('::')
    if key not in allkeys: unresolved[key] += c; continue
P('Điểm tham chiếu nội bộ dạng key: %d (khác nhau); không phân giải được: **%d** %s\n' % (len(refs), len(unresolved), list(unresolved)[:8]))
# kiểm anchor ky/fz tồn tại
miss_an = []
for r in refs:
    key, _, an = r.partition('::')
    if an:
        bk = key.split(':')[0]
        if bk in ids and an not in ids[bk] and not an.startswith('kbh'): miss_an.append(r)
P('Anchor `::id` trỏ vào id không có trong khung đích: **%d** %s\n' % (len(miss_an), miss_an[:8]))
# _kymap
ky_map = json.load(open('tools/_kymap.json'))
miss_ky = 0; tot_ky = 0
def chk(o):
    global miss_ky, tot_ky
    if isinstance(o, str):
        if re.match(r's\d+-', o):
            tot_ky += 1
            if o not in ids['ky']: miss_ky += 1
    elif isinstance(o, dict):
        for v in o.values(): chk(v)
    elif isinstance(o, list):
        for v in o: chk(v)
chk(ky_map)
P('Bản đồ ky↔KB: %d tham chiếu ky; id ky không tồn tại: %d\n' % (tot_ky, miss_ky))
verdict['S9'] = len(bad_old) + len(unresolved) + len(miss_an) + miss_ky
# localStorage keys in shell
P('Mọi `localStorage.*` ở khung ngoài: `u3-set`, `u3-last`, `u3xb:*` (đã migrate, S9 e2e đã chạy ở P8).\n')

# ---------- S10 ----------
P('## S10 · page-number-in-heading\n')
rows = []; tot10 = 0
for nm, dd in (('fz', fz4), ('ky', ky4), ('ld', ld4)):
    c = sum(1 for L in dd.values() for t, x in L['h'] if PAGE.search(x)); tot10 += c; rows.append((nm, c))
kbc = sum(1 for t in KB4.values() for l in t.split('\n') if l.startswith('#') and PAGE.search(l)); tot10 += kbc; rows.append(('kb (md)', kbc))
table(['sách', 'heading còn số trang'], rows)
verdict['S10'] = tot10

# ---------- S11 ----------
P('## S11 · placeholder-check (banner «chưa có trong nguồn»)\n')
rows = list(BN_V4)
table(['bài', 'đứng dưới mục'], rows)
P('Số banner: %d. Theo mục 3.9 dự kiến: bài 2 题解, bài 4 走进课文, bài 8 题解/走进课文, bài 6 «Trang 100».\n' % len(rows))
verdict['S11'] = '%d banner (xem bảng)' % len(rows)

# ---------- verdict ----------
P('## Tổng kết\n')
table(['mã', 'kết quả'], [(k, v) for k, v in verdict.items()])
print('\n'.join(out))
