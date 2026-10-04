"""fz bài 4 và bài 8: bổ sung phần còn thiếu từ ảnh trang sách (tr.52–68 / tr.123–138).
Chạy trước fz_cardui.py và fz_pair.py.  Dùng: python3 tools/fz_b4b8.py <html>"""
import re, sys, json, os
sys.path.insert(0, os.path.dirname(__file__))
from pypinyin import pinyin, Style
from fz_b4b8_data import *
from fz_pair import han_segments, vi_segments, pair

NOTE = '<div class="note"><b>Bổ sung từ ảnh trang sách %s</b> (bạn gửi 04/10/2026): chữ Hán theo nguyên văn trang sách; bản dịch tiếng Việt do biên soạn.</div>'
UIN = ('<div class="uin"><div class="ansh">✍️ Ô nhập của bạn</div><textarea class="uans" data-k="ans:fz:%s:e%d" '
       'placeholder="Nhập bài làm của bạn — tự lưu trên trình duyệt."></textarea></div>'
       '<div class="ans" hidden=""><div class="ansh">💡 Đáp án</div><div class="ln lv">Chưa có đáp án trong tài liệu nguồn.</div></div>')
BLANK = '<input autocomplete="off" class="uw"/>'

def py(w):
    out = []
    for p in pinyin(re.sub(r'[《》]', '', w), style=Style.TONE, errors=lambda x: [x]):
        out.append(p[0])
    s = ' '.join(out); return re.sub(r'\s+([、，。；：,;:])', r'\1', s)
def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
def zh(s):  # giữ <b>, <I/>
    s = esc(s).replace('&lt;b&gt;', '<b>').replace('&lt;/b&gt;', '</b>').replace('&lt;I/&gt;', BLANK); return s
def vi(s): return esc(s)
def para(h, v): return '<div class="ln lz">%s</div><div class="ln lv">%s</div>' % (zh(h), vi(v))
STAT = {'ok': 0, 'fallback': 0}
def para_p(h, v):
    """Đoạn Hán + đoạn Việt → từng câu Hán (.zu) có câu Việt (.trs) ngay dưới (cùng kiểu bài 1–2)."""
    hs = han_segments(zh(h)); g = pair(hs, vi_segments(vi(v))) if hs else None
    if not g: STAT['fallback'] += 1; return para(h, v)
    STAT['ok'] += 1
    return ''.join('<div class="zu">%s</div><div class="trs">%s</div>' % (''.join(hs[i] for i in hi), t) for hi, t in g)
def notes_html(notes):
    out = ['<h3>注释 · Chú thích</h3><ol>']
    for w, vt, parts in notes:
        li = '<li><div class="zu nh"><strong>%s</strong> <span class="py">%s</span>：</div><div class="trs">%s</div>' % (esc(w), py(w), vi(vt))
        for h, v in parts: li += '<div class="zu">%s</div><div class="trs">%s</div>' % (esc(h), vi(v))
        out.append(li + '</li>')
    return ''.join(out) + '</ol>'
def label(p): return '<p class="py pg">%s</p>' % p
def card(lesson, e, num, title, vit, page, body):
    return '<div class="card ex"><h3>%s、%s</h3>%s<div class="ln lv">%s (tr.%s)</div>%s%s</div>' % (
        num, title, label(page), vit, page.replace('P', '').replace('–', '–'), body, UIN % (lesson, e))
def ol(items):
    return '<ol>' + ''.join('<li>%s</li>' % para(h, v) for h, v in items) + '</ol>'

def section(f, n):
    i = f.find('id="l%d"' % n); j = f.find('<section class="les', i + 10)
    return i, (j if j > 0 else len(f))

