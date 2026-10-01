#!/usr/bin/env python3
# Chuyển file bản dịch song ngữ (md) của 发展汉语 II bài 9–14 thành các <section class="les"> cho D2.
import re,html,os
HERE=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.join(HERE,'nguon','ban-dich-bai-9-14.md')
CJK=re.compile(r'[㐀-鿿]')
LAT=re.compile(r'[A-Za-zÀ-ỹ]')
def is_zh(t):
    z=len(CJK.findall(t)); l=len(LAT.findall(t))
    return z>0 and z>=l
def inline(s):
    s=html.escape(s,quote=False)
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'(?<![\*\w])\*(?!\s)([^*\n]+?)(?<!\s)\*(?![\*\w])',r'<i>\1</i>',s)
    s=s.replace('\\\n','<br>')
    return s
def clean(md):
    lines=md.split('\n'); out=[]; skip=False
    for ln in lines:
        if re.match(r'^# ',ln): skip=True; continue          # lời nhắc của người dùng + lời dẫn của trợ lý
        if skip:
            if re.match(r'^#{2,6} ',ln): skip=False
            else: continue
        if skip is False and ln.startswith('<img'): continue
        if re.match(r'^(---|<div align|\[\^)',ln): continue
        if re.match(r'^_{5,}\s*$',ln): continue
        if re.match(r'^\*[^*].*\*\s*$',ln) and not ln.startswith('**'): continue   # ghi chú của trợ lý (in nghiêng cả dòng)
        out.append(ln)
    return out
def parse_blocks(lines):
    blocks=[]; i=0; n=len(lines)
    while i<n:
        ln=lines[i]
        if not ln.strip(): i+=1; continue
        m=re.match(r'^(#{2,6}) (.*)$',ln)
        if m: blocks.append(('h',len(m.group(1)),m.group(2).strip())); i+=1; continue
        if ln.startswith('|'):
            rows=[]
            while i<n and lines[i].startswith('|'):
                rows.append(lines[i]); i+=1
            blocks.append(('table',rows)); continue
        if re.match(r'^\d+\. ',ln):
            items=[]
            while i<n and re.match(r'^\d+\. ',lines[i]):
                m2=re.match(r'^(\d+)\. (.*)$',lines[i]); parts=[m2.group(2)]; num=int(m2.group(1)); i+=1
                while i<n and lines[i].strip() and not re.match(r'^(\d+\. |#{2,6} |\|)',lines[i]):
                    parts.append(lines[i]); i+=1
                items.append((num,parts))
                while i<n and not lines[i].strip() and i+1<n and re.match(r'^\d+\. ',lines[i+1]): i+=1
            blocks.append(('ol',items)); continue
        parts=[ln]; i+=1
        while i<n and lines[i].strip() and not re.match(r'^(#{2,6} |\||\d+\. )',lines[i]):
            parts.append(lines[i]); i+=1
        blocks.append(('p',parts))
    return blocks
def split_lines(parts):
    # các dòng trong một đoạn (kết thúc bằng \ là xuống dòng)
    return [p.rstrip('\\').strip() for p in parts if p.strip()]
def para_html(parts,cls=None):
    out=[]
    for t in split_lines(parts):
        c='lz' if is_zh(t) else 'lv'
        out.append('<div class="ln %s">%s</div>'%(c,inline(t)))
    return ''.join(out)
