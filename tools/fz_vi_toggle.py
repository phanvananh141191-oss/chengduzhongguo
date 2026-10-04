"""fz: mọi câu tiếng Việt phải nằm trong lớp .lv / .trs để nút «Dòng tiếng Việt» bật/tắt được.
Sửa các dòng `.ln.lz` có tiếng Việt lẫn trong: (a) «Hán pinyin — Việt» → tách lz / lp / lv; (b) dòng toàn tiếng Việt → lớp lv;
(c) chú nghĩa trong ngoặc «(cảnh đẹp)» → <span class="lv">; (d) nhãn đậm lẫn Hán–Việt → bọc phần Việt bằng span.lv.
Dùng: python3 tools/fz_vi_toggle.py <html>   (chạy cuối build_v4.sh)"""
import re, sys, json
VIO = re.compile(r'[ăâđêôơưảãạẻẽẹỉĩịỏõọủũụỷỹỵắằẳẵặấầẩẫậếềểễệốồổỗộớờởỡợứừửữựýỳ]', re.I)   # chữ chỉ có trong tiếng Việt
HAN = re.compile(r'[一-鿿]')
TAG = re.compile(r'<[^>]+>')
PAREN = re.compile(r'\((?:[^()<>]|<[^>]*>)*\)')      # (…) có thể chứa thẻ như <input>
def plain(s): return re.sub(r'\s+', ' ', TAG.sub('', s)).strip()
def vi(s): return bool(VIO.search(plain(s)))

def split_dash(inner):
    """'Hán … — Việt' (dấu ' — ' nằm ngoài thẻ) → (trái, phải) hoặc None"""
    pos = 0
    for m in re.finditer(r' — ', inner):
        before = inner[:m.start()]
        if before.count('<') == before.count('>'): pos = m; break
    else: return None
    return inner[:pos.start()], inner[pos.end():]

def lp_lv(right):
    """phải = 'pinyin (Việt)' hoặc 'Việt' → (pinyin|'', Việt)"""
    m = re.match(r'^(.*?)\s*\(([^()]*[ăâđêôơư][^()]*)\)\s*$', right, re.S)
    if m and not vi(m.group(1)): return m.group(1), m.group(2)
    return '', right

def fix_lz(inner):
    t = plain(inner)
    if not vi(inner): return None
    if not HAN.search(t):
        sd = split_dash(inner)
        if sd and not vi(sd[0]):                          # pinyin — Việt
            return '<div class="ln lp">%s</div><div class="ln lv">%s</div>' % sd
        return '<div class="ln lv">%s</div>' % inner       # toàn tiếng Việt
    sd = split_dash(inner)
    if sd and vi(sd[1]) and not vi(sd[0]):                 # Hán [pinyin] — Việt  (hoặc — pinyin (Việt))
        left, right = sd; p, v = lp_lv(right)
        if left.startswith('(') and right.rstrip().endswith(')') and left.count('(') > left.count(')'):   # (… — …) giữ ngoặc cân
            left += ')'; v = v.rstrip()[:-1]
        if not HAN.search(plain(left)):                    # vế trái là pinyin thuần
            out = '<div class="ln lp">%s</div>' % left
            return out + '<div class="ln lv">%s</div>' % v
        lz = left; lp = ''
        for m in re.finditer(r'(?<=[\u4e00-\u9fff。！？，,.!?）)”"\u3002])\s+(?=[A-Za-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜĀÁǍÀĒÉĚÈĪÍǏÌŌÓǑÒŪÚǓÙ])', left):
            before = left[:m.start()]
            if before.count('<') != before.count('>'): continue            # đang nằm trong thẻ → bỏ qua
            if not HAN.search(TAG.sub('', left[m.end():])): lz, lp = left[:m.start()], left[m.end():]
            break
        if p: lp = (lp + ' ' + p).strip() if lp else p
        out = '<div class="ln lz">%s</div>' % lz
        if lp: out += '<div class="ln lp">%s</div>' % lp
        return out + '<div class="ln lv">%s</div>' % v
    # (c) chú nghĩa trong ngoặc tròn
    def wrap(m): return '<span class="lv">%s</span>' % m.group(0) if vi(m.group(0)) else m.group(0)
    cur = re.sub(PAREN, wrap, inner)
    r = mixed(cur)
    if r is None: return cur if cur != inner else None
    kind, out = r
    return '<div class="ln lv">%s</div>' % out if kind == 'whole' else out

