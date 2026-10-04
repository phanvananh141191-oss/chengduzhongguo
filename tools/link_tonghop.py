#!/usr/bin/env python3
"""Nối các phần «Kiến thức tổng hợp» với bài học (chạy sau gen_ky và link_kb):
 - fz: 词语总表 (lv) ↔ bảng từ trong bài; 语法点总表 (lg) ↔ điểm ngữ pháp trong 综合注释.
 - ky: 附录二 词语总表 (s13) ↔ bảng từ trong bài.
Dùng: python3 tools/link_tonghop.py file.html   (ghi đè tại chỗ)"""
import re, sys, json, collections
f = sys.argv[1]
s = open(f, encoding='utf8').read()
enc = lambda d: json.dumps(d, ensure_ascii=False).replace('<', '\\u003c')
HAN = re.compile(r'[一-鿿]'); hanonly = lambda x: re.sub(r'[^一-鿿]', '', x)
strip = lambda h: re.sub(r'<[^>]+>', '', re.sub(r'<rt>[^<]*</rt>', '', h))
def patch_doc(book, fn):
    global s
    m = re.search(r'(<script type="application/json" id="src-%s">)(.*?)(</script>)' % book, s, re.S)
    d = json.loads(m.group(2).replace('\\u003c', '<')); d = fn(d)
    s = s[:m.start(2)] + enc(d) + s[m.end(2):]
STATS = collections.Counter()

XL_CSS = '''/*xl*/a.xl{text-decoration:none;font-size:.82em;margin-left:.3em;opacity:.85}a.xl:hover{opacity:1}
@keyframes xfl{from{background:rgba(255,200,0,.45);outline:2px solid #e0a800}to{background:transparent;outline:2px solid transparent}}.xflash{animation:xfl 1.8s ease-out}'''
def xl_js(book):
    return '''<script>/*xl*/
(function(){
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a.xl');if(!a)return;e.preventDefault();
  try{window.parent.postMessage({u3:1,book:'%s',t:'nav',key:a.getAttribute('data-go')},'*')}catch(x){}});
window.addEventListener('message',function(e){var m=e.data;if(!m||!m.u3)return;
  if((m.t==='go'||m.t==='init')&&typeof m.go==='string'&&m.go.indexOf('::')>0){
    var p=m.go.split('::'),c={};for(var k in m)c[k]=m[k];c.go=p[0];
    e.stopImmediatePropagation();
    window.dispatchEvent(new MessageEvent('message',{data:c,source:e.source,origin:e.origin}));
    setTimeout(function(){var el=document.getElementById(p[1]);if(el){el.scrollIntoView({block:'center'});el.classList.add('xflash');setTimeout(function(){el.classList.remove('xflash')},1900)}},m.t==='init'?1000:350)}
},true);
})();
</script>''' % book

