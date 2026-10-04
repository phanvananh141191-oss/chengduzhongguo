# -*- coding: utf-8 -*-
ANS = {
 1: dict(guard='冼星海很兴奋', show=[
   ("这次旅行，我写下了自己的<b>所见所闻</b>。", "Chuyến đi này tôi đã ghi lại những điều mắt thấy tai nghe."),
   ("他把自己的<b>所学所想</b>都写进了论文。", "Anh ấy đưa cả những điều đã học, đã nghĩ vào luận văn."),
   ("关于这件事，我<b>所知</b>有限。", "Về việc này, hiểu biết của tôi có hạn.")], note='Đáp án gợi ý (các cụm 所见所闻, 所学, 所想, 所感, 所知, 所为…).'),
 2: dict(guard='冼星海连续六天六夜', show=[
   ("这个问题，谁<b>来回答</b>？", "Câu hỏi này, ai trả lời?"),
   ("老师，让<b>我来修吧</b>，我以前学过修电脑。", "Thầy ơi, để em sửa, trước đây em từng học sửa máy tính."),
   ("咱们今年暑假旅游，<b>你来定个地方</b>怎么样？", "Hè này chúng ta đi du lịch, bạn chọn địa điểm nhé?"),
   ("你总说我不行，那<b>你来试试</b>。", "Bạn cứ nói tôi không được, vậy bạn thử đi.")], note='Đáp án gợi ý (来 + V).'),
 3: dict(guard='第一次走上舞台', show=[
   ("大家都在那儿聊天儿，他却坐在一旁<b>不言不语</b>。", "Mọi người đang trò chuyện, anh lại ngồi một bên không nói không rằng."),
   ("下课了，很快同学们都走了，她才<b>不慌不忙</b>地离开教室。", "Tan học, các bạn đi hết, cô mới thong thả rời lớp."),
   ("中国人爱吃饺子，特别是北方人。过年吃饺子，过节吃饺子，<b>不吃饺子就不像过节</b>。", "Người Trung Quốc thích ăn sủi cảo, nhất là người miền Bắc. Tết ăn, lễ ăn, không ăn sủi cảo thì không giống lễ.")], note='Đáp án gợi ý (不A不B).'),
 4: dict(guard='V + 遍', show=[
   ("这部电影上映没几天就<b>火遍</b>了全国各地。", "Bộ phim này chiếu chưa mấy ngày đã nổi khắp cả nước."),
   ("乘车卡没了，我把能找的地方都<b>找遍</b>了，也没找到。", "Mất thẻ đi xe, tôi tìm khắp mọi nơi có thể mà không thấy."),
   ("来中国不到半年，中国最著名的古镇我都<b>玩儿遍</b>了。", "Đến Trung Quốc chưa đầy nửa năm, các cổ trấn nổi tiếng nhất tôi đều đã đi khắp.")], note='Đáp án gợi ý (V + 遍).'),
 5: dict(guard='一、字词知识与练习', show=[
   ("哄 hǒng：哄骗、劝逗。词语：哄孩子、哄骗；(hōng) 哄堂大笑。", "Lừa gạt, dỗ dành. Từ: dỗ trẻ, lừa; cả phòng cười ầm."),
   ("呛 qiāng/qiàng：气或水进入气管引起难受。词语：呛水、呛着、呛人。", "Sặc; cay nồng. Từ: sặc nước, bị sặc, hăng cay."),
   ("咨 zī：询问、商量。词语：咨询、咨文。", "Hỏi ý kiến, bàn bạc. Từ: tư vấn, quốc thư."),
   ("咸 xián：含盐多；全、都。词语：咸菜、咸味、老少咸宜。", "Mặn; đều. Từ: dưa muối, vị mặn, già trẻ đều hợp.")], note='Đáp án gợi ý (tra từ điển).'),
 6: dict(guard='二、查询字源', refill=['虫灾|蝗灾','雪灾','幸灾乐祸','天灾人祸','家史','发展史','历史博物馆','史书'], show=[
   ("(一) (1) <b>虫灾/蝗灾</b> · (2) <b>雪灾</b> · (3) <b>幸灾乐祸</b> · (4) <b>天灾人祸</b>", "Điền: nạn sâu bệnh / nạn châu chấu · nạn tuyết · hả hê trước tai họa · thiên tai nhân họa"),
   ("(二) (1) <b>家史</b> · (2) <b>发展史</b> · (3) <b>历史博物馆</b> · (4) <b>史书</b>", "Điền: gia sử · lịch sử phát triển · bảo tàng lịch sử · sử sách")], note='Đáp án gợi ý, có chấm tự động theo các từ trên.'),
 7: dict(guard='三、选择合适的词语填空', refill=['完美','魅力','眠','百感交集','共鸣','感染力','典范','经久不衰'], show=[
   ("一部<b>完美</b>之作 · 古琴的<b>魅力</b> · 长夜不<b>眠</b> · 令人<b>百感交集</b>之余，不禁产生情感<b>共鸣</b> · 极具<b>感染力</b> · 无人超越的<b>典范</b> · 受到观影者<b>经久不衰</b>的赞美", "Điền: 完美 · 魅力 · 眠 · 百感交集 · 共鸣 · 感染力 · 典范 · 经久不衰")], note='Đáp án suy ra từ ngữ cảnh và bảng từ.'),
 8: dict(guard='四、用指定词语完成句子', show=[
   ("如果这场<b>战争爆发</b>，会有成千上万的人失去家园。", "Nếu cuộc chiến này nổ ra, hàng nghìn hàng vạn người sẽ mất nhà."),
   ("把我们学到的知识跟<b>实际结合起来</b>，才能真正变成自己的能力。", "Kết hợp kiến thức đã học với thực tế mới thật sự trở thành năng lực của mình."),
   ("我<b>志愿加入环保</b>组织，为保护地球做些力所能及的努力。", "Tôi tình nguyện gia nhập tổ chức bảo vệ môi trường, làm những việc trong khả năng để bảo vệ Trái đất."),
   ("一场音乐会<b>激发了</b>他对流行音乐的兴趣，从此，他开始研究并尝试作曲。", "Một buổi hòa nhạc khơi dậy hứng thú của anh với nhạc đại chúng, từ đó anh bắt đầu nghiên cứu và thử sáng tác."),
   ("小时候，最<b>盼望过年</b>，因为过年有新衣服穿，有好吃的，犯错误也不会挨批评。", "Hồi nhỏ, mong Tết nhất, vì Tết có áo mới, đồ ngon, mắc lỗi cũng không bị mắng."),
   ("今年夏天气温<b>相对往年偏高</b>，要注意防暑。", "Mùa hè năm nay nhiệt độ tương đối cao hơn mọi năm, cần chú ý phòng nóng."),
   ("在历史的长河中，人的生命<b>十分短促</b>。", "Trong dòng chảy lịch sử, đời người rất ngắn ngủi."),
   ("有人把这件事发到网上，<b>引起了</b>热议。", "Có người đăng việc này lên mạng, gây ra bàn luận sôi nổi.")], note='Đáp án gợi ý.'),
 9: dict(guard='五、用指定词语或格式完成对话', show=[
   ("你动作优美，感情真实，<b>整场表演非常完美</b>。", "Động tác đẹp, tình cảm chân thật, cả buổi biểu diễn rất hoàn mỹ."),
   ("工作还是读研，<b>我正处于两难之中</b>，一直拿不定主意。", "Đi làm hay học cao học, tôi đang ở thế khó xử, mãi không quyết được."),
   ("<b>你的短视频创作得真好</b>，有时间也教教我吧。", "Video ngắn bạn làm hay thật, khi rảnh dạy tôi với nhé."),
   ("这人讲得<b>不清不楚</b>，不清楚他在说什么。", "Người này nói không rõ ràng, chẳng hiểu ông ấy nói gì."),
   ("我从小就喜欢植物，还立下过誓言，<b>要认遍世界上所有的植物</b>。", "Từ nhỏ tôi đã thích thực vật, còn từng thề sẽ nhận biết hết thực vật trên đời."),
   ("她特别善于表现人物内心，能把<b>人物的感情表现得淋漓尽致</b>。", "Cô rất giỏi thể hiện nội tâm nhân vật, diễn tả tình cảm nhân vật thật trọn vẹn."),
   ("我在网上查过，说<b>互联网诞生于</b>1969年。", "Tôi tra trên mạng, nói Internet ra đời năm 1969."),
   ("汉语叫“说唱”，<b>它是一种音乐表演形式</b>，就是有节奏地说话。", "Tiếng Hán gọi là “说唱”, là một hình thức biểu diễn âm nhạc, tức nói có nhịp điệu.")], note='Đáp án gợi ý.'),
 10: dict(guard='六、用指定词语改写句子', show=[
   ("时刻认识到<b>自身</b>的不足才能不断进步。", "Luôn nhận ra thiếu sót của bản thân mới có thể không ngừng tiến bộ."),
   ("我们俩说好了，明早七点<b>一同</b>打车去机场。", "Hai chúng tôi hẹn xong, 7 giờ sáng mai cùng bắt taxi ra sân bay."),
   ("多年未见的老同学再次相见，<b>百感交集</b>，有太多的话要说。", "Bạn học cũ lâu năm gặp lại, trăm mối cảm xúc ngổn ngang, có quá nhiều điều muốn nói."),
   ("他大声地、有感情地给全班同学<b>朗诵</b>了一首自己写的新诗。", "Cậu ấy đọc diễn cảm bài thơ mới do mình sáng tác cho cả lớp nghe."),
   ("她的作品写作<b>手法</b>独特，给人强烈的画面感，很吸引人。", "Thủ pháp viết trong tác phẩm của cô độc đáo, gợi hình ảnh mạnh, rất cuốn hút."),
   ("他的笑声很有<b>感染力</b>，往往能让身旁的人也开心起来。", "Tiếng cười của anh rất có sức lan tỏa, thường khiến người bên cạnh cũng vui lên."),
   ("演出结束，台下一下子<b>爆发</b>出暴风雨般的掌声。", "Buổi diễn kết thúc, dưới khán đài bỗng bùng lên tràng pháo tay như bão.")], note='Đáp án gợi ý.'),
 11: dict(guard='七、在理解课文', show=[
   ("Câu 1: nghe trọn tác phẩm rồi nêu cảm nhận — bài mở, không có đáp án cố định.", ""),
   ("Câu 2 (tóm lược theo đoạn bài khóa): 《黄河大合唱》分为八个乐章，各乐章相对独立；音乐形式多样（合唱、独唱、配乐诗朗诵、对唱、轮唱）；中西乐器共同演奏，交响乐与中国民族音乐结合，影响了后来的大合唱和其他音乐创作。", "Gồm tám chương, tương đối độc lập; hình thức đa dạng (hợp xướng, đơn ca, ngâm thơ có nhạc đệm, song ca, canon); nhạc cụ Tây và dân tộc cùng tham gia, giao hưởng kết hợp âm nhạc dân tộc, ảnh hưởng đến các đại hợp xướng và sáng tác âm nhạc sau này.")], note='Tóm lược theo đoạn bài khóa trong bài.'),
 12: dict(guard='八、写一写', show=[("Bài viết tự do (300–320 chữ): giới thiệu bài hát/ca sĩ bạn thích — nêu tên, vì sao thích, cảm nhận khi nghe. Không có đáp án cố định.", "")], note='Bài viết tự do.'),
 13: dict(guard='九、阅读短文', show=[
   ("1. 道理：最好的老师不一定是人，能触动人心的情、景、事（大自然与生活）就是最好的老师；技艺要靠感悟，才能更上一层楼。", "Đạo lý: người thầy tốt nhất không nhất thiết là người; cảnh, tình, việc lay động lòng người (thiên nhiên và cuộc sống) chính là người thầy tốt nhất; kỹ nghệ cần sự cảm ngộ mới tiến thêm một bậc."),
   ("Câu 2–4: chia sẻ câu chuyện của riêng bạn / bài tự học.", "")], note='Đáp án tóm lược theo bài đọc.'),
 14: dict(guard='十、拓展学习', show=[
   ("高山流水：比喻知音难觅，或乐曲高妙。", "Cao sơn lưu thủy: ví tri âm khó tìm, hoặc nhạc khúc cao diệu."),
   ("余音绕梁：形容歌声、乐声优美，余音久久不散。", "Dư âm vấn vương: tiếng hát tiếng nhạc hay, âm vang lưu mãi."),
   ("滥竽充数：没有真才实学的人混在行家里凑数。", "Lạm vu sung số: người không có tài thật lẫn vào giữa người giỏi cho đủ số."),
   ("对牛弹琴：比喻对不懂道理的人讲道理，白费力气。", "Đàn gảy tai trâu: nói lý với người không hiểu, uổng công.")], note='Nghĩa gợi ý của các thành ngữ.'),
}
