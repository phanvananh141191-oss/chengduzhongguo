#!/usr/bin/env python3
"""P6: chỉnh nhỏ ld — không đổi dữ liệu LES.
Dùng: python3 tools/sync_ld.py vào.html ra.html"""
import re, sys, json
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf8').read()
m = re.search(r'(<script type="application/json" id="src-ld">)(.*?)(</script>)', s, re.S)
d = json.loads(m.group(2).replace('\\u003c', '<'))
log = []
def sub(a, b, count=1):
    global d
    n = d.count(a); assert n >= 1, a
    if count and n != count: raise AssertionError((a, n))
    d = d.replace(a, b); log.append((a[:50], n))

# 1. Nhãn đọc quét bài 1 giống 11 bài còn lại
sub('Tín hiệu &amp; Bẫy cần chú ý', 'Tín hiệu / Bẫy cần chú ý')

# 2. Ẩn dòng/mục fid–pid khi trống
sub("const row=(a,b)=>`<div class=\"lk\"><b>${a}</b>${b}</div>`;",
    "const row=(a,b)=>`<div class=\"lk\"><b>${a}</b>${b}</div>`,rowx=(a,b)=>b==='—'?'':row(a,b);")
sub("${row('Formal ↔ Spoken',fs.map(", "${rowx('Formal ↔ Spoken',fs.map(")
sub("${row('Pattern',ps.map(", "${rowx('Pattern',ps.map(")
sub("[(L.fid||[]).length+(L.pid||[]).length,'formal + pattern']].map(x=>",
    "[(L.fid||[]).length+(L.pid||[]).length,'formal + pattern']].filter(x=>x[1]!=='formal + pattern'||x[0]).map(x=>")
sub('<div class="sec"><h4>（二）常用书面词语 · Formal ↔ Spoken · ${fs.length}</h4>',
    '${fs.length?`<div class="sec"><h4>（二）常用书面词语 · Formal ↔ Spoken · ${fs.length}</h4>')
sub("<i>›</i></button>`).join('')}</div></div><h3 class=\"h3\">（三）常用格式 · Pattern · ${ps.length}</h3>${ps.map(x=>patCard(x,PAT.indexOf(x))).join('')}`",
    "<i>›</i></button>`).join('')}</div></div>`:''}${ps.length?`<h3 class=\"h3\">（三）常用格式 · Pattern · ${ps.length}</h3>${ps.map(x=>patCard(x,PAT.indexOf(x))).join('')}`:''}`")

# 3. Tên trang ngân hàng: Việt là tên, Anh/Hán trong ngoặc; số thứ tự khớp mục lục
V = [('v-for', '03 Formal ↔ Spoken · 常用书面词语', '02 Từ văn viết (Formal ↔ Spoken) · 常用书面词语'),
     ('v-pat', '04 Pattern Bank · 常用格式', '03 Khung câu (Pattern Bank) · 常用格式'),
     ('v-chk', '06 Chunk Bank', '04 Kho cụm từ (Chunk Bank) · 固定搭配'),
     ('v-par', '05 Parsing Lab', '05 Bẻ câu dài (Parsing Lab) · 长句分析'),
     ('v-scn', '07 Scanning Notes · 实况阅读', '06 Đọc quét (Scanning Notes) · 实况阅读'),
     ('v-map', '08 Map 24 技巧', '07 Bản đồ kỹ năng (Map 24) · 技巧地图'),
     ('v-gap', '09 GAP checklist', '08 Khoảng trống (GAP) · 查漏补缺')]
for vid, a, b in V:
    sub('<section class="view" id="%s"><div class="wrap"><div class="vh"><div class="kick">%s</div>' % (vid, a),
        '<section class="view" id="%s"><div class="wrap"><div class="vh"><div class="kick">%s</div>' % (vid, b))
sub('<h1>Chunk <em>Bank</em></h1>', '<h1>Kho <em>cụm từ</em></h1>')
sub('<h1>Parsing <em>Lab</em></h1>', '<h1>Bẻ <em>câu dài</em></h1>')
sub('<h1>7 dạng <em>实况</em></h1>', '<h1>7 dạng <em>đọc quét</em></h1>')
sub('<h1>Hub <em>12 bài</em></h1>', '<h1>Tổng quan <em>12 bài</em></h1>')
sub('<div class="kick">12 Bài · 乐读 5</div>', '<div class="kick">十二课总览 · 乐读 5</div>')


