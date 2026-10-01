#!/usr/bin/env python3
# Chuyển file bản dịch song ngữ (md) của 发展汉语 II bài 9–14 thành các <section class="les"> cho D2.
import re,html,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import csvdata
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
        head=(['#','词语','Pinyin','Loại từ','Nghĩa tiếng Việt','English'] if len(head)==6 else ['#','词语','Loại từ','Nghĩa tiếng Việt'][:len(head)])
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

# ---- Bài 11: 题解 + 词语学习 lấy từ ảnh sách (tr.171–172); nghĩa tiếng Việt do người biên soạn dịch thêm, cần duyệt ----
POS={'动':'动 — Động từ','名':'名 — Danh từ','形':'形 — Tính từ','副':'副 — Phó từ','连':'连 — Liên từ'}
L11_JIETI_ZH='朋友，是不是有太多因素干扰你的生活和心情？那不妨试着把它们调成“飞行模式”吧，摆脱各种干扰，静听心灵之声，享受独处带来的内心的丰富。'
L11_JIETI_VI='Bạn ơi, có phải có quá nhiều yếu tố đang gây nhiễu cuộc sống và tâm trạng của bạn không? Vậy sao không thử chuyển chúng sang “chế độ máy bay”, thoát khỏi mọi sự quấy nhiễu, lặng nghe tiếng nói của tâm hồn và tận hưởng sự phong phú nội tâm mà việc ở một mình mang lại.'
L11_VOCAB=[
(1,'调','tiáo','动','to adjust','Điều chỉnh'),
(2,'模式','móshì','名','mode; pattern','Chế độ; mô thức'),
(3,'颠簸','diānbǒ','动','to jolt; to shake up and down','Rung lắc; xóc nảy'),
(4,'安抚','ānfǔ','动','to appease; to pacify','Trấn an; xoa dịu'),
(5,'不安','bù\'ān','形','uneasy','Bất an; lo lắng'),
(6,'一时','yìshí','名','a short while; a moment','Một lúc; nhất thời'),
(7,'不由得','bùyóude','副','can\'t help (doing sth.)','Không kìm được; không thể không'),
(8,'瞥见','piējiàn','动','to get a glimpse of','Thoáng thấy'),
(9,'何况','hékuàng','连','moreover; what\'s more','Huống chi; hơn nữa'),
(10,'出于','chūyú','动','to stem from; to be out of','Xuất phát từ; vì'),
(11,'强迫','qiǎngpò','动','to compel; to force','Ép buộc; cưỡng ép'),
(12,'惊奇','jīngqí','形','surprised; amazed','Ngạc nhiên; kinh ngạc'),
(13,'浮躁','fúzào','形','restless; impulsive','Nôn nóng; bồn chồn'),
(14,'冷静','lěngjìng','形','calm','Bình tĩnh'),
(15,'屏蔽','píngbì','动','to shield','Che chắn; chặn'),
(16,'外界','wàijiè','名','outside world','Thế giới bên ngoài'),
(17,'干扰','gānrǎo','动','to disturb','Quấy nhiễu; làm phiền'),
(18,'噪声','zàoshēng','名','noise','Tiếng ồn'),
(19,'精英','jīngyīng','名','elite','Tinh hoa; người ưu tú'),
(20,'打交道','dǎ jiāodao','动','to make contact with; to have dealings with','Giao thiệp; tiếp xúc với'),
(21,'公寓','gōngyù','名','apartment','Căn hộ; chung cư'),
(22,'负担','fùdān','名','burden; load','Gánh nặng'),
(23,'空虚','kōngxū','形','empty; blank','Trống rỗng'),
(24,'再三','zàisān','副','repeatedly; again and again','Nhiều lần; hết lần này đến lần khác'),
(25,'辞','cí','动','to resign','Từ chức; xin thôi việc'),
(26,'稳定','wěndìng','形','steady; stable','Ổn định'),
(27,'体面','tǐmiàn','形','honorable; decent','Thể diện; đàng hoàng'),
(28,'寂静','jìjìng','形','silent; quiet; noiseless','Tĩnh lặng; yên ắng'),
(29,'终极','zhōngjí','名','ultimate; final','Tối thượng; cuối cùng'),
(30,'打击','dǎjī','动','to attack; to strike','Đả kích; tấn công'),
(31,'悲观','bēiguān','形','pessimistic; gloomy','Bi quan'),
(32,'消极','xiāojí','形','passive; negative','Tiêu cực; thụ động'),
(33,'宁静','níngjìng','形','tranquil; peaceful','Yên tĩnh; thanh bình'),
(34,'尽头','jìntóu','名','end','Điểm cuối; tận cùng'),
(35,'导致','dǎozhì','动','to lead to; to result in','Dẫn đến; gây ra'),
(36,'浏览','liúlǎn','动','to glance over; to skim through','Lướt xem; duyệt qua'),
(37,'设置','shèzhì','动','to set','Thiết lập; cài đặt'),
(38,'当下','dāngxià','名','the present; the current','Hiện tại; lúc này')]
def dict_words():
    d={}
    for n,w,py,pos,en,vi in L11_VOCAB:
        if len(w)>1: d[w]='!'+' '.join(re.sub(r"'"," ",py).split(' ')) if False else None
    out={}
    for n,w,py,pos,en,vi in L11_VOCAB:
        if len(w)<2: continue
        if ' ' in py: syl=py.split(' ')
        else:
            syl=[];cur=''
            # tách theo dấu ' và theo số chữ: dùng bảng chia sẵn
            syl=SPLIT.get(w)
        out[w]='!'+' '.join(syl)
    out['调成']='!tiáo chéng'
    return out