def l4(s):
    # ---- 走进课文
    a = s.index('<h2>走进课文'); b = s.index('<h3>课文旁问题')
    body = '<h2>走进课文 · Tìm hiểu bài đọc</h2>' + label('P54–P56') + (NOTE % 'tr.54–56')
    for h, v in L4_TEXT: body += para_p(h, v)
    body += '<div class="ln lz">%s</div><div class="ln lv">%s</div>' % L4_AUTHOR
    body += notes_html(L4_NOTES)
    s = s[:a] + body + s[b:]
    # ---- 课文旁问题: nhãn trang + hàng còn thiếu (3, 6, 7)
    s = s.replace('<p class="py pg">P54–P55</p><div class="ln lp">Yī, kèwén wèndá (P54, P55 yòucè sīkǎotí)</div><div class="ln lv">I. Hỏi đáp bài khóa (câu hỏi suy nghĩ bên phải tr.54, 55)</div>',
                  '<p class="py pg">P54–P56</p><div class="ln lp">Yī, kèwén wèndá (P54–P56 yòucè sīkǎotí)</div><div class="ln lv">I. Hỏi đáp bài khóa (câu hỏi suy nghĩ bên phải tr.54–56)</div>')
    def row(n):
        q, qv, a, av = L4_QS[n]
        qc = '<div class="ln lz">%s</div><div class="ln lp">%s</div><div class="ln lv">%s</div>' % (esc(q), py(q), vi(qv))
        ac = ('<div class="ln lz">%s</div><div class="ln lp">%s</div><div class="ln lv">%s</div>' % (esc(a), py(a), vi(av))) if a else \
             '<div class="ln lv">Hoạt động thực hành, không có đáp án cố định.</div>'
        return '<tr><td>%s</td><td>%s</td></tr>' % (qc, ac)
    def after(s, key, new):
        m = re.search(r'<tr><td><div class="ln lz">%s</div>.*?</tr>' % re.escape(key), s, re.S)
        assert m, key; return s[:m.end()] + new + s[m.end():]
    if '“此时”' not in s:
        s = after(s, '起飞', row(3)); s = after(s, '老奶奶睡得很沉', row(6) + row(7))
    # ---- 四: nốt đoạn cuối, bỏ cảnh báo cắt
    m = re.search(r'<div class="ln lz">天色发白了.*?</div><div class="ln lp">.*?</div><div class="ln lv">.*?</div><div class="card">⚠️.*?</div><div class="note">.*?</div>', s, re.S)
    assert m
    p = ('Tiānsè fābái le, rénmen fēnfēn jǔqǐ xiàngjī, pòqiè de děngdài rìchū. Kěshì, hěnjiǔ dōu bújiàn tàiyáng chūlái, zhèshí, dàjiā cái yìshí dào, '
         'pà shì yīntiān, tàiyáng bù chūlái le. Yěbà, nà jiù kàn yúnhǎi ba, yě bié yǒu yì fān fēngqù ne.')
    new = '<div class="ln lz">%s</div><div class="ln lp">%s</div><div class="ln lv">%s</div>' % (zh(L4_SI[0]), p, vi(L4_SI[1])) + label('P62–P63')
    s = s[:m.start()] + new + s[m.end():]
    # ---- 五 … 十一
    e = 101; add = ''
    for num, title, vit, page, items in L4_EX:
        add += card('l4', e, num, title, vit, page, ol(items)); e += 1
    num, title, vit, page, tbl, items = L4_EX8
    t = '<div class="w"><table><tr><th>Yêu cầu</th><th>Mẫu / từ ngữ gợi ý</th></tr>' + ''.join(
        '<tr><td><div class="ln lz">%s</div><div class="ln lv">%s</div></td><td><div class="ln lz">%s</div><div class="ln lv">%s</div></td></tr>' % (esc(a), vi(b), esc(c), vi(d)) for a, b, c, d in tbl) + '</table></div>'
    add += card('l4', e, num, title, vit, page, t + ol(items)); e += 1
    num, title, vit, page, items, bank, bankvi = L4_EX9
    chips = ''.join('<span class="chip" data-w="%s" draggable="true">%s</span>' % (esc(re.sub(r'（.*?）', '', w)), esc(w)) for w in bank)
    simple = ','.join(esc(re.sub(r'（.*?）', '', w)) for w in bank if '……' not in w and 'A' not in w)
    wr = ('<blockquote><p><div class="ln lz"><div class="bank">%s</div></div><div class="ln lv">%s</div></p></blockquote>'
          '<div class="wr" data-k="wr:fz:l4:101" data-min="280" data-w="%s"><textarea placeholder="Viết ở đây… (tự động lưu trong trình trình duyệt)"></textarea><div class="wi"></div>'
          '<button class="b sv">Lưu</button><button class="b cp">Sao chép</button><button class="b cl">Xóa</button> <span class="tag st"></span></div>'
          '<div class="ans" hidden=""><div class="ansh">💡 Đáp án</div><div class="ln lv">Chưa có đáp án trong tài liệu nguồn.</div></div>') % (chips, vi(bankvi), simple)
    wr = wr.replace('trình trình duyệt', 'trình duyệt')
    add += '<div class="card ex"><h3>%s、%s</h3>%s<div class="ln lv">%s (tr.65–66)</div>%s%s</div>' % (num, title, label(page), vit, ol(items), wr)
    num, title, vit, page, (ttl, ttlv), paras, qs = L4_EX10
    body = '<div class="ln lz"><strong>%s</strong></div><div class="ln lv">%s</div>' % (esc(ttl), vi(ttlv)) + ''.join(para_p(h, v) for h, v in paras) + ol(qs)
    add += card('l4', e, num, title, vit, page, body); e += 1
    num, title, vit, page, items = L4_EX11
    add += card('l4', e, num, title, vit, page, ol(items))
    k = s.rfind('</section>') if s.rstrip().endswith('</section>') else len(s)
    return s[:k] + add + s[k:]

