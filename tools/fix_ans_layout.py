"""Thứ tự trong mỗi bài tập fz: yêu cầu → ô nhập (luôn hiện) → nút (Kiểm tra / Xem đáp án / Làm lại) → đáp án (gập).
Trước đây ô nhập nằm TRONG khối đáp án ẩn và nút nằm sau đáp án.  Dùng: python3 tools/fix_ans_layout.py <html>"""
import re, sys, json

TA = r'<div class="ansh">✍️ Ô nhập của bạn</div><textarea class="uans"[^>]*></textarea>'

def main(path):
    h = open(path, encoding='utf-8').read()
    m = re.search(r'(<script type="application/json" id="src-fz">)(.*?)(</script>)', h, re.S)
    d = json.loads(m.group(2))
    # 1) nâng ô nhập ra ngoài .ans
    pat = re.compile(r'<div class="ans" hidden="">((?:(?!<div class="ans").)*?)(' + TA + r')</div>', re.S)
    d, n = pat.subn(lambda x: '<div class="uin">%s</div><div class="ans" hidden="">%s</div>' % (x.group(2), x.group(1)), d)
    # 1b) bài 3–14: khối đáp án chỉ có ô tự nhập → ô nhập ra ngoài, khối đáp án ghi «chưa có đáp án trong nguồn»
    pat2 = re.compile(r'<div class="ans" hidden=""><div class="ansh">💡 Đáp án</div>(<textarea class="uans"[^>]*>)</textarea></div>')
    def v2(x):
        ta = re.sub(r'placeholder="[^"]*"', 'placeholder="Nhập bài làm của bạn — tự lưu trên trình duyệt."', x.group(1))
        return '<div class="uin"><div class="ansh">✍️ Ô nhập của bạn</div>%s</textarea></div><div class="ans" hidden=""><div class="ansh">💡 Đáp án</div><div class="ln lv">Chưa có đáp án trong tài liệu nguồn.</div></div>' % ta
    d, n2 = pat2.subn(v2, d); n += n2
    # 1c) thẻ đã có khung viết riêng (.wr) thì không thêm ô nhập thứ hai
    out = []; pos = 0; dropped = 0
    for x in re.finditer(r'<div class="uin">.*?</textarea></div>', d, re.S):
        ci = d.rfind('<div class="card', 0, x.start())
        if ci >= 0 and 'class="wr"' in d[ci:x.start()] or (ci >= 0 and re.search(r'class="wr[ "]', d[ci:x.start()])):
            out.append(d[pos:x.start()]); pos = x.end(); dropped += 1
    out.append(d[pos:]); d = ''.join(out)
    print('  bỏ %d ô nhập trùng với khung viết .wr' % dropped)
    # 2) thanh nút đặt trước khối đáp án
    a = "  card.appendChild(bar);\n"
    assert a in d
    d = d.replace(a, "  (function(){var fa=A[0];if(fa&&fa.parentNode===card)card.insertBefore(bar,fa);else card.appendChild(bar)})();\n", 1)
    b = "x.appendChild(b)\n    });"
    assert b in d
    d = d.replace(b, "if(a.parentNode===x)x.insertBefore(b,a);else x.appendChild(b)\n    });", 1)
    # 3) CSS
    css = ".uin{margin:10px 0}.uin .ansh{font-size:.9em;color:var(--u-mut,#666);margin:0 0 4px}.uin textarea.uans{width:100%;min-height:5.5em;box-sizing:border-box;border:1px dashed var(--u-line);border-radius:8px;background:var(--u-card);color:inherit;font:inherit;padding:8px}.uxb{margin:8px 0}"
    d = d.replace("</style>", css + "</style>", 1) if '.uin{' not in d else d
    h = h[:m.start(2)] + json.dumps(d, ensure_ascii=False).replace('<', '\\u003c') + h[m.end(2):]
    open(path, 'w', encoding='utf-8').write(h)
    print('fix_ans_layout: %d ô nhập nâng ra ngoài khối đáp án' % n)

if __name__ == '__main__':
    main(sys.argv[1])
