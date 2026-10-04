#!/usr/bin/env python3
"""P2: chuẩn hoá 12 file md của ky về một mẫu heading (xem reports/P2_anh_xa_heading_ky.md).

Chỉ sửa dòng heading (đổi cấp, đổi nhãn, thêm tiêu đề cho chỗ bị gộp, gom mục trùng).
Dòng thân văn bản không bị sửa; script kiểm tra bất biến này (S1) và ghi báo cáo.
Dùng: python3 tools/normalize_ky_md.py   → nguon_md_ky/chuan/BaiNN.md + reports/P2_ket_qua_chuan_hoa.md
"""
import re, os, sys, json, zipfile, collections, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'nguon_md_ky')
OUT = os.path.join(SRC, 'chuan')
KB = os.path.join(OUT, '_kb')
os.makedirs(KB, exist_ok=True)

FILES = {1: 'Bai01_ban_dich_song_ngu_hoan_chinh.docx', 2: 'Bai02_dich_song_ngu.md', 3: 'Bai03_ban_dich_song_ngu_day_du.md',
         4: 'Bai04_TronBo.md', 5: 'Bai05_TongHop_SongNgu.md', 6: 'Bai06_TongHop_SongNgu.md', 7: 'Bai07_Tong_hop_day_du.md',
         8: 'Bai08_Tong_hop_day_du.md', 9: 'Bai09_song_ngu_day_du.md', 10: 'Bai10_TONG_HOP_song_ngu.md',
         11: 'Bai11_toan_bo_song_ngu.md', 12: 'Bai12_ban_dich_song_ngu_day_du.md'}
# Tiêu đề Hán lấy từ h1 của HTML ky hiện có (bài nào md không có)
HAN = {1: '友谊的小船要远行', 2: '我想去旅游', 3: '话说“相亲”', 4: '生，还是不生？', 5: '宠物大家谈', 6: '健康最重要',
       7: '今天你晒了没有？', 8: '闲话“瘾”', 9: '共享的生活', 10: '人工智能改变生活', 11: '卡主还是卡奴？', 12: '夜经济，夜生活'}

# ---------------------------------------------------------------- docx → md (bài 1)
def docx_to_md(path):
    x = zipfile.ZipFile(path).read('word/document.xml').decode('utf8')
    body = x[x.index('<w:body>'):]
    def runs(p):
        out = ''
        for r in re.findall(r'<w:r[ >].*?</w:r>', p, re.S):
            b = '<w:b/>' in r or '<w:b ' in r; i = '<w:i/>' in r or '<w:i ' in r
            t = ''.join(re.findall(r'<w:t[^>]*>(.*?)</w:t>', r, re.S))
            t = t.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&apos;', "'")
            if '<w:br/>' in r: t += '\\\n'
            if t.strip() and b: t = '**' + t + '**'
            if t.strip() and i: t = '*' + t + '*'
            out += t
        return out
    lines = []
    pos = 0
    toks = re.finditer(r'<w:tbl>.*?</w:tbl>|<w:p[ >].*?</w:p>', body, re.S)
    for m in toks:
        s = m.group(0)
        if s.startswith('<w:tbl>'):
            rows = []
            for tr in re.findall(r'<w:tr[ >].*?</w:tr>', s, re.S):
                cells = [' '.join(runs(p) for p in re.findall(r'<w:p[ >].*?</w:p>', tc, re.S)).replace('\n', ' ').replace('|', '\\|')
                         for tc in re.findall(r'<w:tc>.*?</w:tc>', tr, re.S)]
                rows.append('| ' + ' | '.join(c.strip() for c in cells) + ' |')
            if rows:
                lines.append(rows[0]); lines.append('| ' + ' | '.join([':--'] * (rows[0].count('|') - 1)) + ' |'); lines += rows[1:]
                lines.append('')
            continue
        st = re.search(r'<w:pStyle w:val="([^"]+)"', s); st = st.group(1) if st else ''
        t = runs(s).strip()
        if not t: lines.append(''); continue
        lv = {'Title': 1, 'Heading1': 1, 'Heading2': 2, 'Heading3': 3}.get(st)
        if lv:
            t = re.sub(r'\*', '', t); lines.append('#' * lv + ' ' + t); lines.append('')
        elif st == 'ListParagraph': lines.append('- ' + t)
        else: lines.append(t); lines.append('')
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)) + '\n'