def mixed(cur):
    """(d) còn tiếng Việt lẫn Hán: dòng chủ yếu là tiếng Việt → ('whole', html); ngược lại bọc từng đoạn Việt bằng span.lv → ('wrap', html)"""
    rest = plain(re.sub(r'<span class="lv">.*?</span>', '', cur, flags=re.S))
    if not VIO.search(rest): return None
    letters = len(re.findall(r'[A-Za-zÀ-ỹ]', re.sub(r'[\u4e00-\u9fff]', '', rest)))
    if letters > 6 * max(1, len(HAN.findall(rest))): return 'whole', cur
    toks = re.split(r'(<span class="lv">.*?</span>|<[^>]+>)', cur, flags=re.S)
    def run(r):
        g = r.group(0)
        if not (VIO.search(g) and len(g.strip()) > 3): return g
        return '%s<span class="lv">%s</span>%s' % (re.match(r'^[\s：:，,;；]*', g).group(0), g.strip(' ：:，,;；'), re.search(r'[\s：:，,;；]*$', g).group(0))
    for k, tk in enumerate(toks):
        if tk.startswith('<') or not tk.strip(): continue
        toks[k] = re.sub(r'(?:["“][\u4e00-\u9fff]{1,10}["”]|[^\u4e00-\u9fff])+', run, tk)
    return 'wrap', ''.join(toks)

def main(path):
    h = open(path, encoding='utf-8').read()
    m = re.search(r'(<script type="application/json" id="src-fz">)(.*?)(</script>)', h, re.S); f = json.loads(m.group(2))
    cnt = {'lz→lv/tách': 0, 'ngoặc': 0}
    def sub(mm):
        inner = mm.group(1); r = fix_lz(inner)
        if r is None: return mm.group(0)
        if r.startswith('<div'): cnt['lz→lv/tách'] += 1; return r
        cnt['ngoặc'] += 1; return '<div class="ln lz">%s</div>' % r
    f2 = re.sub(r'<div class="ln lz">((?:(?!</div>).)*)</div>', sub, f, flags=re.S)
    def sub_zu(mm):       # tiêu đề chú giải «<b>…</b> (chú nghĩa Việt) — ví dụ Hán»
        inner = mm.group(1)
        new = re.sub(PAREN, lambda x: '<span class="lv">%s</span>' % x.group(0) if vi(x.group(0)) else x.group(0), inner)
        r = mixed(new); cls = 'zu'
        if r: cls = 'zu lv' if r[0] == 'whole' else 'zu'; new = r[1]
        if new != inner: cnt['ngoặc'] += 1
        return '<div class="%s">%s</div>' % (cls, new)
    f2 = re.sub(r'<div class="zu">((?:(?!</div>).)*)</div>', sub_zu, f2, flags=re.S)
    f2 = re.sub(r'(\(Thứ tự thích hợp là: (?:<input[^>]*>)?\))', r'<span class="lv">\1</span>', f2)   # chữ lẻ ngoài thẻ
    h = h[:m.start(2)] + json.dumps(f2, ensure_ascii=False).replace('<', '\\u003c') + h[m.end(2):]
    open(path, 'w', encoding='utf-8').write(h); print('fz_vi_toggle:', cnt)
    # còn sót?
    left = []
    for mm in re.finditer(r'<div class="ln lz">((?:(?!</div>).)*)</div>', f2, re.S):
        i = mm.group(1); t = plain(re.sub(r'<span class="lv">.*?</span>', '', i, flags=re.S))
        if VIO.search(t): left.append(t[:100])
    print('còn sót', len(left)); [print('  ', x) for x in left[:12]]
if __name__ == '__main__': main(sys.argv[1])