def table_html(rows,vocab=False):
    cells=[[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
    cells=[c for c in cells if not all(re.match(r'^:?-+:?$',x) for x in c)]
    if not cells: return ''
    head=cells[0]
    if vocab:
        head=['#','词语','Loại từ','Nghĩa tiếng Việt'][:len(head)]
    h='<thead><tr>'+''.join('<th>%s</th>'%inline(c) for c in head)+'</tr></thead>'
    b='<tbody>'+''.join('<tr>'+''.join('<td>%s</td>'%inline(c) for c in r)+'</tr>' for r in cells[1:])+'</tbody>'
    return '<div class="tw"><table>%s%s</table></div>'%(h,b)
GRLAB={'Câu trong bài':'Câu trong bài','Giải thích':'Giải thích','例如':'Ví dụ','试一试':'Thử làm'}
def label_of(t):
    for k in GRLAB:
        if t.startswith(k): return t
    return None
def role(t):
    if re.match(r'^题解',t): return 'ti'
    if re.match(r'^词语学习',t): return 'vo'
    if re.match(r'^(走进课文|课文旁问题|注释|胡适、吴健雄名片)',t): return 'tx'
    if re.match(r'^综合练习',t): return 'ex'
    if re.match(r'^附录',t): return 'ap'
    return 'other'
def lessons():
    md=open(SRC,encoding='utf-8').read()
    lines=clean(md)
    blocks=parse_blocks(lines)
    L=[]; cur=None
    for b in blocks:
        if b[0]=='h' and b[1]==2 and re.match(r'^第\d+课',b[2]):
            m=re.match(r'^第(\d+)课[：:]\s*(.*)$',b[2]); cur={'n':int(m.group(1)),'zh':m.group(2).strip(),'vi':None,'blocks':[]}; L.append(cur); continue
        if cur is None: continue
        cur['blocks'].append(b)
    for c in L:
        # dòng tiêu đề tiếng Việt "Bài N: …" ngay sau tiêu đề bài
        bl=c['blocks']
        if bl and bl[0][0]=='p':
            t=' '.join(split_lines(bl[0][1])); m=re.match(r'^Bài \d+:\s*(.*)$',t)
            if m: c['vi']=m.group(1).rstrip('.'); bl.pop(0)
        # tiêu đề h3 "题解" ở bài 9 -> h2
        c['blocks']=[('h',2,b[2]) if b[0]=='h' and b[1]==3 and re.match(r'^(题解|词语学习|走进课文|课文旁问题|综合练习)',b[2]) else b for b in c['blocks']]
    return L
def lesson_html(c):
    out=[]
    zh=c['zh']
    out.append('<section class="les" id="l%d">\n<h1>第%d课　%s</h1>'%(c['n'],c['n'],inline(zh)))
    state='ti'; gram_open=False; seen_zs=False; gr_started=False
    bl=c['blocks']; i=0; open_lab=False; in_item=False
    def close_lab():
        nonlocal open_lab
        if open_lab: out.append('</div>'); open_lab=False
    def close_item():
        nonlocal in_item
        close_lab()
        if in_item: out.append('</div>'); in_item=False
    for b in bl:
        if b[0]=='h':
            lvl,t=b[1],b[2]
            if lvl==2:
                close_item()
                r=role(t)
                if r=='other' and state in ('tx','gr') and not (re.match(r'^(对话片段|十|\d+\.)',t) and state=='ex'):
                    # mục ngữ pháp: gom dưới một tiêu đề 综合注释
                    if not gr_started:
                        out.append('<h2>综合注释 — Chú giải tổng hợp</h2>'); gr_started=True
                    out.append('<div class="card ul-gitem">'); in_item=True
                    out.append('<h3>%s</h3>'%inline(t)); state='gr'; continue
                if r!='other': state={'ti':'ti','vo':'vo','tx':'tx','ex':'ex','ap':'ap'}[r]
                out.append('<h2>%s</h2>'%inline(t)); continue
            # h3+
            if state=='gr':
                lab=label_of(t)
                if lab:
                    close_lab(); out.append('<div class="ul-gf" data-gl="%s">'%html.escape(lab)); open_lab=True; continue
                close_lab(); out.append('<h4>%s</h4>'%inline(t)); continue
            close_lab()
            out.append('<h%d>%s</h%d>'%(min(lvl,4),inline(t),min(lvl,4))); continue
        if b[0]=='p':
            out.append(para_html(b[1])); continue
        if b[0]=='ol':
            out.append('<ol>')
            for num,parts in b[1]:
                out.append('<li value="%d">%s</li>'%(num,para_html(parts)))
            out.append('</ol>'); continue
        if b[0]=='table':
            out.append(table_html(b[1],vocab=(state=='vo'))); continue
    close_item()
    out.append('</section>')
    return '\n'.join(out)
def toc_items():
    items=[]
    for c in lessons():
        zh=re.sub(r'[¹²³⁴⁵⁶⁷⁸⁹⁰]+$','',c['zh']).strip()
        items.append({'key':'fz:l%d'%c['n'],'n':'Bài %d'%c['n'],'zh':zh,'vi':c['vi'] or ''})
    return items
def sections_html():
    return '\n'.join(lesson_html(c) for c in lessons())
if __name__=='__main__':
    for c in lessons(): print(c['n'],c['zh'],'|',c['vi'],len(c['blocks']))
    h=sections_html(); print(len(h)); open('/tmp/fz9_14.html','w').write(h)