# 5. 《家庭学校》 (泛读, bài 1): 5 đoạn chỉ có tóm ý tiếng Việt → biên soạn Hán + pinyin theo nghĩa tiếng Việt (yêu cầu 04/10/2026)
HS = [
 ('家庭学校（Homeschooling）是美国的一种教育形式：孩子不去公立学校或私立学校，而是由父母亲自在家教授知识。',
  'jiā tíng xué xiào（Homeschooling）shì měi guó de yì zhǒng jiào yù xíng shì：hái zi bú qù gōng lì xué xiào huò sī lì xué xiào，ér shì yóu fù mǔ qīn zì zài jiā jiào shòu zhī shi。'),
 ('家庭学校历史悠久，最初是出于安全方面的考虑，如今已经吸引了二百多万名五至十七岁的学生参加。',
  'jiā tíng xué xiào lì shǐ yōu jiǔ，zuì chū shì chū yú ān quán fāng miàn de kǎo lǜ，rú jīn yǐ jīng xī yǐn le liǎng bǎi duō wàn míng wǔ zhì shí qī suì de xué shēng cān jiā。'),
 ('家庭学校在美国所有的州都是合法的，但是各州对管理方式、父母学历以及监督检查的要求并不相同。',
  'jiā tíng xué xiào zài měi guó suǒ yǒu de zhōu dōu shì hé fǎ de，dàn shì gè zhōu duì guǎn lǐ fāng shì、fù mǔ xué lì yǐ jí jiān dū jiǎn chá de yāo qiú bìng bù xiāng tóng。'),
 ('这种教育形式既有积极的一面，也有挑战：父母要辛苦地制订学习计划，还担心孩子的社交能力；但是它尊重孩子的个性，也增进了家人之间的亲密关系。',
  'zhè zhǒng jiào yù xíng shì jì yǒu jī jí de yí miàn，yě yǒu tiǎo zhàn：fù mǔ yào xīn kǔ de zhì dìng xué xí jì huà，hái dān xīn hái zi de shè jiāo néng lì；dàn shì tā zūn zhòng hái zi de gè xìng，yě zēng jìn le jiā rén zhī jiān de qīn mì guān xì。'),
 ('最后的建议是：父母在选择家庭学校时要深思熟虑，因为它并不是让每个孩子都比在普通学校里表现得更出色的默认选择。',
  'zuì hòu de jiàn yì shì：fù mǔ zài xuǎn zé jiā tíng xué xiào shí yào shēn sī shú lǜ，yīn wèi tā bìng bú shì ràng měi gè hái zi dōu bǐ zài pǔ tōng xué xiào lǐ biǎo xiàn de gèng chū sè de mò rèn xuǎn zé。'),
]
PH = re.compile(r'("i":(\d+),"r":"((?:[^"\\]|\\.)*)","s":"(?:[^"\\]|\\.)*","h":)"（Vault chưa có nguyên văn Hán ngữ của đoạn này — chỉ có tóm ý tiếng Việt）","p":""')
hits = PH.findall(d)
assert len(hits) == 5, len(hits)
def _fill(m):
    i = int(m.group(2)); h, py = HS[i - 1]
    r = m.group(3)
    head = m.group(1).replace('"r":"%s"' % r, '"r":"%s · Hán biên soạn lại từ tóm ý"' % r)
    return head + json.dumps(h, ensure_ascii=False) + ',"p":' + json.dumps(py, ensure_ascii=False)
d = PH.sub(_fill, d)
assert 'Vault chưa có nguyên văn Hán ngữ' not in d
log.append(('Hán biên soạn lại (ld bài 1)', 5))

new = json.dumps(d, ensure_ascii=False).replace('<', '\\u003c')
s = s[:m.start(2)] + new + s[m.end(2):]

# 4. Mục lục ở shell
tm = re.search(r'(<script type="application/json" id="toc-data">)(.*?)(</script>)', s, re.S)
toc = tm.group(2)
for a, b in [('Morpheme Bank · 24 ngữ tố', 'Kho ngữ tố (Morpheme Bank) · 24 ngữ tố'),
             ('Từ văn viết ↔ khẩu ngữ', 'Từ văn viết (Formal ↔ Spoken)'),
             ('Pattern Bank · khung câu văn viết', 'Khung câu (Pattern Bank) · văn viết'),
             ('Chunk Bank · cụm cố định', 'Kho cụm từ (Chunk Bank) · cụm cố định'),
             ('Parsing Lab · bẻ câu dài', 'Bẻ câu dài (Parsing Lab)'),
             ('Scanning Notes · 7 dạng đọc quét', 'Đọc quét (Scanning Notes) · 7 dạng'),
             ('Map 24 · 24 kỹ năng × 12 bài', 'Bản đồ kỹ năng (Map 24) · 24 kỹ năng × 12 bài'),
             ('GAP · danh sách khoảng trống', 'Khoảng trống (GAP) · danh sách')]:
    assert toc.count(a) == 1, a; toc = toc.replace(a, b)
s = s[:tm.start(2)] + toc + s[tm.end(2):]
open(dst, 'w', encoding='utf8').write(s)
print('ld: %d thay thế' % len(log))
