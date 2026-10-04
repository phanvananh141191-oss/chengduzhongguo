# -*- coding: utf-8 -*-
ANS = {
 0: dict(guard='什么打乒乓球用的球拍', show=[
   ("他是我的朋友里<b>数</b>做事<b>最</b>认真的。", "Trong các bạn tôi, anh ấy là người làm việc nghiêm túc nhất."),
   ("我的同学中，<b>数</b>王小力<b>最</b>幽默。", "Trong các bạn học của tôi, Vương Tiểu Lực hài hước nhất."),
   ("这么多人中，<b>数</b>那个大高个儿太极拳打得最好。", "Trong nhiều người thế này, anh chàng cao kều kia đánh Thái cực quyền hay nhất."),
   ("这几只小猫里，<b>数</b>那只黄的最顽皮。", "Trong mấy con mèo nhỏ này, con màu vàng nghịch nhất.")], note='Đáp án gợi ý (mẫu: 在…里/中，数……最……).'),
 1: dict(guard='我心里别提多高兴了', show=[
   ("我学会了做很多中餐，什么包子啦，饺子啦，麻婆豆腐啦，都会做。", "Tôi đã học làm nhiều món Trung Quốc: bánh bao, sủi cảo, đậu phụ Tứ Xuyên… món nào cũng biết làm."),
   ("我去超市买了很多东西，什么洗发水啦，卫生纸啦，笔啦，牙膏啦，什么都买了。", "Tôi đi siêu thị mua nhiều thứ: dầu gội, giấy vệ sinh, bút, kem đánh răng… cái gì cũng mua."),
   ("我什么书都爱看，什么经济啦，哲学啦，历史啦，文学啦，都喜欢。", "Sách gì tôi cũng thích đọc: kinh tế, triết học, lịch sử, văn học… đều thích."),
   ("跟“看”有关的词语很多，什么张望啦，打量啦，盯啦，瞧啦，远望啦，都是。", "Từ liên quan đến “看” rất nhiều: ngóng, nhìn kỹ, nhìn chằm chằm, nhìn, nhìn xa… đều thế."),
   ("那儿离学校远，可是交通很方便，什么地铁啦，公共汽车啦，打车啦，应有尽有。", "Chỗ đó xa trường nhưng giao thông tiện: tàu điện ngầm, xe buýt, taxi… đều có."),
   ("我们学校的社团种类很多，什么戏剧啦，体育啦，音乐啦，什么都有。", "Câu lạc bộ ở trường chúng tôi rất đa dạng: kịch, thể thao, âm nhạc… cái gì cũng có.")], note='Đáp án gợi ý (mẫu: 什么……啦，(什么)……啦，都……).'),
 2: dict(guard='住在一个大院里', show=[
   ("A：这次旅游感觉怎么样？ B：<b>别提多开心了</b>。", "Chuyến du lịch này thấy thế nào? — Vui không thể tả."),
   ("A：那里的秋天一定很美吧？ B：<b>别提多美了</b>，<b>漫山遍野的红叶，像着了火一样</b>。", "Mùa thu ở đó chắc đẹp lắm? — Đẹp khỏi nói, lá đỏ khắp núi non như bốc lửa."),
   ("B：你要是学会用中国人理解汉语词汇的方法学汉语，<b>别提多轻松了</b>。", "Nếu bạn học tiếng Hán theo cách người Trung Quốc hiểu từ vựng, sẽ nhẹ nhàng không thể tả."),
   ("B：刚来的时候，<b>我想家想得别提多难受了</b>，现在好多了。", "Lúc mới đến, tôi nhớ nhà đến khó chịu vô cùng, bây giờ đỡ nhiều rồi.")], note='Đáp án gợi ý (別提多A了: A đến mức không tả nổi).'),
 3: dict(guard='对此,你怎么看', show=[
   ("失眠了，我躺了一夜，<b>睡也睡不着</b>。", "Mất ngủ, tôi nằm cả đêm mà ngủ cũng không ngủ được."),
   ("我想听演讲，可是有考试，<b>去也去不了</b>。", "Tôi muốn nghe diễn thuyết, nhưng có thi, đi cũng không đi được."),
   ("楼上的音乐那么响，我<b>睡也睡不着</b>。", "Nhạc trên lầu to thế, tôi ngủ cũng không ngủ nổi."),
   ("这首歌的歌词那么长，我<b>记也记不住</b>。", "Lời bài hát dài thế, tôi nhớ cũng không nhớ nổi."),
   ("“儿”不好读，我<b>读也读不好</b>。", "Chữ “儿” khó đọc, tôi đọc mãi cũng không đọc tốt được."),
   ("那不是普通话，我<b>听也听不懂</b>。", "Đó không phải tiếng phổ thông, tôi nghe cũng không hiểu.")], note='Đáp án gợi ý (V也V不C).'),
 4: dict(guard='对此', show=[
   ("公司决定周末加班，对此，只有他没意见。", "Công ty quyết định tăng ca cuối tuần, về việc này chỉ có anh ấy là không có ý kiến."),
   ("网上买的衣服材质、颜色常和图片不一样，对此，我不在网店买衣服了，改去实体店。", "Quần áo mua mạng thường khác ảnh về chất liệu, màu sắc; vì thế tôi không mua ở shop online nữa mà chuyển sang cửa hàng thật."),
   ("我的电脑经常出问题，对此，我很烦恼。", "Máy tính của tôi hay gặp lỗi, về việc này tôi rất phiền não."),
   ("老年人爱买便宜东西，年轻人觉得是浪费，对此，我觉得不能一概而论。", "Người già thích mua đồ rẻ, người trẻ cho là lãng phí; về điều này tôi thấy không nên cào bằng."),
   ("有人说女司机开车技术不好，对此，她认为这是偏见。", "Có người nói tài xế nữ lái xe kém, về điều này cô cho đó là định kiến."),
   ("有人每天吃很多维生素，医生说过量有害，对此，医生建议在医生指导下服用。", "Có người ngày nào cũng uống nhiều vitamin; bác sĩ nói dùng quá liều có hại, nên chỉ nên dùng dưới sự hướng dẫn của bác sĩ.")], note='Đáp án gợi ý (对此: về việc này).'),
 5: dict(guard='一、字词知识与练习', refill=['铅','锁','银','银','银','钟','钢','钻','钓'], show=[
   ("1 <b>铅</b>笔 · 2 <b>锁</b>好门 · 3 <b>银</b>行 · 4 三个<b>钟</b>头 · 5 <b>钢</b>琴 · 6 <b>钻</b>山洞 · 7 <b>钓</b>鱼", "Các chữ cần điền: 铅 · 锁 · 银 · 钟 · 钢 · 钻 · 钓"),
   ("“想一想” gợi ý: 针、钉、钩、铁、铜、锅、链、镜、钥匙、铃…", "")], note='Đã sửa dữ liệu chấm bài bị lệch ô ở thẻ này.'),
 6: dict(guard='二、参考注释', refill=['丢|失去|没有|没了','丢|失去|没有|没了','失声','遗失|丢失','顾此失彼|因小失大|贪小失大','丢失|遗失','丢失|遗失','失主','隐含','隐私','隐藏','隐瞒','隐瞒','隐瞒'], show=[
   ("“失”的意思是：丢、失去、没有。", "“失” nghĩa là: mất, đánh mất, không còn."),
   ("(1) 兴奋得<b>失声</b> · (2) <b>遗失/丢失</b> · (3) 不能<b>顾此失彼/因小失大</b> · (4) 我<b>丢失/遗失</b>的 · <b>失主</b>", "Điền: 失声 · 遗失/丢失 · 顾此失彼 · 丢失 · 失主"),
   ("(二) (1) <b>隐含</b> · (2) <b>隐私</b> · (3) <b>隐藏</b> · (4) <b>隐瞒</b>", "Điền: 隐含 · 隐私 · 隐藏 · 隐瞒")], note='Đã bổ sung ô còn thiếu và sửa dữ liệu chấm bài ở thẻ này.'),
 13: dict(guard='九、写一写', show=[
   ("Dàn ý gợi ý (≥280 chữ): ① 胡同里的<b>玩伴</b>、<b>乐在其中</b>；② 邻里没有<b>隐私</b>，大院里的事想<b>瞒也瞒不住</b>；③ 有人<b>在意</b><b>面子</b>，有人<b>单独</b>住更自在；④ 你的看法：胡同生活的<b>烦恼</b>与乐趣，各有利弊。", "")],
   note='Bài viết tự do — chỉ là dàn ý gợi ý.'),
 14: dict(guard='练习', show=[
   ("Câu 1: trả lời theo bài đọc (nơi xảy ra câu chuyện). Câu 2–3: nêu ý kiến riêng (ví dụ: bình tĩnh thương lượng, nhường nhịn để giữ hòa khí hàng xóm). Câu 4–5: tự học.", "")],
   note='Bài đọc hiểu mở — đáp án mang tính gợi ý.'),
 15: dict(guard='十一、拓展学习', show=[("Bài mở rộng (tìm bài về hutong, nghe và hát bài 《前门情思大碗茶》) — không có đáp án cố định.", "")], note='Bài mở rộng/tự tìm hiểu.'),
}
