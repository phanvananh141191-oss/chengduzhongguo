"""Danh mục giọng tiếng Trung (ElevenLabs, trong tài khoản) và quy tắc ghép giọng cho bài khoá/bài đọc.
Giọng nam/nữ trẻ lấy theo danh sách bạn chọn; giọng trung niên/người lớn tuổi lấy từ nhãn tuổi của thư viện giọng ElevenLabs."""
import re
VOICES = {   # tên → voice_id   (n = nam, nu = nữ; y = trẻ, m = trung niên)
 # nữ trẻ
 'nu1': 'bhJUNIXWQQ94l8eI2VUf', 'bobo': 's2LjOZIlsH2Yu4p6MtAK', 'anna': 'PSvrh6w41Qm19oaaHLca', 'shan': 'ByhETIclHirOlWnWKhHc',
 'xiaoxi': '9DMBSOAnMDPiFAsz1ZGK', 'julia': 'tOuLUAIdXShmWH7PEUrU', 'willow': 'SyNyPD84lTuHqi1HONfV', 'susan': 'kAIqZ7fZv234ClKXwzDx', 'sage': 'APSIkVZudNbPAwyPoeVO',
 # nam trẻ
 'nam1': 'BWN0mOtkGHghA3CYFzFK', 'nam2': 'MI36FIkp9wRP7cpWKPTl', 'anson': 'xh2OInDk4GEYuYRtHx4M', 'jun': '5s3UifUu3OJ90z17rRMA', 'lan': 'bZtjnyJAFD0Cp3lfNG5g',
 'liuping': 'pTOe8BQRdydOEIgv0wFL', 'nss': 'nss5M23ZSzhG3Tn0b7wN', 'julian': 'j2FxFb20sd3xlm2pRaM5', 'adriany': 'agczkAUlHLowaNnL72Cc', 'aliby': 'qwKjxMVO8wNg6qaKKH1k',
 # nam trung niên
 'anchor': '2I36mEahS1u7ZnTKUoaB', 'erich': 'fYmV8EanqZP9BI4WvpB7', 'jason': 'DowyQ68vDpgFYdWVGjc3', 'adrianm': 'i2gDhHnLj4CvKBpf3gPR', 'siqi': 'W8lBaQb9YIoddhxfQNLP', 'jordan': 'EttSxNTvxX50EUdRPQQl',
 # nữ trung niên
 'huafeng': 'rtRocV7drsrJFSQPxlD3', 'mingyao': 'JZLpE3AGwpKYZI2X65hN', 'stella': 'BqljjWyTnrioXPCNkCd4', 'jill': 'V3z1DARAbkkTVEx5lmEl',
}
GENDER = {k: ('F' if k in ('nu1','bobo','anna','shan','xiaoxi','julia','willow','susan','sage','huafeng','mingyao','stella','jill') else 'M') for k in VOICES}
# nhân vật ky: (giọng, mô tả tuổi/giới)
CHAR = {
 '王晴晴': ('nu1', 'nữ trẻ'), '周雪松': ('nam1', 'nam trẻ'), '田梦': ('bobo', 'nữ trẻ'), '李岩': ('jason', 'nam trung niên (bố)'), '思思表哥': ('anson', 'nam trẻ'),
 '马波罗': ('jun', 'nam trẻ'), '张丽': ('huafeng', 'nữ trung niên (vợ Lý Nham)'), '爱娜': ('anna', 'nữ trẻ'), '王勇': ('jordan', 'nam trung niên'), '朴智慧': ('shan', 'nữ trẻ'),
 '陈文': ('nam2', 'nam ~30'), '王珊珊': ('julia', 'nữ ~29'), '丁思思': ('xiaoxi', 'nữ trẻ'), '陈新阳': ('lan', 'nam trẻ'), '林凯': ('liuping', 'nam trẻ'), '陈武': ('nss', 'nam trẻ'),
 '主持人': ('anchor', 'nam trung niên (MC)'), '许欣然': ('willow', 'nữ trẻ'), '李小岩': ('aliby', 'nam, con trai'), '冯尚德': ('julian', 'nam trẻ'), '陈文妈妈': ('mingyao', 'nữ lớn tuổi'),
 '咨询者': ('susan', 'nữ trẻ'), '咨询人': ('susan', 'nữ trẻ'), '专家': ('erich', 'nam trung niên (chuyên gia)'), '山下和也': ('adriany', 'nam trẻ'),
 '刘小姐': ('sage', 'nữ trẻ'), '钱先生': ('siqi', 'nam trung niên'), '李女士': ('stella', 'nữ trung niên'),
}
NARR = 'jill'      # dẫn truyện (chú thích sân khấu trong ngoặc), câu hướng dẫn lặp lại ở mọi bài (cố định để file dùng chung nhất quán)
MONO = ('susan', 'adriany')   # đoạn độc thoại/bài đăng không rõ người nói: luân phiên nữ – nam theo khối
F_POOL = ['nu1', 'bobo', 'anna', 'shan', 'xiaoxi', 'julia', 'willow', 'susan']
M_POOL = ['nam1', 'nam2', 'anson', 'jun', 'lan', 'liuping', 'julian']
SWITCH = 140       # fz/ld: đổi giọng nam↔nữ tại ranh giới câu sau khi đã đọc ≥ ngần này chữ

SPK = re.compile(r'^([^\s：:（(，。！？]{1,8})[：:]')
def assign(items, LONG_PREFIX='sents/'):
    """Gán item['voice'] cho mọi mục bài khoá ('t'). Trả về thống kê."""
    by = {}
    for i in items:
        if i['kind'] == 't': by.setdefault((i['book'], i['lesson']), []).append(i)
    for (b, n), L in sorted(by.items()):
        if b == 'ky':
            cur = None; lastblk = None; blkno = {}; k = 0
            for i in L:
                blk = i.get('blk', 0)
                if blk != lastblk: cur = None; lastblk = blk
                t = i['text']; m = SPK.match(t)
                if t.startswith('（') and t.endswith('）'): v = NARR; cur = None
                elif m and m.group(1) in CHAR: cur = m.group(1); v = CHAR[cur][0]
                elif cur: v = CHAR[cur][0]
                else:
                    if blk not in blkno: blkno[blk] = len(blkno)
                    v = MONO[blkno[blk] % 2] if sum(1 for x in L if x.get('blk', 0) == blk) >= 3 else NARR
                i['voice'] = v; i['speaker'] = cur
        else:
            f = F_POOL[(n * 3) % len(F_POOL)]; m_ = M_POOL[(n * 2 + (1 if b == 'ld' else 0)) % len(M_POOL)]
            first = f if n % 2 else m_; second = m_ if n % 2 else f
            cur_v = first; acc = 0
            for i in L:
                i['voice'] = cur_v; acc += len(i['text'])
                if acc >= SWITCH: cur_v = second if cur_v == first else first; acc = 0
    # câu dài dùng chung giữa các bài → một giọng cố định
    shared = {}
    for i in items:
        if i['kind'] == 't' and i['file'].startswith(LONG_PREFIX): shared.setdefault(i['file'], []).append(i)
    for f, L in shared.items():
        if len({(x['book'], x['lesson']) for x in L}) > 1:      # chỉ khi cùng một câu xuất hiện ở ≥2 bài
            for x in L: x['voice'] = NARR
    return by