# ---------------------------------------------------------------- phân tích heading
HRE = re.compile(r'^(#{1,6})\s+(.*?)\s*$')
def parse(text):
    """→ (preamble_lines, [ {lv, t, body[list of lines]} ])"""
    pre = []; blocks = []; fence = False; cur = None
    for ln in text.split('\n'):
        if ln.strip().startswith('```'): fence = not fence
        m = None if fence else HRE.match(ln)
        if m:
            cur = dict(lv=len(m.group(1)), t=m.group(2), body=[]); blocks.append(cur)
        else:
            (cur['body'] if cur else pre).append(ln)
    return pre, blocks

def role(t):
    s = t.strip()
    if re.match(r'^Mục lục\b', s): return 'DROP'
    if re.match(r'^(Bài\s*\d+\s*·\s*Phần|PHẦN\s*\d)', s, re.I): return 'DROP'
    if re.match(r'^Tổng kết', s): return 'DROP'              # bỏ hẳn (người dùng chốt)
    if re.match(r'^(Phụ lục tổng hợp|Tổng hợp các chỗ Lưu ý)', s): return 'KB'
    if re.match(r'^Ghi chú sắc thái', s): return 'NOTE1'
    if re.match(r'^Những từ dễ dịch lệch', s): return 'NOTE2'
    if re.match(r'^Bài tập và (hội thoại|bài đọc)\s*$', s): return 'WRAP'
    if re.match(r'^Bảng tên nhân vật', s): return 'CHARS'
    if re.match(r'^Bài\s*\d+\s*[:：]', s): return 'TITLE'
    if re.match(r'^PREPARE', s): return 'PREPARE'
    if re.match(r'^EXPLORE', s): return 'EXPLORE'
    if re.match(r'^促成\s*·\s*对话', s) or re.match(r'^促成\s*·\s*段话', s): return 'S_DIALOG'
    if re.match(r'^促成\s*·\s*拓展', s): return 'S_EXT'
    if re.match(r'^PRODUCE', s): return 'PRODUCE'
    if re.match(r'^评价', s): return 'EVAL'
    if re.match(r'^附录', s): return 'APPX'
    if re.match(r'^(录音文本|Bản ghi âm)', s): return 'AUDIO'
    if s.startswith('🎧'): return 'TRACK'
    if re.match(r'^📝\s*参考答案', s): return 'ANSWERS'
    if re.match(r'^(Mở đầu|Đoạn mở đầu|Giới thiệu và câu hỏi mở đầu|Câu hỏi mở đầu)\s*$', s): return 'OPEN'
    if re.match(r'^牛刀小试', s): return 'NIUDAO'
    if re.match(r'^学习目标', s): return 'GOALS'
    if re.match(r'^(Hoạt động và mục tiêu)', s): return 'ACTGOAL'
    if re.match(r'^(任务支持|Hỗ trợ (làm )?(nhiệm vụ|bài tập)|Hỗ trợ thực hiện)', s): return 'TSUPPORT'
    if re.match(r'^(任务选择|Lựa chọn (nhiệm vụ|bài tập))', s): return 'TCHOOSE'
    if re.match(r'^(任务[一二三四五六七八九十]|Nhiệm vụ\s*(một|hai|ba|\d))', s): return 'TASK'
    if re.search(r'词语表|Bảng từ (vựng|ngữ)', s): return 'VOCAB'
    if re.match(r'^(Bài tập\s+)?[A-H](\s|\.|:|：|–|-|$)', s) and not re.match(r'^[A-H][\d\.]\d', s): return 'EX'
    return 'OTHER'

# ---------------------------------------------------------------- tách thân theo mẫu «**中文：** / A 听…»
CN_EX = re.compile(r'^\s*([A-H])\s+[\u4e00-\u9fff（(]')
CN_TASK = re.compile(r'^\s*任务([一二三])[\s　]')