# ================================================================== fz
def fz_fn(d):
    if '/*xl*/' in d: return d
    lessons = {}
    # 1. id hàng từ vựng và điểm ngữ pháp trong từng bài
    def do_lesson(m):
        n = int(m.group(2)); sec = m.group(3)
        if n > 14: return m.group(0)
        seen = set(); words = []
        # bảng từ: bảng đầu tiên sau h2 «词语学习»
        a = sec.find('词语学习'); tb = re.search(r'<table[^>]*>.*?</table>', sec[a:], re.S) if a >= 0 else None
        if tb:
            t0 = sec[a:][tb.start():tb.end()]
            def row(mr):
                w = hanonly(strip(mr.group(2)))
                if not w or w in seen: return mr.group(0)
                seen.add(w); words.append(w)
                c1 = mr.group(1)[:-5] + '@@LV:%d:%s@@</td>' % (n, w)          # chèn chỗ giữ liên kết cuối ô đầu
                return '<tr id="l%d-w-%s">%s%s' % (n, w, c1, mr.group(2))
            t1 = re.sub(r'<tr>(<td[^>]*>.*?</td>)(<td[^>]*>.*?</td>)', row, t0, flags=re.S)
            sec = sec[:a] + sec[a:].replace(t0, t1, 1)
        # điểm ngữ pháp 1..5 trong 综合注释
        g = sec.find('综合注释'); gend = len(sec)
        if g >= 0:
            mm = re.search(r'<h[23]>(?:Ví dụ|综合练习)|<h2>综合练习', sec[g + 10:])
            gend = g + 10 + mm.start() if mm else len(sec)
        gseg = sec[g:gend] if g >= 0 else ''; got = set()
        def h3(mm):
            k = int(mm.group(1))
            if k in got or not 1 <= k <= 5: return mm.group(0)
            got.add(k); return '<h3 id="l%d-g-%d">%s. %s%s</h3>' % (n, k, k, mm.group(2), '@@LG:%d:%d@@' % (n, k))
        def card(mm):
            k = int(mm.group(1))
            if k in got or not 1 <= k <= 5: return mm.group(0)
            got.add(k); return '<div class="card" id="l%d-g-%d"><b>%d. %s%s</b>' % (n, k, k, mm.group(2), '@@LG:%d:%d@@' % (n, k))
        def para(mm):
            k = int(mm.group(1))
            if k in got or not 1 <= k <= 5: return mm.group(0)
            got.add(k); return '<p id="l%d-g-%d"><b>%d. %s%s</b>' % (n, k, k, mm.group(2), '@@LG:%d:%d@@' % (n, k))
        gseg2 = re.sub(r'<h3>(\d)\.\s*(.*?)</h3>', h3, gseg, flags=re.S)
        gseg2 = re.sub(r'<p><b>(\d)\.\s*(.*?)</b>', para, gseg2, flags=re.S)
        gseg2 = re.sub(r'<div class="card"><b>(\d)\.\s*(.*?)</b>', card, gseg2, flags=re.S)
        if g >= 0: sec = sec[:g] + gseg2 + sec[gend:]
        lessons[n] = (set(words), got)
        return m.group(1) + sec
    d = re.sub(r'(<section class="les[^"]*" id="l(\d+)">)(.*?)(?=</section>)', do_lesson, d, flags=re.S)
    # 2. lv / lg: id hàng và liên kết về bài; bài về lv / lg
    def do_sum(sid, kind):
        nonlocal d
        a = d.find('id="%s"' % sid); b = d.find('</section>', a); sec = d[a:b]
        parts = re.split(r'(<h2>.*?</h2>)', sec, flags=re.S); out = [parts[0]]; cur = None
        for i in range(1, len(parts), 2):
            h = parts[i]; body = parts[i + 1] if i + 1 < len(parts) else ''
            mm = re.search(r'第(\d+)课', h); n = int(mm.group(1)) if mm else None
            if n and n in lessons:
                ws, gs = lessons[n]
                def row(mr):
                    key = hanonly(strip(mr.group(2))) if kind == 'lv' else mr.group(1)
                    if kind == 'lv':
                        if not key or key not in ws: return mr.group(0)
                        STATS['lv→bài'] += 1
                        return '<tr id="lv-l%d-%s"><td>%s<a class="xl" data-go="fz:l%d::l%d-w-%s" title="Mở từ này trong bài %d">📖</a></td><td>%s</td>' % (n, key, mr.group(1), n, n, key, n, mr.group(2))
                    k = int(key)
                    if k not in gs: return mr.group(0)
                    STATS['lg→bài'] += 1
                    return '<tr id="lg-l%d-%d"><td>%s<a class="xl" data-go="fz:l%d::l%d-g-%d" title="Mở điểm ngữ pháp trong bài %d">📖</a></td><td>%s</td>' % (n, k, mr.group(1), n, n, k, n, mr.group(2))
                body = re.sub(r'<tr><td>(\d+)</td><td>(.*?)</td>', row, body, flags=re.S)
            out += [h, body]
        d = d[:a] + ''.join(out) + d[b:]
    do_sum('lv', 'lv'); do_sum('lg', 'lg')
    # 3. liên kết ngược từ bài về lv / lg (thay thẻ giữ chỗ)
    def back(mm):
        kind, n, k = mm.group(1), int(mm.group(2)), mm.group(3)
        if kind == 'LV':
            if 'id="lv-l%d-%s"' % (n, k) not in d: return ''
            STATS['bài→lv'] += 1; return '<a class="xl" data-go="fz:lv::lv-l%d-%s" title="Xem trong 词语总表">📑</a>' % (n, k)
        if 'id="lg-l%d-%s"' % (n, k) not in d: return ''
        STATS['bài→lg'] += 1; return '<a class="xl" data-go="fz:lg::lg-l%d-%s" title="Xem trong 语法点总表">📑</a>' % (n, k)
    d = re.sub(r'@@(LV|LG):(\d+):([^@]+)@@', back, d)
    # 4. bộ dựng bảng từ của fz (vtBuild) làm phẳng ô → giữ id hàng và liên kết trong ô số thứ tự
    for a_, b_ in [
        ("rows.forEach(function(r){var cells=[].slice.call(r.cells);",
         "rows.forEach(function(r){var lk=[].slice.call(r.querySelectorAll('a.xl')).map(function(a){return a.cloneNode(true)}),rid=r.id;var cells=[].slice.call(r.cells);"),
        ("var o={cls:{}};", "var o={cls:{},links:lk,id:rid};"),
        ("if(k==='n'){td.textContent=o.n?o.n.td.textContent.trim():String(ri+1)}",
         "if(k==='n'){td.textContent=o.n?o.n.td.textContent.replace(/[\\u{1F4D6}\\u{1F4D1}]/gu,'').trim():String(ri+1);(o.links||[]).forEach(function(a){td.appendChild(document.createTextNode(' '));td.appendChild(a)})}"),
        ("data.forEach(function(o,ri){var tr=document.createElement('tr');", "data.forEach(function(o,ri){var tr=document.createElement('tr');if(o.id)tr.id=o.id;")]:
        assert d.count(a_) == 1, a_
        d = d.replace(a_, b_)
    d = d.replace('</style>', XL_CSS + '</style>', 1)
    i = d.rfind('</body>'); return d[:i] + xl_js('fz') + d[i:]
