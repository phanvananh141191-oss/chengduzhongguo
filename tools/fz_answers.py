"""Đáp án tự soạn cho thẻ bài tập fz (nguồn không có đáp án).
Dữ liệu: tools/fz_answers_data/lNN.py, biến ANS = {chỉ số thẻ: {...}} (chỉ số như `fz_dump_cards.py N`).
  guard : đầu h3 (hoặc chuỗi bất kỳ trong thẻ) để chắc chắn đúng thẻ
  refill: [đáp án cho TẤT CẢ ô nhập theo thứ tự] ghi đè data-a cũ (khi dữ liệu cũ bị lệch)
  fill  : [đáp án mỗi chỗ trống theo thứ tự]  → gắn data-a (chấm tự động; 'a|b' = nhiều đáp án chấp nhận)
  show  : [(hán, việt) hoặc str] → khối «Đáp án» (đánh số)
  note  : ghi chú dưới đáp án
Dùng: python3 tools/fz_answers.py <html>   (chạy sau fz_b4b8.py, trước fz_cardui.py)"""
import re, sys, json, os, importlib.util, html as H
HEAD = '<div class="ansh">💡 Đáp án <span class="tag">tự soạn — không phải đáp án của sách</span></div>'
OLD = re.compile(r'<div class="ans" hidden="">.*?Chưa có đáp án trong tài liệu nguồn\.</div></div>', re.S)

def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
def ans_html(e):
    out = [HEAD]
    items = e.get('show') or []
    if items:
        out.append('<ol>')
        for it in items:
            if isinstance(it, str): it = (it, '')
            zh, vi = it
            out.append('<li><div class="ln lz">%s</div>%s</li>' % (zh, ('<div class="ln lv">%s</div>' % esc(vi)) if vi else ''))
        out.append('</ol>')
    if e.get('note'): out.append('<div class="ln lv">%s</div>' % esc(e['note']))
    return '<div class="ans" hidden="">' + ''.join(out) + '</div>'

def patch_card(c, e):
    if 'fill' in e:
        it = iter(e['fill']); cnt = [0]
        def sub(m):
            tag = m.group(0)
            if 'data-a=' in tag: return tag
            try: a = next(it)
            except StopIteration: return tag
            cnt[0] += 1
            return tag.replace('<input', '<input data-a="%s"' % esc(a).replace('"', '&quot;'), 1)
        c = re.sub(r'<input[^>]*class="uw[^"]*"[^>]*/?>', sub, c)
        assert cnt[0] == len(e['fill']), ('số chỗ trống không khớp', cnt[0], len(e['fill']), e.get('guard'))
    if 'refill' in e:   # ghi đè data-a của TẤT CẢ ô nhập theo thứ tự (sửa dữ liệu lệch)
        it = iter(e['refill']); cnt = [0]
        def sub2(m):
            tag = re.sub(r'\sdata-a="[^"]*"', '', m.group(0))
            try: a = next(it)
            except StopIteration: return m.group(0)
            cnt[0] += 1
            return tag.replace('<input', '<input data-a="%s"' % esc(a).replace('"', '&quot;'), 1)
        c = re.sub(r'<input(?![^>]*type="?checkbox)[^>]*>', sub2, c)
        assert cnt[0] == len(e['refill']), ('refill không khớp', cnt[0], len(e['refill']), e.get('guard'))
    new = ans_html(e)
    if OLD.search(c): c = OLD.sub(lambda m: new, c, count=1)
    else: raise AssertionError('không thấy khối đáp án: %s' % e.get('guard'))
    return c

def load(n):
    p = os.path.join(os.path.dirname(__file__), 'fz_answers_data', 'l%02d.py' % n)
    if not os.path.exists(p): return None
    sp = importlib.util.spec_from_file_location('l%d' % n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m.ANS

def main(path):
    h = open(path, encoding='utf-8').read()
    m = re.search(r'(<script type="application/json" id="src-fz">)(.*?)(</script>)', h, re.S); f = json.loads(m.group(2)); done = {}
    for n in range(1, 15):
        ANS = load(n)
        if not ANS: continue
        i = f.find('id="l%d"' % n); j = f.find('<section class="les', i + 10); j = j if j > 0 else len(f); s = f[i:j]
        starts = [x.start() for x in re.finditer(r'<div class="card ex', s)] + [len(s)]
        pieces = []; last = 0; k = 0
        for a, b in zip(starts, starts[1:]):
            c = s[a:b]
            if k in ANS:
                e = ANS[k]; g = e.get('guard', '')
                assert g in H.unescape(re.sub(r'<[^>]+>', '', c)), ('guard sai', n, k, g)
                c = patch_card(c, e); done[n] = done.get(n, 0) + 1
            pieces.append(s[last:a]); pieces.append(c); last = b; k += 1
        pieces.append(s[last:]); f = f[:i] + ''.join(pieces) + f[j:]
    h = h[:m.start(2)] + json.dumps(f, ensure_ascii=False).replace('<', '\\u003c') + h[m.end(2):]
    open(path, 'w', encoding='utf-8').write(h); print('fz_answers:', done)
if __name__ == '__main__': main(sys.argv[1])