def split_body(body, kind):
    """Chia thân thành các đoạn khi gặp nhãn Hán «A 听录音…» (kind='EX') hoặc «任务一　…» (kind='TASK')
    đứng ngay sau dòng **中文：**. Trả [(nhãn, dòng_Hán, [dòng...]), ...]; đoạn đầu có nhãn None."""
    pat = CN_EX if kind == 'EX' else CN_TASK
    out = [(None, None, [])]; i = 0
    while i < len(body):
        ln = body[i]
        nxt = None
        if re.match(r'^\*\*中文[:：]\*\*', ln.strip()):
            j = i + 1
            while j < len(body) and not body[j].strip(): j += 1
            if j < len(body):
                m = pat.match(body[j])
                if m: nxt = (m.group(1), body[j].strip().rstrip('\\').strip(), i)
        if nxt:
            out.append((nxt[0], nxt[1], [])); out[-1][2].append(ln)
        else:
            out[-1][2].append(ln)
        i += 1
    return out


M_LAB = re.compile(r'^\*\*中文[:：]\*\*\s*\\?\s*$')
def _clean(x):
    return x.replace('**', '').strip().rstrip('\\').strip()

def cand(lines, i):
    """Nếu dòng i (hoặc dòng sau dòng **中文：**) là nhãn Hán của bài tập/nhiệm vụ/bảng từ → (kind, nhãn, chỉ_số_dòng_nhãn)."""
    ln = lines[i].strip(); j = i; has_cn = False
    if re.match(r'^\*\*中文[:：]\*\*', ln):
        has_cn = True
        rest = _clean(re.sub(r'^\*\*中文[:：]\*\*', '', ln))
        if not rest:
            j = i + 1
            while j < len(lines) and not lines[j].strip(): j += 1
            if j >= len(lines): return None
            rest = _clean(lines[j])
    else:
        if not ln.startswith('**'): return None
        rest = _clean(ln)
    if re.match(r'^[A-H]\s+[\u4e00-\u9fff（(]', rest): return ('EX', rest.rstrip('。').strip(), j)
    if re.match(r'^任务[一二三][\s　]', rest): return ('TASK', rest, j)
    if has_cn and rest.startswith('词语表'): return ('VOC', rest, j)
    return None

def marker(lines, i):
    c = cand(lines, i)
    if not c: return None
    kind, label, j = c
    vie = ''
    for k in range(i, min(i + 9, len(lines))):
        mv = re.match(r'^\*\*Tiếng Việt:\*\*\s*\\?\s*(.*)$', lines[k].strip())
        if mv:
            vie = mv.group(1).strip().rstrip('\\').strip()
            if not vie:
                for q in range(k + 1, min(k + 3, len(lines))):
                    if lines[q].strip(): vie = lines[q].strip().rstrip('\\').strip(); break
            break
    return kind, label, vie, j

def explode(blocks, flags):
    res = []
    for b in blocks:
        r = role(b['t']); lines = b['body']
        cuts = []; consumed = set()
        first_nb = next((i for i, l in enumerate(lines) if l.strip()), None)
        for i in range(len(lines)):
            if i in consumed: continue
            mk = marker(lines, i)
            if not mk: continue
            consumed.update(range(i, mk[3] + 1))
            if i == first_nb and r in ('EX', 'VOCAB', 'TASK'): continue
            cuts.append((i, mk[:3]))
        if not cuts or r in ('DROP', 'KB', 'NOTE1', 'NOTE2'):
            res.append(b); continue
        res.append(dict(lv=b['lv'], t=b['t'], body=lines[:cuts[0][0]]))
        for (i, mk), nxt in zip(cuts, cuts[1:] + [(len(lines), None)]):
            kind, han, vie = mk
            if kind == 'EX':
                vie2 = re.sub(r'^[A-H]\s*[\.:：]\s*', '', vie).strip()
                t = han + (' (' + vie2 + ')' if vie2 else '')
            elif kind == 'VOC':
                t = han + (' (' + vie + ')' if vie else '')
            else:
                t = han
            flags.append('tiêu đề «%s» được chèn từ nhãn Hán trong thân (nguồn không có heading) — cần duyệt' % han)
            res.append(dict(lv=b['lv'] + 1, t=t, body=lines[i:nxt[0]], synthetic=True))
    return res

# ---------------------------------------------------------------- chuẩn hoá một bài
def vie_part(t):
    t = re.sub(r'^(Bài tập\s+)?[A-H]\s*[\.:：–-]*\s*', '', t.strip())
    return t.strip(' :.')