patch_doc('fz', fz_fn)

# ================================================================== ky: 附录二 词语总表 (s13)
def ky_fn(d):
    if '/*xl*/' in d: return d
    anchors = collections.defaultdict(set)      # từ -> {bài}
    for m in re.finditer(r'id="s(\d+)-w-([^"]+)"', d): anchors[m.group(2)].add(int(m.group(1)))
    a = d.find('id="s13"'); b = d.find('</section>', a); sec = d[a:b]
    ROW = re.compile(r'<tr>(\s*)<td([^>]*)>(.*?)</td>(\s*)<td([^>]*)>(.*?)</td>\s*</tr>', re.S)
    pages = collections.defaultdict(list)
    for mr in ROW.finditer(sec):
        h = hanonly(strip(mr.group(3))); pg = strip(mr.group(6)).strip()
        if h in anchors and len(anchors[h]) == 1 and pg.isdigit(): pages[next(iter(anchors[h]))].append(int(pg))
    rng = {n: (min(v), max(v)) for n, v in pages.items()}
    def pick(h, pg):
        ls = anchors.get(h)
        if not ls: return None
        if len(ls) == 1: return next(iter(ls))
        if pg.isdigit():
            p = int(pg); inr = [n for n in ls if n in rng and rng[n][0] <= p <= rng[n][1]]
            if inr: return inr[0]
            return min(ls, key=lambda n: min(abs(p - rng[n][0]), abs(p - rng[n][1])) if n in rng else 999)
        return min(ls)
    mapped = {}
    def row(mr):
        ws, wattr, wcell, mid, pattr, pgcell = mr.groups()
        h = hanonly(strip(wcell)); pg = strip(pgcell).strip()
        n = pick(h, pg) if h else None
        if not n:
            if h: STATS['s13 không nối được'] += 1
            return mr.group(0)
        mapped[(n, h)] = 1; STATS['s13→bài'] += 1
        return ('<tr id="s13-%d-%s">%s<td%s>%s</td>%s<td%s>%s <a class="xl" data-go="ky:s%d::s%d-w-%s" title="Mở trong bài %d">→ bài %d</a></td></tr>'
                % (n, h, ws, wattr, wcell, mid, pattr, pgcell, n, n, h, n, n))
    sec = ROW.sub(row, sec)
    d = d[:a] + sec + d[b:]
    def back(mm):
        n, w = int(mm.group(1)), mm.group(2)
        if (n, w) not in mapped: return mm.group(0)
        STATS['bài→s13'] += 1
        return mm.group(0) + '<a class="xl" data-go="ky:s13::s13-%d-%s" title="Xem trong 词语总表 cuối sách">📑</a>' % (n, w)
    d = re.sub(r'<a id="s(\d+)-w-([^"]+)" class="(?:kbl|kbx)"[^>]*>(?:🔗)?</a>', back, d)
    d = d.replace('</style>', XL_CSS + '</style>', 1)
    i = d.rfind('</body>'); return d[:i] + xl_js('ky') + d[i:]
patch_doc('ky', ky_fn)
open(f, 'w', encoding='utf8').write(s)
print('nối tổng hợp:', dict(STATS))
