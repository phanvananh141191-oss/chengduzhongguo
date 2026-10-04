"""ld: bài đọc hiển thị theo câu — mỗi câu Hán kèm pinyin và Việt ngay bên dưới; bổ sung Việt còn thiếu cho ví dụ họ formal.
Dùng: python3 tools/ld_sentences.py <html>   (sửa tại chỗ)"""
import re, sys, json, os
sys.path.insert(0, os.path.dirname(__file__))
import ld_sent as S

OLD = '<div class="ptx han">${hv(p.h,LC.V)}</div><div class="spy pin">${esc(p.p)}</div><div class="svi mv">${esc(p.v)}</div>'
NEW = ("${p.hd?`<div class=\"phd\">${esc(p.hd)}</div>`:''}"
       "${(p.sn||[{h:p.h,p:p.p,v:p.v}]).map(s=>`<div class=\"sn\"><div class=\"ptx han\">${hv(s.h,LC.V)}</div>"
       "<div class=\"spy pin\">${esc(s.p)}</div><div class=\"svi mv\">${esc(s.v)}</div></div>`).join('')}")
CSS = (".pa .sn{margin:0 0 10px}.pa .sn:last-child{margin-bottom:0}.pa .sn .ptx{line-height:1.9}"
       ".pa .sn .svi{margin-top:2px;line-height:1.6;padding-left:10px;border-left:3px solid var(--line)}"
       ".pa .phd{font-weight:700;color:var(--gc);margin:0 0 6px}")

def main(path):
    h = open(path, encoding='utf-8').read()
    m = re.search(r'(<script type="application/json" id="src-ld">)(.*?)(</script>)', h, re.S)
    d = json.loads(m.group(2))
    # --- LES ---
    i = d.index('const LES='); j = d.index('\n', i)
    L = json.loads(d[i + 10:j].rstrip(';'))
    tot = 0; merged = 0
    for l in L:
        for r in l['reads']:
            for p in r['p']:
                hd = re.match(r'\s*\*\*([^*]+)\*\*\s*', p['h'])
                q = dict(p)
                if hd: q['h'] = p['h'][hd.end():]; p['hd'] = hd.group(1).strip()
                p['sn'] = S.pair_para(q); tot += len(p['sn'])
                merged += sum(1 for x in p['sn'] if len(S.sent_zh(x['h'])) > 1)
    lit = json.dumps(L, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    d = d[:i + 10] + lit + ';' + d[j:]
    # --- JS + CSS ---
    assert OLD in d, 'không thấy mẫu reading()'
    d = d.replace(OLD, NEW, 1)
    d = d.replace('</style>', CSS + '</style>', 1) if '.pa .sn{' not in d else d
    # --- Việt còn thiếu ở ví dụ họ formal ---
    vi = json.load(open(os.path.join(os.path.dirname(__file__), 'ld_vi_bosung.json'), encoding='utf-8'))
    i = d.index('const BK='); j = d.index('\n', i)
    BK = json.loads(d[i + 9:j].rstrip(';')); filled = 0
    def fill(exs):
        nonlocal filled
        for e in exs:
            if not (e.get('vi') or '').strip() and e['h'] in vi: e['vi'] = vi[e['h']]; filled += 1
    for f in BK['FORM']: fill(f['ex'])
    for f in BK['fadd'].values(): fill(f.get('ex', []))
    d = d[:i + 9] + json.dumps(BK, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + ';' + d[j:]
    h = h[:m.start(2)] + json.dumps(d, ensure_ascii=False).replace('<', '\\u003c') + h[m.end(2):]
    open(path, 'w', encoding='utf-8').write(h)
    print('ld_sentences: %d khối câu (%d khối gộp nhiều câu Hán); điền Việt cho %d ví dụ' % (tot, merged, filled))

if __name__ == '__main__':
    main(sys.argv[1])