def han_from_body(body, pat):
    nb = [i for i, l in enumerate(body[:14]) if l.strip()]
    for i in nb:
        c = cand(body, i)
        if c and pat.match(c[1]): return c[1]
    return None

def code_of(t, body, n, sub):
    m = re.search(r'\b%d-\d(?:-\d)?\b' % n, t)
    return m.group(0) if m else None

def normalize(n, text):
    pre, bl = parse(text)
    out = []; flags = []; dropped = []; kbout = []
    gone = collections.Counter()
    bl = explode(bl, flags)
    def _cl(t): return t.replace('**', '').replace('  ', ' ').strip()
    emit = lambda lv, t, body=None: (out.append('#' * lv + ' ' + _cl(t)), out.append('') if body is None else None, out.extend(body or []))
    # tiêu đề h1
    title_vi = None
    for b in bl:
        m = re.match(r'^Bài\s*%d\s*[:：]\s*(.*)$' % n, b['t'])
        if m and role(b['t']) == 'TITLE' and 'Tiêu đề' not in b['t']:
            title_vi = re.sub(r'[\s·]*(Bản dịch.*)$', '', m.group(1)).strip()
            break
    if not title_vi:
        for b in bl:
            if role(b['t']) == 'TITLE':
                title_vi = re.sub(r'\s*·.*$', '', b['t'].split(':', 1)[1]).strip(); break
    # lấy Việt từ dòng **Tiếng Việt:** Bài n: … nếu có
    for b in bl:
        if role(b['t']) == 'TITLE':
            txt = '\n'.join(b['body'])
            mm = re.search(r'\*\*Tiếng Việt:\*\*\s*\\?\s*\n?\s*Bài\s*%d\s*[:：]\s*(.+)' % n, txt)
            if mm: title_vi = mm.group(1).strip().rstrip('.\\ ').strip()
            break
    out.append('# 第%d课 %s · Bài %d: %s' % (n, HAN[n], n, title_vi or '?'))
    out.append('')
    pre_txt = [l for l in pre if l.strip()]
    if pre_txt:
        out.extend(pre); flags.append('phần trước heading đầu tiên được giữ dưới h1 (%d dòng)' % len(pre_txt))

    # thứ tự: tiêu đề bài trước, rồi bảng nhân vật
    chars = [b for b in bl if role(b['t']) == 'CHARS']
    titles = [b for b in bl if role(b['t']) == 'TITLE' and 'Bản dịch' not in b['t'] and not b['t'].startswith('Bài %d ·' % n) and not re.match(r'^Bài\s*\d+\s*:\s*\S.*·', b['t'])]
    used = set()
    h1_like = [b for b in bl if b['lv'] == 1 and role(b['t']) in ('TITLE', 'OTHER') and b is bl[0]]
    for b in titles:
        if id(b) in used: continue
        used.add(id(b)); emit(2, 'Tiêu đề bài', b['body'])
    for b in chars:
        used.add(id(b)); emit(2, 'Bảng tên nhân vật', b['body'])
    # bỏ khối h1/title đầu file đã chuyển vào h1 (nếu có thân trống)
    first = bl[0] if bl else None
    state = dict(phase=None, sub=None, ex_orig=None, last_ex=None, seen_ex_h4=False, emitted=set())
    stack = []  # (orig_lv, out_lv)
    def sup(lv):
        return lv
    def push(orig, outlv):
        while stack and stack[-1][0] >= orig: stack.pop()
        stack.append((orig, outlv))
    def child_level(orig):
        while stack and stack[-1][0] >= orig: stack.pop()
        if not stack: return None
        return stack[-1][1] + (orig - stack[-1][0])
    swallow = {}   # id(block) -> 'KB' | 'DROP' cho các heading con của mục bị gom/bỏ
    k = 0
    while k < len(bl):
        rr = role(bl[k]['t'])
        if rr == 'KB' or (rr == 'DROP' and not re.match(r'^(Bài\s*\d+\s*·\s*Phần|PHẦN\s*\d)', bl[k]['t'], re.I)):
            j = k + 1
            while j < len(bl) and bl[j]['lv'] > bl[k]['lv']:
                swallow[id(bl[j])] = (rr, bl[k]); j += 1
        k += 1
    for k, b in enumerate(bl):
        if id(b) in used: continue
        r = role(b['t']); t = b['t']; body = b['body']; lv = b['lv']
        if id(b) in swallow:
            kind, parent = swallow[id(b)]
            for l in body:
                if l.strip(): gone[l.strip()] += 1
            if kind == 'KB': kbout.append('#' * max(b['lv'] - parent['lv'] + 1, 2) + ' ' + t + '\n' + '\n'.join(body))
            else: dropped.append((t, sum(len(x) for x in body)))
            continue
        if b is first and lv == 1 and r in ('TITLE', 'OTHER'):
            # tiêu đề file: chỉ giữ thân nếu có chữ
            if any(x.strip() for x in body): out.extend(body)
            continue
        if r == 'DROP':
            if re.match(r'^(Bài\s*\d+\s*·\s*Phần|PHẦN\s*\d)', t, re.I):
                if any(x.strip() for x in body):
                    out.extend(body); flags.append('thân của dấu «%s» được giữ nguyên (chỉ bỏ dòng tiêu đề)' % t[:40])
                continue
            for l in body:
                if l.strip(): gone[l.strip()] += 1
            dropped.append((t, sum(len(x) for x in body))); continue
        if r == 'WRAP':
            out.extend(body); flags.append('tiêu đề bọc «%s» bị bỏ, thân giữ nguyên' % t); continue
        if r == 'KB':
            for l in body:
                if l.strip(): gone[l.strip()] += 1
            kbout.append('# %s\n' % t + '\n'.join(body)); continue
        if r in ('NOTE1', 'NOTE2'):
            label = '📝 ' + re.sub(r'^📝\s*', '', t)
            emit(4, label, body); continue
        if state['phase'] == 'APPX' and r in ('S_DIALOG', 'S_EXT', 'EVAL', 'EX', 'VOCAB', 'TASK'):
            emit(4, t, body); continue
        if r == 'PREPARE':
            state.update(phase='PREPARE', sub=None); emit(2, 'PREPARE · 驱动 (Khởi động)', body); stack[:] = [(lv, 2)]; continue
        if r == 'EXPLORE':
            if 'EXPLORE' not in state['emitted']:
                emit(2, 'EXPLORE · 促成 (Khám phá)', body); state['emitted'].add('EXPLORE'); stack[:] = [(lv, 2)]
            else:
                out.extend(body)
            state['phase'] = 'EXPLORE'
            if re.search(r'拓展', t): state['sub'] = 'EXT'; r2 = 'S_EXT'
            elif re.search(r'对话', t): state['sub'] = 'DIALOG'; r2 = 'S_DIALOG'
            else: r2 = None
            if r2 and ('S_' + state['sub']) not in state['emitted'] and not (k + 1 < len(bl) and role(bl[k + 1]['t']) == r2):
                lab = '促成 · 对话 (Hội thoại)' if r2 == 'S_DIALOG' else '促成 · 拓展 (Mở rộng)'
                emit(3, lab, []); state['emitted'].add('S_' + state['sub']); stack.append((lv + 1, 3))
            continue
        if r in ('S_DIALOG', 'S_EXT'):
            state['phase'] = 'EXPLORE'; state['sub'] = 'DIALOG' if r == 'S_DIALOG' else 'EXT'
            key = 'S_' + state['sub']
            if 'EXPLORE' not in state['emitted']:
                emit(2, 'EXPLORE · 促成 (Khám phá)', []); state['emitted'].add('EXPLORE')
            if key not in state['emitted']:
                lab = ('促成 · 对话 (Hội thoại)' if r == 'S_DIALOG' else '促成 · 拓展 (Mở rộng)')
                if re.match(r'^促成\s*·\s*段话', t): lab = '促成 · 段话 (Đoạn văn)'
                emit(3, lab, body); state['emitted'].add(key)
            else:
                out.extend(body); flags.append('mục trùng tiêu đề «%s» được gộp vào mục trước' % t)
            state['last_ex'] = None; stack[:] = [(2, 2), (lv, 3)]; continue
        if r == 'PRODUCE':
            state['phase'] = 'PRODUCE'; state['sub'] = None; emit(2, 'PRODUCE · 产出 (Sản xuất)', body); stack[:] = [(lv, 2)]; continue
        if r == 'EVAL':
            state['phase'] = 'PRODUCE'; state['sub'] = 'EVAL'; emit(3, '评价 (Tự đánh giá)', body); stack[:] = [(2, 2), (lv, 3)]; continue
        if r == 'APPX':
            state['phase'] = 'APPX'; state['sub'] = None
            emit(2, '附录 · 录音文本 (Bài nghe)', body); stack[:] = [(lv, 2)]
            state['appx_audio'] = False; continue
        if state['phase'] == 'APPX':
            if r == 'AUDIO':
                emit(3, '录音文本 (Bản ghi âm)', body); state['appx_audio'] = True; stack[:] = [(2, 2), (lv, 3)]; continue
            if r == 'ANSWERS':
                emit(3, t, body); stack[:] = [(2, 2), (lv, 3)]; state['appx_audio'] = False; state['in_ans'] = True; continue
            if r == 'TRACK':
                if not state['appx_audio'] and not state.get('in_ans'):
                    emit(3, '录音文本 (Bản ghi âm)', []); state['appx_audio'] = True
                emit(4, t, body); stack[:] = [(2, 2), (3, 3), (lv, 4)]; continue
            if state.get('in_ans'):
                emit(4, t, body); continue
            emit(3, t, body); stack[:] = [(2, 2), (lv, 3)]; continue
        if state['phase'] == 'PREPARE':
            if r == 'OPEN': emit(3, 'Mở đầu', body); stack[:] = [(2, 2), (lv, 3)]; continue
            if r == 'NIUDAO': emit(3, '牛刀小试 (Thử sức bước đầu)', body); stack[:] = [(2, 2), (lv, 3)]; continue
            if r == 'GOALS': emit(3, '学习目标 (Mục tiêu học tập)', body); stack[:] = [(2, 2), (lv, 3)]; continue
            if r == 'ACTGOAL': emit(3, 'Hoạt động và mục tiêu', body); stack[:] = [(2, 2), (lv, 3)]; continue
            cl = child_level(lv)
            if r == 'EX' or (re.match(r'^[AB]\s*[\u4e00-\u9fff]', t)):
                han = han_from_body(body, re.compile(r'^[AB]\s'))
                emit(4, han or t, body); continue
            emit(max(cl or 3, 3), t, body); continue
        if state['phase'] == 'PRODUCE' and state['sub'] != 'EVAL':
            if r == 'TSUPPORT': emit(3, '任务支持 (Hỗ trợ nhiệm vụ)', body); state['sub'] = 'TS'; stack[:] = [(2, 2), (lv, 3)]; continue
            if r == 'TCHOOSE':
                emit(3, '任务选择 (Lựa chọn nhiệm vụ)', body); state['sub'] = 'TC'; stack[:] = [(2, 2), (lv, 3)]
                emit_tasks(out, flags, body, n); continue
            if r == 'TASK':
                han = han_from_body(body, re.compile(r'^任务[一二三]'))
                vi = t
                lab = ('%s (%s)' % (han, vi)) if han and not t.startswith('任务') else (t if t.startswith('任务') else vi)
                emit(4, lab, body); stack[:] = [(2, 2), (3, 3), (lv, 4)]; continue
            cl = child_level(lv) or 3
            emit(max(cl, 3), t, body); continue
        if state['phase'] == 'PRODUCE' and state['sub'] == 'EVAL':
            emit(4, t, body); continue
        # ---- EXPLORE
        if state['phase'] == 'EXPLORE' and state['sub'] in ('DIALOG', 'EXT'):
            sub = state['sub']
            if r == 'VOCAB':
                m = re.search(r'\b%d-\d\b' % n, t)
                code = m.group(0) if m else '%d-%d' % (n, 1 if sub == 'DIALOG' else 3)
                emit(4, '词语表 %s 🔊 (Bảng từ vựng)' % code, body); state['last_ex'] = 'VOCAB'; stack[:] = [(2, 2), (3, 3), (lv, 4)]; continue
            if r == 'EX' or r == 'OTHER' or r == 'TITLE':
                is_num = bool(re.match(r'^(\d+\.|Hội thoại\s*\d)', t.strip()))
                if is_num:
                    if state['last_ex'] in ('EX', 'TEXT'):
                        emit(5, t, body); split_inline(out, flags, body, n); continue
                    emit(4, '对话文本 (Văn bản hội thoại)', []); state['last_ex'] = 'TEXT'; flags.append('tiêu đề tổng hợp «对话文本» (nguồn không có tiêu đề cho bài đọc to) — cần duyệt')
                    emit(5, t, body); continue
                cl = child_level(lv)
                if r == 'EX':
                    letter = re.match(r'^(?:Bài tập\s+)?([A-H])', t).group(1)
                    han = han_from_body(body, re.compile(r'^%s\s' % letter))
                    vie = ''
                    if han:
                        for i0, l0 in enumerate(body[:14]):
                            if l0.strip():
                                c0 = cand(body, i0)
                                if c0 and c0[1] == han:
                                    vie = re.sub(r'^[A-H]\s*[\.:：]\s*', '', marker(body, i0)[2]).strip(); break
                    if han and not re.search(r'[\u4e00-\u9fff]', t):
                        label = han + (' (' + vie + ')' if vie else '')
                    else: label = t
                    emit(4, label, body)
                    state['last_ex'] = 'EX'; stack[:] = [(2, 2), (3, 3), (lv, 4)]
                    if not han and not re.search(r'[\u4e00-\u9fff]', t): flags.append('«%s»: không thấy nhãn Hán trong thân, giữ nhãn Việt — cần duyệt' % t)
                    continue
                # OTHER (bài đọc, mục con …)
                if cl is not None and stack and stack[-1][1] >= 4 and lv > stack[-1][0]:
                    emit(cl, t, body); continue
                emit(4, t, body); state['last_ex'] = 'TEXT'; stack[:] = [(2, 2), (3, 3), (lv, 4)]; continue
        # mặc định
        emit(max(child_level(lv) or 3, 3), t, body)
    return out, flags, dropped, kbout, gone

