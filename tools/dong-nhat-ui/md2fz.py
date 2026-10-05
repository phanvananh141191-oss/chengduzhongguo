#!/usr/bin/env python3
# Chuyển file bản dịch song ngữ (md) của 发展汉语 II bài 9–14 thành các <section class="les"> cho D2.
import re,html,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import csvdata,photo_vocab
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
    for L,t in photo_vocab.V.items():
        for i,(w,py,en) in t.items():
            if len(w)>1:
                sy=csvdata.syllables(w,py.replace('//',' '))
                if sy: out[w]='!'+' '.join(sy)
    return out
SPLIT={'模式':['mó','shì'],'颠簸':['diān','bǒ'],'安抚':['ān','fǔ'],'不安':['bù','ān'],'一时':['yì','shí'],'不由得':['bù','yóu','de'],'瞥见':['piē','jiàn'],'何况':['hé','kuàng'],'出于':['chū','yú'],'强迫':['qiǎng','pò'],'惊奇':['jīng','qí'],'浮躁':['fú','zào'],'冷静':['lěng','jìng'],'屏蔽':['píng','bì'],'外界':['wài','jiè'],'干扰':['gān','rǎo'],'噪声':['zào','shēng'],'精英':['jīng','yīng'],'打交道':['dǎ','jiāo','dao'],'公寓':['gōng','yù'],'负担':['fù','dān'],'空虚':['kōng','xū'],'再三':['zài','sān'],'稳定':['wěn','dìng'],'体面':['tǐ','miàn'],'寂静':['jì','jìng'],'终极':['zhōng','jí'],'打击':['dǎ','jī'],'悲观':['bēi','guān'],'消极':['xiāo','jí'],'宁静':['níng','jìng'],'尽头':['jìn','tóu'],'导致':['dǎo','zhì'],'浏览':['liú','lǎn'],'设置':['shè','zhì'],'当下':['dāng','xià']}
def l11_front():
    rows=['| # | 词语 | Pinyin | Loại từ | Nghĩa tiếng Việt | English |','| :-- | :-- | :-- | :-- | :-- | :-- |']
    for n,w,py,pos,en,vi in L11_VOCAB:
        rows.append('| %d | %s | %s | %s | %s | %s |'%(n,w,py,POS[pos],vi,en))
    return [('h',2,'题解 — Giới thiệu chủ đề'),('p',[L11_JIETI_ZH]),('p',[L11_JIETI_VI]),('h',2,'词语学习 — Học từ vựng'),('table',rows)]