SPLIT={'模式':['mó','shì'],'颠簸':['diān','bǒ'],'安抚':['ān','fǔ'],'不安':['bù','ān'],'一时':['yì','shí'],'不由得':['bù','yóu','de'],'瞥见':['piē','jiàn'],'何况':['hé','kuàng'],'出于':['chū','yú'],'强迫':['qiǎng','pò'],'惊奇':['jīng','qí'],'浮躁':['fú','zào'],'冷静':['lěng','jìng'],'屏蔽':['píng','bì'],'外界':['wài','jiè'],'干扰':['gān','rǎo'],'噪声':['zào','shēng'],'精英':['jīng','yīng'],'打交道':['dǎ','jiāo','dao'],'公寓':['gōng','yù'],'负担':['fù','dān'],'空虚':['kōng','xū'],'再三':['zài','sān'],'稳定':['wěn','dìng'],'体面':['tǐ','miàn'],'寂静':['jì','jìng'],'终极':['zhōng','jí'],'打击':['dǎ','jī'],'悲观':['bēi','guān'],'消极':['xiāo','jí'],'宁静':['níng','jìng'],'尽头':['jìn','tóu'],'导致':['dǎo','zhì'],'浏览':['liú','lǎn'],'设置':['shè','zhì'],'当下':['dāng','xià']}
def l11_front():
    rows=['| # | 词语 | Pinyin | Loại từ | Nghĩa tiếng Việt | English |','| :-- | :-- | :-- | :-- | :-- | :-- |']
    for n,w,py,pos,en,vi in L11_VOCAB:
        rows.append('| %d | %s | %s | %s | %s | %s |'%(n,w,py,POS[pos],vi,en))
    return [('h',2,'题解 — Giới thiệu chủ đề'),('p',[L11_JIETI_ZH]),('p',[L11_JIETI_VI]),('h',2,'词语学习 — Học từ vựng'),('table',rows)]

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
    for c in L:
        if c['n']==11 and not any(b[0]=='h' and b[2].startswith('词语学习') for b in c['blocks']):
            c['blocks']=l11_front()+c['blocks']
    return L

def vocab_table(rows):
    cells=[[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
    cells=[c for c in cells if not all(re.match(r'^:?-+:?$',x) for x in c)]
    body=cells[1:]; six=len(cells[0])==6
    head=['#','词语','Pinyin','Loại từ','Hán Việt','Nghĩa tiếng Việt']+(['English'] if six else [])
    out=[]
    for c in body:
        w=c[1]; r=csvdata.lookup(w)
        if six: n,_,py,pos,vi,en=c
        else:
            n,_,pos,vi=c; en=''; py=(r['pinyin'].strip() if r else '')
        hv=(r['han_viet'].strip() if r else '')
        row=[n,w,py,pos,hv,vi]+([en] if six else [])
        out.append(row)
    return head,out
def cells_table(head,rows):
    h='<thead><tr>'+''.join('<th>%s</th>'%inline(c) for c in head)+'</tr></thead>'
    b='<tbody>'+''.join('<tr>'+''.join('<td>%s</td>'%inline(c) for c in r)+'</tr>' for r in rows)+'</tbody>'
    return '<div class="tw"><table>%s%s</table></div>'%(h,b)
def dict_updates(present,C,W):
    """trả về (C_mới, W_mới) lấy từ kho từ vựng CSV cho chữ chưa có pinyin"""
    R=csvdata.rows(); newC={}; newW={}
    for ch in present:
        if ch in C: continue
        r=R.get(ch)
        if r and r['pinyin'] and not re.search(r'[\s/,;、]',r['pinyin'].strip()): newC[ch]=r['pinyin'].strip()
    for w,r in R.items():
        if not (2<=len(w)<=6) or not r['pinyin'] or w in W: continue
        if not all('\u3400'<=c<='\u9fff' for c in w): continue
        if not any((c not in C) for c in w if c in present or True): continue
        if not any(c not in C and c in present for c in w): continue
        sy=csvdata.syllables(w,r['pinyin'])
        if sy: newW[w]=' '.join(sy)
    # từ vựng bài 9–14 (kể cả khi mọi chữ đã có pinyin riêng)
    for c in lessons():
        for b in c['blocks']:
            pass
    return newC,newW
def vocab_words():
    ws=set()
    for c in lessons():
        st=None
        for b in c['blocks']:
            if b[0]=='h' and b[1]==2: st=b[2]
            if b[0]=='table' and st and st.startswith('词语学习'):
                for r in b[1]:
                    cc=[x.strip() for x in r.strip().strip('|').split('|')]
                    if len(cc)>1 and re.match(r'^\d+$',cc[0]): ws.add(cc[1])
    return ws

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
            if state=='vo':
                hd,rw=vocab_table(b[1]); out.append(cells_table(hd,rw))
            else: out.append(table_html(b[1])); continue
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