def emit_tasks(out, flags, body, n):
    """Nếu 任务选择 không có tiêu đề cho từng nhiệm vụ, nhưng thân có «任务一 …» thì chèn tiêu đề."""
    pass

def split_inline(out, flags, body, n):
    pass

# ---------------------------------------------------------------- hậu xử lý: chèn tiêu đề cho thân gộp (EX / TASK)
def postprocess(lines, n, flags):
    """Tách các thân gộp: đoạn có nhãn Hán «B 朗读…», «任务二　…» nhưng không có heading riêng → chèn heading."""
    res = []; i = 0
    cur_h = None; cur_lv = None; cur_letter = None; in_tc = False
    for idx, ln in enumerate(lines):
        m = HRE.match(ln)
        if m:
            lv = len(m.group(1)); t = m.group(2)
            cur_h = t; cur_lv = lv
            in_tc = t.startswith('任务选择')
            mm = re.match(r'^([A-H])\b', t)
            cur_letter = mm.group(1) if mm else (None if lv <= 3 else cur_letter)
            res.append(ln); continue
        # dòng «**中文：**» theo sau là nhãn Hán
        if re.match(r'^\*\*中文[:：]\*\*', ln.strip()):
            j = idx + 1
            while j < len(lines) and not lines[j].strip(): j += 1
            if j < len(lines):
                me = CN_EX.match(lines[j]); mt = CN_TASK.match(lines[j])
                if me and cur_lv is not None and cur_lv in (3, 4, 5) and not (HRE.match(lines[idx - 1]) or (idx > 1 and HRE.match(lines[idx - 2]))):
                    L = me.group(1)
                    if L != cur_letter and not in_task_block(res):
                        hl = lines[j].strip().rstrip('\\').strip()
                        res.append('#### ' + hl); res.append(''); cur_letter = L
                        flags.append('tiêu đề «%s» được chèn từ nhãn Hán trong thân (nguồn gộp) — cần duyệt' % hl)
                if mt and in_tc_context(res):
                    hl = lines[j].strip().rstrip('\\').strip()
                    res.append('#### ' + hl); res.append('')
                    flags.append('tiêu đề «%s» được chèn từ nhãn Hán trong thân — cần duyệt' % hl)
        res.append(ln)
    return res