# ---- Bài 11 bài tập tr.182 và tr.184 (từ ảnh sách); bản dịch tiếng Việt do người biên soạn dịch thêm, cần duyệt ----
B8='＿＿＿＿＿＿'
def _ol(items): return ('ol',[(i+1,[z,v]) for i,(z,v) in enumerate(items)])
def l11_exercises():
    b=[]
    b+=[('h',3,'四、选择合适的词语填空'),('p',['Chọn từ ngữ thích hợp điền vào chỗ trống'])]
    b+=[('p',['浮躁　于　导致　浏览　调　强迫　专注　出于　干扰　不由得　刷']),
        ('p',['Nôn nóng · Ở, vào (giới từ) · Dẫn đến · Duyệt, lướt xem · Điều chỉnh · Ép buộc · Tập trung · Xuất phát từ · Quấy nhiễu · Không kìm được · Quẹt, lướt (màn hình).'])]
    b+=[('p',['随着手机功能的增加，人们使用手机的场景日渐增多，使用手机的时间更是成倍增长。很多人%s发出这样的感叹：手机打败了电视，打败了电脑，打败了游戏机……'%B8]),
        ('p',['Cùng với việc chức năng của điện thoại ngày càng nhiều, các tình huống con người dùng điện thoại ngày càng tăng, thời gian dùng điện thoại lại càng tăng gấp bội. Rất nhiều người %s thốt lên rằng: điện thoại đã đánh bại ti vi, đánh bại máy tính, đánh bại máy chơi game……'%B8]),
        ('p',['手机的确给我们带来了很多便利，但同时也带来了害处。首先，手机大大改变了我们的阅读习惯，很多人不再习惯%s专心阅读，而是变成了%s，这一习惯的改变%s我们整个人都变了样子。我们变得心生%s，做事不再%s，被那个什么都不是的手机搞得失魂落魄，三心二意。其次，我无数次看到开车的、骑车的，一路走一路%s手机，弄得马路上险象环生。我还看到过，边走边看手机，一头撞在电线杆子上的事。当然，医生给病人看病，抽空还要“关照”一下手机的情况也是屡见不鲜，%s对自己负责，也是对他人负责，这些现象真的不应该再存在了。'%((B8,)*7)]),
        ('p',['Điện thoại quả thực mang lại cho chúng ta rất nhiều tiện lợi, nhưng đồng thời cũng mang đến tác hại. Trước hết, điện thoại đã thay đổi rất nhiều thói quen đọc của chúng ta: nhiều người không còn quen %s đọc tập trung nữa mà trở thành %s; sự thay đổi thói quen này %s cả con người chúng ta đều đổi khác. Chúng ta trở nên %s trong lòng, làm việc không còn %s nữa, bị chiếc điện thoại chẳng là gì ấy làm cho thẫn thờ, mất hồn, ba lòng hai ý. Tiếp theo, tôi đã vô số lần thấy người lái xe, người đạp xe vừa đi vừa %s điện thoại, khiến trên đường nguy hiểm rình rập. Tôi còn từng thấy người vừa đi vừa xem điện thoại rồi đâm đầu vào cột điện. Dĩ nhiên, bác sĩ khám bệnh cho bệnh nhân mà tranh thủ còn “để mắt” xem tình hình điện thoại cũng là chuyện thường thấy; %s chịu trách nhiệm với bản thân, cũng là chịu trách nhiệm với người khác. Những hiện tượng này thật sự không nên tồn tại nữa.'%((B8,)*7)]),
        ('p',['说句时髦的话，请%s你自己把手机%s成飞行模式或者干脆关机，这样才能免去外界的%s，一心一意做事。你觉得对吗？'%((B8,)*3)]),
        ('p',['Nói một câu thời thượng, xin hãy %s bạn tự chuyển điện thoại %s thành chế độ máy bay hoặc dứt khoát tắt máy, như vậy mới tránh được %s từ thế giới bên ngoài và một lòng một dạ làm việc. Bạn thấy đúng không?'%((B8,)*3)])]
    b+=[('h',3,'五、用指定词语完成句子'),('p',['Hoàn thành câu bằng từ ngữ được chỉ định'])]
    b+=[_ol([
      ('据说这种花草的香味具有%s。（安抚）'%B8,'Nghe nói hương thơm của loài hoa cỏ này có tác dụng %s. (安抚 — trấn an)'%B8),
      ('三层玻璃就能有效地%s，让我们免受干扰吗？（隔绝）'%B8,'Chỉ cần kính ba lớp là có thể %s một cách hiệu quả, giúp chúng ta khỏi bị quấy nhiễu phải không? (隔绝 — cách ly)'%B8),
      ('%s，不妨听一听轻音乐，让心静下来。（浮躁）'%B8,'%s, bạn thử nghe một chút nhạc nhẹ để lòng tĩnh lại. (浮躁 — nôn nóng)'%B8),
      ('有人说，你常%s，你就会变成什么样的人。（打交道）'%B8,'Có người nói, bạn thường %s, bạn sẽ trở thành kiểu người như thế. (打交道 — giao thiệp)'%B8),
      ('咱们出去旅游别住%s，据说民宿又便宜又舒服。（高档）'%B8,'Chúng ta đi du lịch đừng ở %s, nghe nói nhà dân vừa rẻ vừa thoải mái. (高档 — cao cấp)'%B8),
      ('我好像感冒了，发烧，流鼻涕，还%s。（浑身）'%B8,'Hình như tôi bị cảm, sốt, sổ mũi, lại còn %s. (浑身 — toàn thân)'%B8),
      ('她的%s，现在正在为实现理想而努力呢。（理想）'%B8,'Cái %s của cô ấy, hiện giờ cô ấy đang nỗ lực để thực hiện lý tưởng đấy. (理想 — lý tưởng)'%B8)])]
    b+=[('h',3,'六、用指定词语完成对话'),('p',['Hoàn thành hội thoại bằng từ ngữ được chỉ định'])]
    b+=[_ol([
      ('A：谢谢你，%s。（要不是）\\\nB：别客气，我正好顺路。'%B8,'A: Cảm ơn bạn, %s. (要不是 — nếu không nhờ)\\\nB: Đừng khách sáo, vừa hay tôi tiện đường.'%B8),
      ('A：下周末我们想去爬山。\\\nB：天气预报下周末有大到暴雨，%s，我看，你们还是换个日子吧。（何况）'%B8,'A: Cuối tuần sau chúng tôi muốn đi leo núi.\\\nB: Dự báo thời tiết nói cuối tuần sau có mưa to đến mưa bão, %s, tôi thấy các bạn nên đổi ngày khác. (何况 — huống chi)'%B8),
      ('A：%s，不建议你选择这个工作。（出于）\\\nB：那好吧，我好好想想。'%B8,'A: %s, tôi không khuyên bạn chọn công việc này. (出于 — xuất phát từ)\\\nB: Vậy được, để tôi suy nghĩ kỹ.'%B8),
      ('A：糟了，我的手机不见了，可能丢了。\\\nB：别着急，%s，你都在哪儿用了手机。（冷静）'%B8,'A: Hỏng rồi, điện thoại của tôi không thấy đâu, có thể bị mất rồi.\\\nB: Đừng vội, %s, bạn đã dùng điện thoại ở những đâu. (冷静 — bình tĩnh)'%B8),
      ('A：真佩服她，失败了那么多次，终于成功了。\\\nB：是啊，%s，可她还是坚持下来了。（打击）'%B8,'A: Thật khâm phục cô ấy, thất bại nhiều lần như vậy mà cuối cùng đã thành công.\\\nB: Đúng vậy, %s, nhưng cô ấy vẫn kiên trì được. (打击 — đả kích)'%B8),
      ('A：%s，收入不一定多，但老有人给开支的工作。（稳定）\\\nB：那就去邮局，或者去卖药。'%B8,'A: %s, thu nhập chưa chắc nhiều, nhưng là công việc lúc nào cũng có người chi trả. (稳定 — ổn định)\\\nB: Vậy thì đi bưu điện, hoặc đi bán thuốc.'%B8),
      ('A：你别这样走来走去的，走得我都头晕。\\\nB：唉，病人还在抢救，%s。（不安）'%B8,'A: Bạn đừng đi qua đi lại như vậy, đi làm tôi chóng mặt.\\\nB: Haizz, bệnh nhân vẫn đang được cấp cứu, %s. (不安 — bất an)'%B8),
      ('A：他平时不怎么爱说话，今天怎么话这么多呀？\\\nB：%s，他今天求婚成功了，高兴的。（惊奇）'%B8,'A: Bình thường anh ấy không hay nói, hôm nay sao nói nhiều thế?\\\nB: %s, hôm nay anh ấy cầu hôn thành công, vui quá đấy. (惊奇 — ngạc nhiên)'%B8)])]
    b+=[('h',3,'七、用指定词语改写句子'),('p',['Dùng từ ngữ được chỉ định để viết lại câu']),_ol([
      ('他离开这家小公司，去了一个工资更高的大公司。%s（辞）'%B8,'Anh ấy rời công ty nhỏ này, sang một công ty lớn có lương cao hơn. %s (辞 — từ chức)'%B8),
      ('A：这么快，一张报纸几分钟就看完啦？\\\nB：看一眼大标题而已。%s（浏览）'%B8,'A: Nhanh vậy, một tờ báo mà vài phút đã đọc xong rồi sao?\\\nB: Chỉ liếc qua tiêu đề lớn thôi. %s (浏览 — lướt xem)'%B8),
      ('平常穿衣服一点儿都不讲究的她，今天穿这么漂亮，这是要干什么去呀？%s（体面）'%B8,'Cô ấy bình thường ăn mặc chẳng chút cầu kỳ, hôm nay lại mặc đẹp thế này, đây là định đi đâu vậy? %s (体面 — thể diện, chỉnh tề)'%B8)]),
      _ol([
      ('你想事情不能总往不好的方面想，要多想它好的一面。%s（悲观）'%B8,'Bạn nghĩ sự việc không thể lúc nào cũng nghĩ theo hướng xấu, hãy nghĩ nhiều hơn đến mặt tốt của nó. %s (悲观 — bi quan)'%B8),
      ('你把时间安排得太紧了吧，减轻点儿压力，留出点儿娱乐的时间吧。%s（负担）'%B8,'Bạn sắp xếp thời gian quá sát rồi, hãy giảm bớt áp lực, chừa chút thời gian giải trí đi. %s (负担 — gánh nặng)'%B8),
      ('他第一次看到海底世界有那么多奇形怪状的生物，感到吃惊又好奇。%s（惊奇）'%B8,'Lần đầu tiên anh ấy thấy thế giới dưới đáy biển có nhiều sinh vật hình dạng kỳ quái như vậy, cảm thấy vừa kinh ngạc vừa tò mò. %s (惊奇 — ngạc nhiên)'%B8),
      ('我这么做完全是善意，谁让咱们是朋友呢！%s（出于）'%B8,'Tôi làm như vậy hoàn toàn là thiện ý, ai bảo chúng ta là bạn bè chứ! %s (出于 — xuất phát từ)'%B8),
      ('张教授实在是太忙了，这场报告还是经过一次又一次请求，他才答应的。%s（再三）'%B8,'Giáo sư Trương thật sự quá bận, bài báo cáo này vẫn là sau khi được thỉnh cầu hết lần này đến lần khác ông mới nhận lời. %s (再三 — nhiều lần)'%B8)])]
    b[-1]=('ol',[(i+4,p) for i,(n,p) in enumerate(b[-1][1])])
    b+=[('h',3,'八、在理解课文的基础上，回答下面的问题'),('p',['Dựa trên sự hiểu bài khóa, trả lời các câu hỏi sau']),
        _ol([('飞机颠簸后，“我”看见一位老人在看书，老人把书递给“我”，让“我”看。请以“我”的口气说说当时的情况和想法。','Sau khi máy bay xóc nảy, “tôi” nhìn thấy một cụ già đang đọc sách, cụ đưa cuốn sách cho “tôi”, bảo “tôi” xem. Hãy dùng giọng của “tôi” để kể lại tình huống và suy nghĩ lúc đó.'),
             ('畅想一下：如果你接受课文中的建议，把生活设置成“飞行模式”，你打算在什么时候设置，设置成什么样？','Hãy tưởng tượng: nếu bạn tiếp nhận lời khuyên trong bài khóa, thiết lập cuộc sống của mình sang “chế độ máy bay”, bạn dự định thiết lập vào lúc nào, thiết lập như thế nào?')])]
    b+=[('h',3,'九、参考提示词语、格式和对话中的特殊要求，完成对话'),('p',['Tham khảo các từ ngữ gợi ý, cấu trúc và yêu cầu đặc biệt trong hội thoại để hoàn thành hội thoại']),
        ('table',['| 表示目的 — Biểu thị mục đích | 出于 — Xuất phát từ　为了 — Để　为的是 — Vì để　目的是 — Mục đích là |','| :-- | :-- |','| 表示假设 — Biểu thị giả thiết | 要不是A — Nếu không phải A　假设 — Giả sử　假如 — Giả như　要是 — Nếu |','| 表示担心 — Biểu thị lo ngại | 恐怕 — E rằng　怕是 — Sợ là |']),
        ('p',['A：毕业后，你想留在大城市，还是回家乡？']),('p',['A: Sau khi tốt nghiệp, bạn muốn ở lại thành phố lớn hay về quê?']),
        ('p',['B：我肯定是要回去的。']),('p',['B: Tôi chắc chắn là sẽ về.']),
        ('p',['A：为什么这么坚决？']),('p',['A: Sao lại kiên quyết như vậy?']),
        ('p',['B：%s：第一，我不习惯北方的气候，太干了；第二，家乡生活节奏慢，压力小，更适合我这种懒人。你呢？（表示目的）'%B8]),
        ('p',['B: %s: Thứ nhất, tôi không quen khí hậu miền Bắc, quá khô; thứ hai, nhịp sống ở quê chậm, áp lực nhỏ, phù hợp hơn với người lười như tôi. Còn bạn? (Yêu cầu: Thể hiện mục đích.)'%B8])]
    return b

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
        if c['n']==11:
            bl=c['blocks']; k=[i for i,x in enumerate(bl) if x[0]=='h' and x[2].startswith('对话片段')]
            if k and not any(x[0]=='h' and x[2].startswith('四、') for x in bl):
                bl[k[0]:k[0]+1]=l11_exercises()+[('h',3,bl[k[0]][2])]
    return L

def vocab_table(rows,lesson=None):
    cells=[[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
    cells=[c for c in cells if not all(re.match(r'^:?-+:?$',x) for x in c)]
    body=cells[1:]; ph=photo_vocab.V.get(lesson,{})
    six=len(cells[0])==6 or bool(ph)
    head=['#','词语','Pinyin','Loại từ','Hán Việt','Nghĩa tiếng Việt']+(['English'] if six else [])
    out=[]
    for c in body:
        w=c[1]; r=csvdata.lookup(w)
        if len(c)==6: n,_,py,pos,vi,en=c
        else:
            n,_,pos,vi=c; p=ph.get(int(n)) if n.isdigit() else None
            if p and p[0]==w: py,en=p[1],p[2]
            else: py=(r['pinyin'].strip() if r else ''); en=''
        hv=(r['han_viet'].strip() if r else '')
        out.append([n,w,py,pos,hv,vi]+([en] if six else []))
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
                hd,rw=vocab_table(b[1],c['n']); out.append(cells_table(hd,rw))
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
