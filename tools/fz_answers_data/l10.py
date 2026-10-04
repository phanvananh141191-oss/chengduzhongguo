# -*- coding: utf-8 -*-
ANS = {
 1: dict(guard='在这去来之间', show=[
   ("阿姨，您<b>尽管尝</b>，这么新鲜的西瓜我保证您吃了还来买。", "Cô cứ nếm thử đi, dưa hấu tươi thế này, cháu đảm bảo cô ăn xong sẽ còn đến mua."),
   ("你想来<b>尽管来</b>，我什么时间都方便。", "Bạn muốn đến thì cứ đến, lúc nào tôi cũng tiện."),
   ("写作文没什么限制，按照自己的想法，<b>尽管写</b>。", "Viết văn không có hạn chế gì, cứ viết theo ý mình."),
   ("<b>尽管去</b>，别犹豫的，这样的机会多难得啊。", "Cứ đi đi, đừng do dự, cơ hội thế này khó có biết bao.")], note='Đáp án gợi ý (尽管 = cứ việc).'),
 2: dict(guard='我发现太阳它居然有脚', refill=['生与死之间','大小之间','两难之间','青山绿水之间'], show=[
   ("(1) 在<b>生与死之间</b> · (2) 在<b>大小之间</b>做选择 · (3) <b>两难之间</b>的选择 · (4) 回到<b>青山绿水之间</b>", "Điền: giữa sống và chết · giữa lớn và nhỏ · giữa hai điều khó · giữa non xanh nước biếc")], note='Đáp án suy ra từ ngữ cảnh và bảng từ.'),
 3: dict(guard='既然什么都带不走', refill=['(3)|3'], show=[
   ("Câu không chứa đồng vị ngữ: <b>(3)</b> 朋友那里有很多关于中国历史的书。", "Câu (3) không có cụm đồng vị; (1) 首都北京, (2) 春夏秋冬四季, (4) 游戏这东西 đều là cụm đồng vị.")], note='Đáp án gợi ý.'),
 4: dict(guard='既然', show=[
   ("既然选择了这个专业，<b>就要好好学下去</b>。", "Đã chọn ngành này thì phải học cho tốt."),
   ("明天既然有雨，<b>那就不去爬山了</b>。", "Mai đã có mưa thì thôi không đi leo núi nữa."),
   ("<b>既然你今天没有时间</b>，会议时间也可以改到明天。", "Nếu hôm nay bạn không có thời gian thì giờ họp cũng có thể dời sang ngày mai."),
   ("<b>既然大家都不想做饭</b>，就叫个外卖吧。", "Đã mọi người đều không muốn nấu thì gọi đồ ăn ngoài đi.")], note='Đáp án gợi ý.'),
 5: dict(guard='一、字词知识与练习', show=[
   ("窜 cuàn：逃跑、乱跑。词语：逃窜、乱窜、窜改。", "Chạy trốn, chạy loạn. Từ: bỏ chạy, chạy tán loạn, sửa đổi bừa bãi."),
   ("窍 qiào：孔洞；关键。词语：窍门、七窍、一窍不通。", "Lỗ; mấu chốt. Từ: bí quyết, thất khiếu, hoàn toàn mù tịt."),
   ("究 jiū：追查、深入研究。词语：研究、究竟、追究。", "Truy cứu, nghiên cứu sâu. Từ: nghiên cứu, rốt cuộc, truy cứu."),
   ("窥 kuī：偷看。词语：窥视、窥探、管窥。", "Nhìn trộm. Từ: dòm ngó, thăm dò, cái nhìn hạn hẹp.")], note='Đáp án gợi ý (tra từ điển).'),
 6: dict(guard='二、参考注释', refill=['小|少|细小|轻微','微薄','稍微','微不足道|微小','微型','甘愿|心甘情愿','誓不甘休|决不甘休','不甘'], show=[
   ("“微”的意思是：细小、轻微；小、少。", "“微” nghĩa là: nhỏ bé, nhẹ; ít."),
   ("(一) (1) <b>微薄</b> · (2) <b>稍微</b> · (3) <b>微不足道</b> · (4) <b>微型</b>", "Điền: 微薄 · 稍微 · 微不足道 · 微型"),
   ("(二) (1) <b>甘愿</b> · (2) <b>誓不甘休</b> · (3) <b>不甘</b>", "Điền: 甘愿 · 誓不甘休 · 不甘")], note='Đáp án gợi ý, có chấm tự động theo các từ trên.'),
 7: dict(guard='三、选择合适的词语填空', refill=['的确','溜','悄无声息','既然','白白','无奈','叹息','盲目','面临','一去不复返'], show=[
   ("它<b>的确</b>老实得出奇 · <b>溜</b>出去就是一天一夜 · <b>悄无声息</b> · <b>既然</b>这里有老鼠 · 不是<b>白白</b>在你家吃饭 · 生活中的<b>无奈</b>发出<b>叹息</b> · <b>盲目</b>地让自己身处险境 · 万一<b>面临</b>危险 · <b>一去不复返</b>了", "Điền: 的确 · 溜 · 悄无声息 · 既然 · 白白 · 无奈 · 叹息 · 盲目 · 面临 · 一去不复返")], note='Đáp án suy ra từ ngữ cảnh và bảng từ.'),
 8: dict(guard='四、用指定词语完成句子', show=[
   ("这个喜剧电影从头到尾一直让观众<b>笑个不止</b>。", "Bộ phim hài này từ đầu đến cuối khiến khán giả cười không ngớt."),
   ("我<b>的确不太清楚这件事</b>，要不你再问问别人？", "Tôi quả thật không rõ chuyện này, hay bạn hỏi thêm người khác?"),
   ("<b>既然你不想跟我们一起去</b>，那我就买我自己的火车票了。", "Đã bạn không muốn đi cùng thì tôi mua vé tàu của riêng mình."),
   ("<b>你这么匆忙</b>，是有什么急事吗？", "Bạn vội vàng thế, có việc gấp à?"),
   ("你<b>回想一下</b>，你觉得什么是这四年最让你难忘的？", "Bạn nhớ lại xem, điều gì khiến bạn khó quên nhất bốn năm qua?"),
   ("<b>你怎么悄无声息地就走了</b>？不跟大家打声招呼吗？", "Sao bạn lặng lẽ đi mất thế? Không chào mọi người à?"),
   ("你就这样<b>白白跑一趟</b>，到了博物馆才知道今天人家休息，<b>白白浪费了半天时间</b>。", "Bạn cứ thế chạy uổng một chuyến, đến bảo tàng mới biết hôm nay nghỉ, uổng phí nửa ngày.")], note='Đáp án gợi ý.'),
 9: dict(guard='五、用指定词语或格式完成对话', show=[
   ("<b>唉，这么晚了</b>，你们怎么还不走？", "Ôi, muộn thế này rồi sao các bạn còn chưa đi?"),
   ("<b>我中途悄悄溜走了</b>。", "Tôi lén chuồn đi giữa chừng."),
   ("<b>咱们是朋友，朋友之间还客气什么</b>。", "Chúng ta là bạn, bạn bè với nhau khách sáo gì."),
   ("<b>第一次面临这么多观众</b>，我可紧张了。", "Lần đầu đối diện nhiều khán giả thế, tôi căng thẳng lắm."),
   ("你想看什么，<b>尽管拿去看</b>。", "Bạn muốn xem gì cứ cầm đi xem."),
   ("<b>不禁想起了</b>小时候烤土豆吃的情景。", "Không khỏi nhớ đến cảnh nướng khoai tây ăn hồi nhỏ."),
   ("<b>既然你不去，怎么不早说</b>？", "Đã không đi thì sao không nói sớm?"),
   ("你们<b>就这样白白走了，甘心吗</b>？", "Các bạn cứ thế đi uổng công, có cam lòng không?")], note='Đáp án gợi ý.'),
 10: dict(guard='六、用指定词语改写句子', show=[
   ("面对突如其来的大火，她<b>大脑一片空白</b>，只是呆呆地望着着火的地方。", "Trước đám cháy bất ngờ, đầu óc cô trống rỗng, chỉ ngây ra nhìn nơi bốc cháy."),
   ("这件事<b>的确</b>是真的，请你相信我。", "Chuyện này đúng là thật, xin bạn tin tôi."),
   ("和女朋友分手了，他很伤心，<b>盲目地</b>在大街上走着。", "Chia tay bạn gái, anh rất buồn, bước đi vô định trên phố."),
   ("我就是这世界上<b>芸芸众生</b>中的一员。", "Tôi chỉ là một trong muôn vàn người bình thường trên đời."),
   ("节日的灯光把城市照得<b>如同</b>白天一样。", "Ánh đèn lễ hội chiếu thành phố sáng như ban ngày."),
   ("没想到朋友<b>悄无声息地</b>走到了他背后。", "Không ngờ bạn lặng lẽ đi đến sau lưng anh."),
   ("燕子找到食物，<b>匆忙</b>飞回家，喂它的孩子们去了。", "Én tìm được thức ăn, vội vã bay về nhà cho con ăn.")], note='Đáp án gợi ý.'),
 12: dict(guard='八、参考提示', show=[
   ("<b>的确如此</b>，读完我也进行了反思，过去浪费了太多时间。（表示肯定）", "Đúng vậy, đọc xong tôi cũng suy ngẫm, trước đây đã lãng phí quá nhiều thời gian."),
   ("<b>唉，没办法呀</b>，我也一样，以前年龄小，没觉得时间宝贵。（表示无奈）", "Ôi, biết làm sao được, tôi cũng vậy, hồi nhỏ không thấy thời gian quý."),
   ("浪费了那么多时间，现在想想，<b>实在令人遗憾</b>。（表示遗憾）", "Lãng phí nhiều thời gian thế, nghĩ lại thật đáng tiếc."),
   ("<b>是啊，太可惜了</b>，时间似流水……（表示遗憾）", "Phải, tiếc quá, thời gian như nước chảy…"),
   ("<b>既然时间已经一去不复返</b>，遗憾也没用，<b>那就从现在开始珍惜吧</b>。（表示推论）", "Đã thời gian không trở lại thì tiếc cũng vô ích, vậy từ bây giờ hãy trân trọng."),
   ("可是，<b>我从未真正珍惜过时间</b>，我都不知道怎么珍惜。（表示否定）", "Nhưng tôi chưa từng thật sự trân trọng thời gian, tôi chẳng biết trân trọng thế nào.")], note='Đáp án gợi ý (đúng chức năng ghi trong ngoặc).'),
 13: dict(guard='九、写一写', show=[("Dàn ý gợi ý (280–300 chữ): ① 时间<b>如同</b>流水，<b>一去不复返</b>；② <b>既然</b>时间无法挽回，就要珍惜；③ <b>尽管</b>…也…；④ 在<b>过去和未来之间</b>(AB之间)，把握现在。", "")], note='Bài viết tự do — chỉ là dàn ý gợi ý.'),
 14: dict(guard='十、阅读短文', show=[
   ("1. 因为时间对每个人都一样：不管富人穷人、老人孩子，它给每个人的分分秒秒都没有一丝一毫的差别。", "Vì thời gian với mọi người đều như nhau: dù giàu hay nghèo, già hay trẻ, từng phút từng giây nó dành cho mỗi người không khác biệt chút nào."),
   ("2. 选择吃喝玩乐的人，时间一到就随时间消失；选择不断超越自我、服务社会的人，思想和精神永存人间。", "Người chọn ăn chơi thì hết thời gian là biến mất; người chọn không ngừng vượt lên bản thân và phục vụ xã hội thì tư tưởng, tinh thần còn mãi."),
   ("Câu 3–4: bài tự học.", "")], note='Đáp án tóm lược theo bài đọc.'),
 15: dict(guard='十一、拓展学习', show=[("Bài mở rộng (chia sẻ cảm nhận về thời gian, danh ngôn bằng tiếng mẹ đẻ, giới thiệu một bài viết về thời gian) — không có đáp án cố định.", "")], note='Bài mở rộng.'),
}