def in_task_block(res):
    for ln in reversed(res):
        m = HRE.match(ln)
        if m: return m.group(2).startswith(('任务', 'Nhiệm vụ'))
    return False

def in_tc_context(res):
    for ln in reversed(res):
        m = HRE.match(ln)
        if m:
            t = m.group(2)
            return t.startswith(('任务选择', '任务')) or t.startswith('评价') is False and 'PRODUCE' in ''.join(x for x in res if x.startswith('## PRODUCE'))
    return False

def body_lines(text):
    """Các dòng không phải heading (đã bỏ dòng trống) — để kiểm bất biến."""
    out = []; fence = False
    for ln in text.split('\n'):
        if ln.strip().startswith('```'): fence = not fence
        if not fence and HRE.match(ln): continue
        if ln.strip(): out.append(ln.strip())
    return out

EXPECT = ['## Tiêu đề bài', '## Bảng tên nhân vật', '## PREPARE', '## EXPLORE', '### 促成 · 对话', '### 促成 · 拓展', '## PRODUCE',
          '### 任务支持', '### 任务选择', '### 评价', '## 附录', '### 录音文本']

def s2(res):
    """S2: các mục khung phải có và đúng thứ tự; trả danh sách mục thiếu / sai thứ tự."""
    heads = [l for l in res.split('\n') if re.match(r'^#{2,3} ', l)]
    pos = []; missing = []
    for e in EXPECT:
        idx = next((i for i, h in enumerate(heads) if h.startswith(e)), None)
        if idx is None: missing.append(e)
        else: pos.append(idx)
    return missing, pos != sorted(pos)