def l8(s):
    s = s.replace('<h2>题解 · Giới thiệu chủ đề</h2><div class="note"><b>Chưa có trong nguồn.</b> Tài liệu gốc không có phần này; không tự bổ sung.</div>',
                  '<h2>题解 · Giới thiệu chủ đề</h2>' + label('P123') + (NOTE % 'tr.123') + para_p(*L8_TIJIE))
    s = s.replace('<h2>词语学习 · Học từ vựng</h2>', '<h2>词语学习 · Học từ vựng</h2>' + label('P123–P124'), 1)
    a = s.index('<div class="card">⚠️ Chưa có phần 题解'); b = s.index('<h2>综合注释')
    body = '<h2>走进课文 · Tìm hiểu bài đọc</h2>' + label('P125–P127') + (NOTE % 'tr.125–127')
    for h, v in L8_TEXT: body += para_p(h, v)
    body += '<div class="ln lz">%s</div><div class="ln lv">%s</div>' % L8_AUTHOR
    body += notes_html(L8_NOTES)
    body += '<h3>课文旁问题 · Câu hỏi bên lề</h3>' + label('P125–P127') + '<div class="ln lv">Câu hỏi bên bài đọc (tr.125–127)</div>' + ol(L8_QS)
    s = s[:a] + body + s[b:]
    # nhãn trang cho 综合注释 / 综合练习 (theo số trang in ở góc sách)
    pg = {'l8-g-1': 'P128', 'l8-g-2': 'P129', 'l8-g-3': 'P129', 'l8-g-4': 'P130', 'l8-g-5': 'P131'}
    for k, v in pg.items():
        s = re.sub(r'(<h3 id="%s">.*?</h3>)' % k, lambda m: m.group(1) + label(v), s, count=1, flags=re.S)
    pe = {'一、字词知识与练习': 'P131', '二、参考注释': 'P132–P133', '三、选择合适的词语填空': 'P133–P134', '四、用指定词语或格式完成对话': 'P134–P135',
          '五、用指定词语或格式改写句子': 'P135', '六、在理解课文的基础上': 'P135', '七、写一写': 'P136–P137', '九、拓展学习': 'P138'}
    for k, v in pe.items():
        s = re.sub(r'(<h3>%s[^<]*</h3>)(?!<p class="py pg">)' % re.escape(k), lambda m: m.group(1) + label(v), s, count=1)
    s = s.replace('<p class="py pg">tr. 137–138</p>', '<p class="py pg">P137–P138</p>')
    # câu bị mờ ở bài 八 → khôi phục từ tr.138
    m = re.search(r'<div class="ln lz">姐姐因为家里旁边说.*?</div><div class="ln lp">.*?</div><div class="ln lv">.*?</div>.*?(<div class="ln lz">我们在明媚)', s, re.S)
    assert m
    new = ('<div class="ln lz">%s</div><div class="ln lp">%s</div><div class="ln lv">%s</div>' % (
        L8_FIX['new_zh'], 'Jiějie yīnwèi jiālǐ qióng dānwù le xuéxí, tā yìbiān gōngzuò, yìbiān shàng yèxiào, wánchéng le dàzhuān xuéyè.', L8_FIX['new_vi']))
    s = s[:m.start()] + new + m.group(1) + s[m.end():]
    return s

def main(path):
    h = open(path, encoding='utf-8').read()
    m = re.search(r'(<script type="application/json" id="src-fz">)(.*?)(</script>)', h, re.S); f = json.loads(m.group(2))
    if 'Bổ sung từ ảnh trang sách tr.54' not in f:
        i, j = section(f, 4); f = f[:i] + l4(f[i:j]) + f[j:]
        i, j = section(f, 8); f = f[:i] + l8(f[i:j]) + f[j:]
    h = h[:m.start(2)] + json.dumps(f, ensure_ascii=False).replace('<', '\\u003c') + h[m.end(2):]
    open(path, 'w', encoding='utf-8').write(h); print('fz_b4b8 ghép câu:', STAT); print('fz_b4b8: bài 4 (走进课文, 注释, 四–十一) và bài 8 (题解, 走进课文, 注释) đã bổ sung')
if __name__ == '__main__': main(sys.argv[1])