def main():
    rep = ['# P2 · Kết quả chuẩn hoá 12 file md của ky (tạo tự động bởi tools/normalize_ky_md.py)\n',
           '| Bài | h2 | Dòng thân trước | Dòng thân sau | Mất | Thêm | Bỏ (Tổng kết…) | Cờ cần duyệt |', '|---|---|---|---|---|---|---|---|']
    detail = []; s2rows = ['\n## S2 · mục khung thiếu / sai thứ tự\n', '| Bài | Thiếu | Sai thứ tự |', '|---|---|---|']
    for n, fn in FILES.items():
        p = os.path.join(SRC, fn)
        text = docx_to_md(p) if fn.endswith('.docx') else open(p, encoding='utf8').read()
        if fn.endswith('.docx'): open(os.path.join(OUT, 'Bai01_tu_docx.md'), 'w', encoding='utf8').write(text)
        out, flags, dropped, kbout, gone = normalize(n, text)
        res = re.sub(r'\n{3,}', '\n\n', '\n'.join(out)).rstrip() + '\n'
        open(os.path.join(OUT, 'Bai%02d.md' % n), 'w', encoding='utf8').write(res)
        if kbout: open(os.path.join(KB, 'Bai%02d_phu_luc.md' % n), 'w', encoding='utf8').write('\n\n'.join(kbout) + '\n')
        before = collections.Counter(body_lines(text)); after = collections.Counter(body_lines(res))
        # dòng thuộc phần bị bỏ/KB không tính là mất
        allowed = gone
        lost = before - after - allowed
        added = after - before
        h2 = [l for l in res.split('\n') if l.startswith('## ')]
        ms, bad = s2(res); s2rows.append('| %d | %s | %s |' % (n, ', '.join(m.lstrip('# ') for m in ms) or '—', 'có' if bad else 'không'))
        rep.append('| %d | %d | %d | %d | %d | %d | %s | %d |' % (n, len(h2), sum(before.values()), sum(after.values()), sum(lost.values()),
                   sum(added.values()), ', '.join('%s (%d ký tự)' % d for d in dropped) or '—', len(flags)))
        detail.append('\n## Bài %d\n\n**h2:** ' % n + ' → '.join(x[3:] for x in h2) + '\n')
        if lost: detail.append('**Dòng thân bị mất (%d), mẫu:**\n' % sum(lost.values()) + '\n'.join('- `%s`' % k[:100] for k in list(lost)[:5]) + '\n')
        if added: detail.append('**Dòng thân mới (%d), mẫu:**\n' % sum(added.values()) + '\n'.join('- `%s`' % k[:100] for k in list(added)[:5]) + '\n')
        for f in flags: detail.append('- ⚠ ' + f)
    open(os.path.join(ROOT, 'reports', 'P2_ket_qua_chuan_hoa.md'), 'w', encoding='utf8').write('\n'.join(rep) + '\n' + '\n'.join(s2rows) + '\n' + '\n'.join(detail) + '\n')
    print('\n'.join(rep))

if __name__ == '__main__':
    main()
