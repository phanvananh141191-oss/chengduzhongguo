# -*- coding: utf-8 -*-
"""Dữ liệu bổ sung fz bài 4 (tr.52–68) và bài 8 (tr.123–138), đọc từ ảnh trang sách bạn gửi (04/10/2026).
Hán = nguyên văn trang sách; Việt = biên soạn (nguồn không có bản dịch)."""

# ───────────────────────── BÀI 4 ─────────────────────────
L4_TEXT = [  # (hán, việt) theo đoạn · tr.54–56
 ("登机后发现，我前面坐了一对上了年纪的老夫妇，老两口儿被一条过道¹隔开了。飞机起飞后，老奶奶不一会儿就睡着了，还张着嘴呼吸。",
  "Sau khi lên máy bay, tôi nhận thấy phía trước mình có một cặp vợ chồng già ngồi, hai ông bà bị một lối đi¹ ngăn cách. Sau khi máy bay cất cánh, bà cụ chẳng mấy chốc đã ngủ thiếp đi, miệng còn há ra thở."),
 ("很快，过道这面的老爷爷看到了老伴儿²张嘴呼吸的睡相，赶忙从口袋里掏出手机，迫切地对准老伴儿的侧脸开始拍照。拍照的声音引来了周围乘客的注意，可那老奶奶睡得很沉，拍照的动静再大也弄不醒她；只见她把头转向另一边，嘴张得更大了，继续呼呼大睡。",
  "Rất nhanh, ông cụ ở bên này lối đi nhìn thấy dáng ngủ há miệng thở của người bạn đời² của mình, vội móc điện thoại trong túi ra, sốt ruột chĩa vào gương mặt nghiêng của bà để chụp ảnh. Tiếng chụp ảnh thu hút sự chú ý của hành khách xung quanh, nhưng bà cụ ngủ rất say, tiếng động chụp ảnh có lớn đến mấy cũng không đánh thức được bà; chỉ thấy bà quay đầu sang phía bên kia, miệng há to hơn, tiếp tục ngủ khò khò."),
 ("见老奶奶没什么反应，老先生站起身，打开头顶的行李舱³，从背包里取出一副老花镜。我本以为他是要拿眼镜自己用，没想到老先生站到老奶奶前面，仔细打量了她几秒钟，然后一边四处张望，一边装作若无其事地把老花镜戴到了老伴儿头上。此时，飞机上已经不止我一人注意到老先生的搞笑⁴行为——有人开始偷笑，还有人目不转睛地盯着这老两口儿，期待着老先生的下一步行动。",
  "Thấy bà cụ chẳng có phản ứng gì, ông cụ đứng dậy, mở khoang hành lý³ trên đầu, lấy từ ba lô ra một cặp kính lão. Tôi vốn tưởng ông định lấy kính cho mình dùng, không ngờ ông đứng trước mặt bà, ngắm nghía bà vài giây, rồi vừa ngó nghiêng khắp nơi, vừa làm bộ như không có chuyện gì mà đeo cặp kính lão lên đầu bà. Lúc này, trên máy bay không chỉ mình tôi để ý đến hành động pha trò⁴ của ông cụ — có người bắt đầu cười thầm, còn có người chằm chằm nhìn đôi vợ chồng già, mong chờ bước tiếp theo của ông."),
 ("老爷子内心一定在说：看我的了！只见他坐回位子上，从前面的口袋里掏出一顶圣诞帽，他先举起帽子对准老奶奶的头，以确认帽子戴在她头上是否合适，然后悄悄地起身，把圣诞帽轻轻地套在老伴儿头上。但这次的动静太大，老奶奶转了转脑袋，醒了过来。老奶奶不醒不知道，一醒就发现眼前多了一层镜片，又抬眼向上看了看，可能她感觉到头上暖和了许多。这时围观的乘客已经有人乐出了声，老奶奶也终于意识到，这些都是自己先生的恶作剧⁵。很快，那一整排的乘客都笑了起来——原来他们互相都认识，这次是一大家人一起出行。",
  "Trong lòng ông cụ chắc hẳn đang nói: Cứ xem tôi đây! Chỉ thấy ông ngồi lại chỗ, móc từ túi phía trước ra một chiếc mũ Giáng sinh; trước hết ông giơ mũ lên áp vào đầu bà để xác nhận đội lên đầu bà có vừa không, rồi lặng lẽ đứng dậy, nhẹ nhàng chụp mũ Giáng sinh lên đầu người bạn đời. Nhưng lần này động tĩnh quá lớn, bà cụ xoay xoay đầu, tỉnh dậy. Bà không tỉnh thì không biết, vừa tỉnh đã thấy trước mắt có thêm một lớp mắt kính, lại ngước mắt lên nhìn, có lẽ bà thấy trên đầu ấm hơn nhiều. Lúc này đã có hành khách đứng xem bật cười thành tiếng, bà cụ cuối cùng cũng nhận ra, tất cả đều là trò đùa tinh quái⁵ của ông nhà mình. Rất nhanh, cả hàng hành khách đó đều bật cười — hóa ra họ đều quen biết nhau, chuyến đi này là cả đại gia đình cùng đi."),
 ("我想起小时候看英国喜剧《憨豆先生》⁶，其中有一集是憨豆先生身旁坐了一位行动不便的老先生。憨豆先生为了逗他，依次把他的帽子、拐杖，还有自己最爱的泰迪熊⁷都挂在了老先生身上。今天飞机上这位老爷爷的一系列恶搞，简直就是美版《憨豆先生》的拍摄现场，也让我在现场看了一场情景喜剧。",
  "Tôi nhớ hồi nhỏ xem hài kịch Anh 《Mr Bean》⁶, trong đó có một tập Mr Bean ngồi cạnh một cụ già đi lại bất tiện. Để chọc cụ cười, Mr Bean lần lượt treo mũ của cụ, gậy chống, cùng chú gấu bông⁷ mà anh yêu thích nhất lên người cụ. Chuỗi trò chọc phá của ông cụ trên máy bay hôm nay quả thật chẳng khác nào hiện trường quay bản Mỹ của 《Mr Bean》, cũng khiến tôi được xem tận nơi một vở hài tình huống."),
 ("飞机降落后，乘客们纷纷走出机舱⁸，我转身看了一眼刚才那位童心未泯的顽皮老先生和他老伴儿。两个人正有说有笑，互相搀着一起去找洗手间。看到他们幸福的样子，我自己也非常开心。希望等我年过古稀⁹的时候，也还能像这位老先生一样对生活充满热情，对家人充满幽默感¹⁰，而且到时候如果要我去捉弄¹¹别人，我恶搞的方式肯定别出心裁，跟别人的都不一样。",
  "Sau khi máy bay hạ cánh, hành khách lần lượt bước ra khỏi khoang⁸, tôi quay lại nhìn một cái vị cụ ông nghịch ngợm, vẫn còn giữ tâm hồn trẻ thơ lúc nãy và người bạn đời của ông. Hai người đang vừa nói vừa cười, dìu nhau đi tìm nhà vệ sinh. Nhìn dáng vẻ hạnh phúc của họ, bản thân tôi cũng rất vui. Mong rằng khi tôi đến tuổi xưa nay hiếm⁹, tôi cũng vẫn có thể như vị cụ ông này, tràn đầy nhiệt huyết với cuộc sống, tràn đầy óc hài hước¹⁰ với người thân, và đến lúc ấy nếu phải trêu chọc¹¹ người khác, cách chọc phá của tôi chắc chắn sẽ độc đáo, không giống ai."),
]
L4_AUTHOR = ("（选自“一昧 One Way”微信公众号，作者：李天一。有删改）",
             "(Trích từ tài khoản WeChat “一昧 One Way”, tác giả: Lý Thiên Nhất. Có lược bớt.)")
L4_NOTES = [  # (từ, tiêu đề Việt, [(hán, việt)...])
 ("过道", "Lối đi", [("飞机上座位之间空出来的、供前后通行的通道。", "Lối đi chừa ra giữa các hàng ghế trên máy bay, để đi lại phía trước và phía sau.")]),
 ("老伴儿", "Bạn đời (cách gọi vợ chồng già)", [
   ("老年夫妻之间的称呼。", "Cách gọi nhau giữa vợ chồng lớn tuổi."),
   ("夫妻之间的称呼比较正式的有：丈夫、妻子，先生、太太，先生、夫人，爱人。此外还有：老公、老婆，他爸、他妈等。", "Những cách gọi khá trang trọng giữa vợ chồng gồm: 丈夫 (chồng), 妻子 (vợ), 先生 (ông xã), 太太 (bà xã), 先生 (ông), 夫人 (phu nhân), 爱人 (người yêu/vợ chồng). Ngoài ra còn có: 老公 (chồng), 老婆 (vợ), 他爸 (bố nó), 他妈 (mẹ nó), v.v.")]),
 ("行李舱", "Khoang hành lý (luggage compartment)", [("飞机上存放行李的地方。", "Nơi cất hành lý trên máy bay.")]),
 ("搞笑", "Pha trò, làm trò cười", [
   ("动词，指有意做出一些动作或说出可笑的话，让人发笑。", "Động từ, chỉ việc cố ý làm vài động tác hoặc nói những lời buồn cười để người khác bật cười."),
   ("例如：一味搞笑的节目，效果也不会太好。／他特别会搞笑。", "Ví dụ: Chương trình chỉ biết làm trò cười thì hiệu quả cũng không tốt lắm. / Anh ấy đặc biệt có tài pha trò.")]),
 ("恶作剧", "Trò đùa tinh quái", [
   ("故意与某人开玩笑，让其出洋相的行为。", "Hành vi cố ý đùa với ai đó để người ấy bị làm trò cười."),
   ("例如：我才知道这只是他的恶作剧。／这个恶作剧一点儿也不好玩儿。", "Ví dụ: Tôi mới biết đó chỉ là trò đùa tinh quái của anh ta. / Trò đùa ác ý này chẳng vui chút nào.")]),
 ("《憨豆先生》", "《Mr. Bean》", [("Mr. Bean 英国喜剧。", "Mr. Bean, hài kịch Anh.")]),
 ("泰迪熊", "Gấu bông Teddy (teddy bear)", []),
 ("机舱", "Khoang máy bay", [("飞机内留给乘客坐和装货物的地方。", "Phần bên trong máy bay dành cho hành khách ngồi và chở hàng hóa.")]),
 ("古稀", "Tuổi xưa nay hiếm (70 tuổi)", [
   ("指人七十岁。", "Chỉ người bảy mươi tuổi."),
   ("例如：年过古稀／古稀之年。", "Ví dụ: tuổi quá thất thập / năm thất thập cổ lai hy.")]),
 ("感", "Cảm (hậu tố chỉ cảm giác)", [
   ("意思是感觉、感想、情感，经常与别的词构成名词。", "Nghĩa là cảm giác, cảm tưởng, tình cảm; thường kết hợp với từ khác tạo thành danh từ."),
   ("例如：好感、美感、幽默感、参与感、方向感。", "Ví dụ: thiện cảm, cảm giác thẩm mỹ, óc hài hước, cảm giác tham gia, cảm giác phương hướng.")]),
 ("捉弄", "Trêu chọc, trêu ghẹo", [
   ("动词，跟人开玩笑，使人为难。", "Động từ, đùa với người khác khiến họ lúng túng, khó xử."),
   ("例如：捉弄小孩儿／别捉弄人。", "Ví dụ: trêu chọc trẻ con / đừng trêu người ta.")]),
]
L4_QS = {  # số câu hỏi → (hán, việt, đáp án hán|None, đáp án việt|None)
 3: ("请学学老奶奶睡着的样子。", "Hãy bắt chước dáng bà cụ ngủ.", None, None),
 6: ("请学学老爷爷取出老花镜以后的几个动作。", "Hãy bắt chước vài động tác của ông cụ sau khi lấy kính lão ra.",
     "站到老奶奶前面，仔细打量她几秒钟；一边四处张望，一边装作若无其事地把老花镜戴到老伴儿头上。（据课文归纳）",
     "Đứng trước mặt bà cụ, ngắm bà vài giây; vừa nhìn quanh vừa làm bộ như không có chuyện gì, đeo kính lão lên đầu bà. (tóm lược theo bài khóa)"),
 7: ("“此时”是什么时候？", "“此时” (lúc này) là lúc nào?",
     "老爷爷把老花镜戴到老奶奶头上的时候。（据课文归纳）",
     "Lúc ông cụ đeo kính lão lên đầu bà cụ. (tóm lược theo bài khóa)"),
}
L4_SI = ("天色发白了，人们<b>纷纷</b>举起相机，<b>迫切</b>地等待日出。可是，很久都不见太阳出来，这时，大家才<b>意识</b>到，怕是阴天，太阳不出来了。也罢，那就看云海吧，也别有一番风趣呢。",
         "Trời hửng sáng, mọi người lũ lượt giơ máy ảnh lên, sốt ruột chờ mặt trời mọc. Nhưng rất lâu vẫn không thấy mặt trời ló ra; lúc này mọi người mới nhận ra rằng có lẽ trời âm u, mặt trời sẽ không mọc. Thôi vậy, thế thì ngắm biển mây cũng được, cũng có một nét thú vị riêng.")

# (số, tiêu đề hán, dạng việt, trang, mục: [(hán, việt)], kiểu)
L4_EX = [
 ("五", "用指定词语或格式完成对话", "V. Dùng từ ngữ hoặc cấu trúc được chỉ định để hoàn thành hội thoại", "P63", [
   ("A：明天的乒乓球比赛，你有没有信心？\nB：当然有，<I/>。[（就／全）看A的（了／吧）]",
    "A: Trận bóng bàn ngày mai, bạn có tự tin không? B: Đương nhiên có, ＿＿＿＿. [(就/全)看A的(了/吧): tất cả trông vào A đấy]"),
   ("A：<I/>，您还没认出我是谁？（打量）\nB：你是李华吧？变化挺大的，有点儿不敢认了！",
    "A: ＿＿＿＿, bác vẫn chưa nhận ra tôi là ai sao? (打量: nhìn kỹ từ trên xuống) B: Cậu là Lý Hoa nhỉ? Thay đổi khá nhiều, tôi suýt không dám nhận!"),
   ("A：我暗示他注意发言的时间，不知道他明白了没有。\nB：我觉得<I/>，他一直看手表。（意识）",
    "A: Tôi ám chỉ anh ấy chú ý thời gian phát biểu, không biết anh ấy đã hiểu chưa. B: Tôi thấy ＿＿＿＿, anh ấy cứ nhìn đồng hồ mãi. (意识: nhận ra)"),
   ("A：听你同学说，你最近特别忙，就别陪我了。\nB：咱们好久不见，<I/>。（再……也……）",
    "A: Nghe bạn học của bạn nói dạo này bạn rất bận, đừng đi cùng tôi nữa. B: Lâu lắm rồi chúng ta mới gặp nhau, ＿＿＿＿. (再……也……: dù… đến mấy cũng…)"),
   ("A：你看你，一遍一遍地打电话，我不是说了吗，一有消息就告诉你。\nB：我这不是<I/>。（迫切）",
    "A: Nhìn bạn kìa, gọi điện hết lần này đến lần khác, tôi chẳng nói rồi sao, có tin là báo ngay cho bạn. B: Tôi đây chẳng phải là ＿＿＿＿ sao. (迫切: sốt ruột, cấp thiết)"),
   ("A：你们昨天玩儿得怎么样？\nB：<I/>（本以为……，没想到……）",
    "A: Hôm qua các bạn chơi thế nào? B: ＿＿＿＿ (本以为……，没想到……: vốn tưởng…, không ngờ…)"),
   ("A：你站在<I/>？（张望）\nB：等出租车呢，我都站这儿半个小时了，一辆空车也没有。",
    "A: Bạn đứng ở ＿＿＿＿ à? (张望: ngóng nhìn) B: Đang đợi taxi, tôi đứng ở đây nửa tiếng rồi mà không có chiếc xe trống nào.")]),
 ("六", "用指定词语或格式改写句子", "VI. Dùng từ ngữ hoặc cấu trúc được chỉ định để viết lại câu", "P63–P64", [
   ("这个地方真美，不来不知道，来了真觉得没白来。<I/>（不V……，一V……）",
    "Nơi này đẹp thật, không đến thì không biết, đến rồi mới thấy thật không uổng công. ＿＿＿＿ (不V……，一V……)"),
   ("秋风阵阵，树叶不断飘落下来。<I/>（纷纷）", "Gió thu từng đợt, lá cây không ngừng rơi xuống. ＿＿＿＿ (纷纷: lũ lượt)"),
   ("刚被批评了一顿，他却像什么事也没有发生一样，好像挨批评的不是他。<I/>（若无其事）",
    "Vừa bị phê bình một trận, anh ấy lại như chẳng có chuyện gì xảy ra, cứ như người bị phê bình không phải là anh. ＿＿＿＿ (若无其事: như không có chuyện gì)"),
   ("出版社的这些介绍历史文化知识的书很受欢迎。<I/>（系列）",
    "Những cuốn sách giới thiệu kiến thức lịch sử văn hóa này của nhà xuất bản rất được hoan nghênh. ＿＿＿＿ (系列: loạt, chuỗi)"),
   ("这只小猫闲不住，一会儿蹲在那儿想抓小鸟，一会儿玩自己的尾巴。<I/>（顽皮）",
    "Chú mèo con này không chịu ngồi yên, lúc thì ngồi xổm ở đó định vồ chim nhỏ, lúc thì nghịch đuôi của mình. ＿＿＿＿ (顽皮: nghịch ngợm)"),
   ("电影散场了，大家一个一个按顺序走出电影院，还在议论着电影中的情节。<I/>（依次）",
    "Phim tan, mọi người lần lượt theo thứ tự đi ra khỏi rạp, vẫn còn bàn tán về tình tiết trong phim. ＿＿＿＿ (依次: lần lượt)"),
   ("这位建筑大师设计的作品与众不同，所以多次获奖。<I/>（别出心裁）",
    "Tác phẩm do vị kiến trúc sư bậc thầy này thiết kế khác biệt với mọi người, nên đã nhiều lần đoạt giải. ＿＿＿＿ (别出心裁: độc đáo, sáng tạo)")]),
 ("七", "在理解课文的基础上，完成下面的练习", "VII. Dựa trên việc hiểu bài đọc, hoàn thành các bài tập sau", "P64", [
   ("分组表演：根据课文内容表演“她睡着了，我干点儿什么呢”。", "Diễn theo nhóm: dựa vào nội dung bài khóa, diễn lại tình huống “Bà ấy ngủ rồi, tôi làm gì đây nhỉ”."),
   ("你喜欢课文中的这位老先生吗？为什么？", "Bạn có thích vị cụ ông trong bài khóa không? Vì sao?"),
   ("即时短剧表演。要求与规则：\n（1）学生从教室里随意选取5样东西作为道具。\n（2）学生分小组讨论剧情（10分钟），并分配好角色，每个人都必须参加表演，5样道具都必须在剧情里发挥作用。\n（3）给自己小组的短剧起好名字。\n（4）每个小组按讨论好的剧情进行表演。\n（5）集体评奖，评选剧情奖、表演奖、最佳台词奖。",
    "Diễn kịch ngắn ngay tại chỗ. Yêu cầu và quy tắc: (1) Học sinh tùy ý chọn 5 món đồ trong lớp làm đạo cụ. (2) Học sinh chia nhóm thảo luận cốt truyện (10 phút) và phân vai, mỗi người đều phải tham gia diễn, cả 5 món đạo cụ đều phải phát huy tác dụng trong cốt truyện. (3) Đặt tên cho vở kịch ngắn của nhóm mình. (4) Mỗi nhóm diễn theo cốt truyện đã thảo luận. (5) Cả lớp cùng bình chọn giải: giải cốt truyện, giải diễn xuất, giải lời thoại hay nhất.")]),
]
L4_EX8 = ("八", "参考提示词语、格式和对话中的特殊要求，完成对话", "VIII. Dựa vào từ ngữ, cấu trúc gợi ý và yêu cầu đặc biệt trong hội thoại, hoàn thành hội thoại", "P64–P65",
  [("表示比较", "Biểu thị so sánh", "跟……不一样／不同", "so với… không giống / khác"),
   ("表示顿悟", "Biểu thị chợt hiểu ra", "明白了　懂了　怪不得　原来……", "hiểu rồi · biết rồi · thảo nào · thì ra…"),
   ("表示希望", "Biểu thị hy vọng", "（人＋）希望……　（人＋）期待……　……那样……　能……就好（了）　（就／全）看A的（了／吧）", "hy vọng… · mong chờ… · như thế… · có thể… thì tốt (rồi) · (就/全)看A的")],
  [("A：你喜欢这个爱恶搞的“老顽童”吗？\nB：<I/>。（表示喜欢，并说明喜欢的原因）",
    "A: Bạn có thích “ông lão ngoan đồng” hay chọc phá này không? B: ＿＿＿＿. (biểu thị thích và nói lý do thích)"),
   ("A：你身边有老顽童这样的人吗？\nB：<I/>。（表示肯定，并举例说明）",
    "A: Quanh bạn có người như ông lão ngoan đồng này không? B: ＿＿＿＿. (biểu thị khẳng định và nêu ví dụ)"),
   ("A：你希望自己幽默、对生活永远充满热情吗？\nB：当然希望了，<I/>，因为我爱我的家人。（表示希望，像老爷爷那样）",
    "A: Bạn có mong mình hài hước, mãi mãi tràn đầy nhiệt huyết với cuộc sống không? B: Đương nhiên mong rồi, ＿＿＿＿, vì tôi yêu gia đình mình. (biểu thị hy vọng, như ông cụ kia)"),
   ("A：<I/>，我还以为是人的性格决定的呢。（表示顿悟）\nB：在我看来，没有爱，就不会幽默，也不想幽默，没有动力呀！",
    "A: ＿＿＿＿, tôi còn tưởng là do tính cách con người quyết định cơ. (biểu thị chợt hiểu ra) B: Theo tôi, không có tình yêu thì sẽ không hài hước, cũng chẳng muốn hài hước, không có động lực mà!"),
   ("A：周有光先生也很幽默。<I/>。（表示比较，周先生的幽默和“老顽童”的幽默有区别）\nB：不管什么样的幽默，<I/>。（表示希望）",
    "A: Ông Chu Hữu Quang cũng rất hài hước. ＿＿＿＿. (biểu thị so sánh: sự hài hước của ông Chu khác với “ngoan đồng”) B: Bất kể là kiểu hài hước nào, ＿＿＿＿. (biểu thị hy vọng)"),
   ("A：幽默也是天生的吧，幽默能培养吗？有学习幽默的书吗？给我介绍一本。\nB：我不给你介绍书，等我练好了，教教你，<I/>。（表示希望，在自己身上）",
    "A: Hài hước cũng là bẩm sinh nhỉ, có thể rèn luyện được không? Có sách học hài hước không? Giới thiệu cho tôi một cuốn. B: Tôi không giới thiệu sách đâu, đợi tôi luyện giỏi rồi sẽ dạy bạn, ＿＿＿＿. (biểu thị hy vọng, nơi chính mình)")])
L4_EX9 = ("九", "写一写", "IX. Tập viết", "P65–P66",
  [("以“老顽童”为题，写一篇短文。", "Lấy “ông lão ngoan đồng” làm đề, viết một bài văn ngắn."),
   ("要求：（1）尽量使用以下词语或格式；（2）短文不少于280字。", "Yêu cầu: (1) cố gắng dùng các từ ngữ hoặc cấu trúc dưới đây; (2) bài văn không ít hơn 280 chữ."),
   ("如果有更好的内容，鼓励自选。", "Nếu có nội dung hay hơn, khuyến khích tự chọn.")],
  ["登", "赶忙", "掏", "打量", "张望（东张西望）", "沉", "弄", "以", "不V……，一V……", "看A的"],
  "Đăng (lên) · vội vàng · móc · nhìn kỹ · ngóng nhìn (nhìn đông ngó tây) · sâu, say · làm · để (mục đích) · không V…, vừa V… · trông vào A")
L4_EX10 = ("十", "阅读短文，并按要求完成练习", "X. Đọc đoạn văn và hoàn thành bài tập theo yêu cầu", "P67–P68",
  ("钱锺书和杨绛的小故事", "Câu chuyện nhỏ về Tiền Chung Thư và Dương Giáng"),
  [("钱锺书（1910—1998）和杨绛（1911—2016）在清华大学一见钟情。第一次见面，钱锺书第一句话就是：“我没有订婚。”杨绛回答：“我也没有男朋友。”就这样，他们开始了恋爱。",
    "Tiền Chung Thư (1910–1998) và Dương Giáng (1911–2016) yêu nhau từ cái nhìn đầu tiên tại Đại học Thanh Hoa. Lần đầu gặp mặt, câu đầu tiên của Tiền Chung Thư là: “Tôi chưa đính hôn.” Dương Giáng đáp: “Tôi cũng chưa có bạn trai.” Cứ như vậy, họ bắt đầu yêu nhau."),
   ("可能有人会问，他们争吵过吗？他们结婚后，有过一次吵架。为了一个法文“bon”的读音，杨绛说钱锺书的发音带着家乡的口音，钱锺书不服，你一言我一语就吵起来了，结果是杨绛赢了。但不管赢的还是输的，都不开心。从此，他们决定以后对问题可以有不同意见，但不必非得争输赢，非得要说服对方。",
    "Có thể có người sẽ hỏi: họ đã từng cãi nhau chưa? Sau khi kết hôn, họ có một lần cãi nhau. Vì cách đọc một từ tiếng Pháp “bon”, Dương Giáng nói cách phát âm của Tiền Chung Thư mang giọng quê, Tiền Chung Thư không phục, anh một câu tôi một câu rồi cãi nhau, kết quả là Dương Giáng thắng. Nhưng dù là người thắng hay người thua đều không vui. Từ đó, họ quyết định sau này có thể có ý kiến khác nhau về vấn đề, nhưng không cần nhất thiết phải tranh hơn thua, nhất thiết phải thuyết phục đối phương."),
   ("一次，杨绛午睡，童心未泯的钱锺书想给她画个大花脸。毛笔刚落到脸上，就惊醒了杨绛。杨绛赶忙去洗脸，可不洗不知道，一洗才发现墨汁很难洗净，把脸皮洗到快要破了，才看不出墨痕。从此以后，钱锺书再也不搞恶作剧了，但他画了一幅杨绛的头像，上面画上眼镜和胡子，以过瘾。",
    "Có lần, Dương Giáng ngủ trưa, Tiền Chung Thư vẫn còn tâm hồn trẻ thơ muốn vẽ lên mặt bà một cái mặt hề. Bút lông vừa chạm xuống mặt, Dương Giáng đã giật mình tỉnh dậy. Bà vội đi rửa mặt, nhưng không rửa thì không biết, rửa mới thấy mực rất khó sạch, rửa đến suýt rách cả da mặt mới không còn thấy vết mực. Từ đó về sau, Tiền Chung Thư không bao giờ bày trò đùa ác nữa, nhưng ông vẽ một bức chân dung Dương Giáng, vẽ thêm kính và râu lên đó cho đã tay."),
   ("“没遇到你之前，我没想过结婚。遇见你，结婚这事，我没想过别人。”这是杨绛和钱锺书两人的心声。",
    "“Trước khi gặp em, anh chưa từng nghĩ đến chuyện kết hôn. Gặp em rồi, chuyện kết hôn, anh chưa từng nghĩ đến ai khác.” Đây là tiếng lòng của cả Dương Giáng lẫn Tiền Chung Thư.")],
  [("阅读中，请记下你不懂的字词，并用你自己的方式弄懂它们。", "Khi đọc, hãy ghi lại các chữ từ bạn chưa hiểu và tự tìm cách hiểu chúng."),
   ("如有不懂的句子请记下来，找时间向老师请教，或者和同学们讨论。", "Nếu có câu không hiểu, hãy ghi lại, tìm thời gian hỏi thầy cô hoặc thảo luận với các bạn."),
   ("上网查查钱锺书和杨绛，并把你查到的最有趣的部分和同学们分享。", "Lên mạng tìm hiểu về Tiền Chung Thư và Dương Giáng, rồi chia sẻ với các bạn phần thú vị nhất bạn tìm được.")])
L4_EX11 = ("十一", "拓展学习", "XI. Học tập mở rộng", "P68", [
   ("你身边有没有“老顽童”“小顽童”或者什么顽童，给大家讲讲他／她的故事。", "Quanh bạn có “ông lão ngoan đồng”, “cậu bé tinh nghịch” hay một người ngoan đồng nào không? Hãy kể cho mọi người nghe câu chuyện của người ấy."),
   ("“童心未泯”“一事未成”中都带“未”字，请你找出5个这样的成语并弄明白它们的意思，别忘了分享给大家！", "Trong “童心未泯” và “一事未成” đều có chữ “未”. Hãy tìm 5 thành ngữ như vậy và hiểu nghĩa của chúng, đừng quên chia sẻ với mọi người!")])

# ───────────────────────── BÀI 8 ─────────────────────────
L8_TIJIE = ("20世纪80年代，中国实行对内改革、对外开放的政策，全国上下一心，人人充满干劲，中国发生了前所未有的变化，人们的生活水平不断提高。80年代成为许多中国人最难忘的年代。你想了解一下那时的中国吗？那就看看这篇课文吧。",
            "Trong thập niên 80 của thế kỷ 20, Trung Quốc thực hiện chính sách cải cách đối nội, mở cửa đối ngoại; cả nước trên dưới một lòng, ai nấy tràn đầy khí thế, Trung Quốc xảy ra những thay đổi chưa từng có, mức sống của người dân không ngừng được nâng cao. Thập niên 80 trở thành thời kỳ khó quên nhất đối với nhiều người Trung Quốc. Bạn có muốn tìm hiểu về Trung Quốc thời ấy không? Vậy hãy đọc bài khóa này nhé.")
L8_TEXT = [  # tr.125–127
 ("20世纪80年代，中国实行对内改革、对外开放¹的政策，鼓励搞活经济、发展经济，提高人们的生活水平。“改革”和“创新”成了那个年代人们谈论最多的话题，也因为改革和创新，人们的观念和各行各业都发生了巨大的变化。",
  "Trong thập niên 80 của thế kỷ 20, Trung Quốc thực hiện chính sách cải cách đối nội, mở cửa đối ngoại¹, khuyến khích làm sống động nền kinh tế, phát triển kinh tế, nâng cao mức sống của người dân. “Cải cách” và “đổi mới” trở thành chủ đề được bàn luận nhiều nhất thời ấy, và cũng nhờ cải cách, đổi mới mà quan niệm của con người cùng mọi ngành nghề đều có những thay đổi to lớn."),
 ("80年代之前，中国农村基本上是典型的“大锅饭²”，一个生产队少则³几十人，多则上百人、几百人，集体劳动，集体分配，干多干少一个样，干好干坏一个样，不能调动人们的劳动积极性。",
  "Trước thập niên 80, nông thôn Trung Quốc về cơ bản là kiểu “ăn chung nồi cơm lớn²” điển hình: một đội sản xuất ít thì³ vài chục người, nhiều thì hàng trăm, vài trăm người, lao động tập thể, phân phối tập thể, làm nhiều làm ít như nhau, làm tốt làm xấu như nhau, không thể khơi dậy tính tích cực lao động của mọi người."),
 ("80年代，农村实行家庭联产承包责任制⁴。种的粮食，除了交给国家的，剩下都是自己的。农民有了积极性，起早贪黑地用心种植管理，粮食产量大增，不但够吃了，而且有了剩余。于是，农民开始种棉花⁵、种蔬菜、种果树、养猪、养鸡、养鸭，开工厂、办企业……几年下来，村里出现了一排排宽敞明亮的新房子。手里有钱了，把大家高兴得无法形容。那也是父母们一生最值得怀念的日子。",
  "Thập niên 80, nông thôn thực hiện chế độ khoán hộ gia đình⁴. Lương thực trồng ra, trừ phần nộp cho nhà nước, phần còn lại đều là của mình. Nông dân có tính tích cực, dậy sớm thức khuya chăm chút trồng trọt, quản lý, sản lượng lương thực tăng mạnh, không những đủ ăn mà còn dư dả. Thế là nông dân bắt đầu trồng bông⁵, trồng rau, trồng cây ăn quả, nuôi lợn, nuôi gà, nuôi vịt, mở xưởng, lập doanh nghiệp…… Vài năm sau, trong làng xuất hiện từng dãy nhà mới rộng rãi, sáng sủa. Có tiền trong tay, mọi người vui mừng không sao tả xiết. Đó cũng là những ngày tháng đáng nhớ nhất trong cuộc đời của các bậc cha mẹ."),
 ("80年代是全民读书学习的年代。那时，读书是一种潮流，大大小小的图书馆里总是坐满了人，公园里、公交车上，随处可见捧着书本的人。学生的目标是考上大学，上班族的首选是夜大、函授⁶大学和自学考试。当时，广播英语是最大的课堂，一天播放好多遍，学生数以万计、百万计。人们之所以如饥似渴地学习，就是因为他们要把耽误的时间抢回来，要睁开眼睛看世界。",
  "Thập niên 80 là thời đại toàn dân đọc sách, học tập. Khi ấy, đọc sách là một trào lưu: các thư viện lớn nhỏ lúc nào cũng kín người, trong công viên, trên xe buýt, đâu đâu cũng thấy người cầm sách. Mục tiêu của học sinh là thi đỗ đại học; lựa chọn hàng đầu của người đi làm là đại học buổi tối, đại học hàm thụ⁶ và thi tự học. Lúc bấy giờ, tiếng Anh qua đài phát thanh là lớp học lớn nhất, một ngày phát đi phát lại nhiều lượt, số học viên lên đến hàng chục nghìn, hàng triệu. Sở dĩ mọi người học khao khát như đói như khát, chính là vì họ muốn giành lại khoảng thời gian đã bị lỡ, muốn mở to mắt nhìn ra thế giới."),
 ("提起80年代，必然要说中国女排，女排分别在世界杯、世锦赛和奥运会上夺得冠军！女排和中国一起腾飞！那时候，只要有女排的比赛，不管老幼，都会早早地坐在电视机前或围在收音机旁，聚精会神地观看或收听比赛实况。女排姑娘们代表着积极努力、顽强拼搏的时代精神，她们是全国人民心中的英雄！",
  "Nhắc đến thập niên 80, nhất định phải nói đến đội bóng chuyền nữ Trung Quốc: đội nữ lần lượt giành chức vô địch ở World Cup, Giải vô địch thế giới và Thế vận hội! Bóng chuyền nữ cùng Trung Quốc cất cánh! Thời ấy, chỉ cần có trận đấu của đội nữ, bất kể già trẻ, mọi người đều ngồi trước tivi hoặc quây quanh chiếc radio từ rất sớm, chăm chú xem hoặc nghe tường thuật trực tiếp trận đấu. Các cô gái bóng chuyền đại diện cho tinh thần thời đại là nỗ lực tích cực, kiên cường quyết chiến, họ là những người hùng trong lòng cả nước!"),
 ("80年代还是流行音乐的时代。港台歌曲开始在内地（大陆）流行，《我的中国心》《冬天里的一把火》及台湾校园歌曲很快就红⁷遍了全国。与此同时，歌坛刮来了“西北风”。“我家住在黄土高坡，大风从坡上刮过，不管是西北风还是东南风，都是我的歌，我的歌。”既有传统西北民歌特点，又有西方现代摇滚⁸和流行音乐特点的“西北风”，很快就受到男女老少的喜爱。",
  "Thập niên 80 còn là thời đại của nhạc đại chúng. Ca khúc Hồng Kông, Đài Loan bắt đầu thịnh hành ở nội địa (đại lục): 《Trái tim Trung Hoa của tôi》, 《Ngọn lửa giữa mùa đông》 cùng các bài hát học đường Đài Loan nhanh chóng nổi⁷ khắp cả nước. Cùng lúc đó, làng ca nhạc nổi lên “gió Tây Bắc”. “Nhà tôi ở cao nguyên hoàng thổ, gió lớn thổi qua sườn dốc, dù là gió Tây Bắc hay gió Đông Nam, đều là bài ca của tôi, bài ca của tôi.” “Gió Tây Bắc” vừa mang đặc điểm dân ca Tây Bắc truyền thống, vừa mang đặc điểm nhạc rock⁸ hiện đại phương Tây và nhạc đại chúng, nhanh chóng được nam nữ già trẻ yêu thích."),
 ("80年代最重要的要数观念上的变化，“发展才是硬道理⁹”“科学技术是第一生产力¹⁰”等观念深入人心，各行各业争先恐后求发展，整个中国发生着日新月异的变化。在“时间就是金钱，效率就是生命”的口号下，出现了三天一层楼的“深圳¹¹速度”。中国，带着希望，飞速发展！",
  "Điều quan trọng nhất của thập niên 80 phải kể đến là sự thay đổi trong quan niệm: những quan niệm như “phát triển mới là chân lý cứng⁹”, “khoa học kỹ thuật là lực lượng sản xuất hàng đầu¹⁰” thấm sâu vào lòng người, mọi ngành nghề đua nhau tìm cách phát triển, cả Trung Quốc thay đổi từng ngày từng tháng. Dưới khẩu hiệu “thời gian là tiền bạc, hiệu suất là sinh mệnh”, đã xuất hiện “tốc độ Thâm Quyến¹¹” xây một tầng lầu trong ba ngày. Trung Quốc, mang theo hy vọng, phát triển như bay!"),
 ("这就是80年代，一个普通又不普通的年代，那时虽然还很贫穷，但人人都积极努力，不计较得失，对美好生活充满希望，正如歌中唱的“再过二十年我们重相会，伟大的祖国该有多么美，天也新，地也新，春光更明媚，城市乡村处处增光辉”。",
  "Đó chính là thập niên 80, một thời đại bình thường mà lại không bình thường; khi ấy tuy còn rất nghèo, nhưng ai cũng tích cực nỗ lực, không so đo được mất, tràn đầy hy vọng vào cuộc sống tốt đẹp, đúng như lời bài hát: “Hai mươi năm nữa chúng ta sẽ gặp lại, Tổ quốc vĩ đại sẽ đẹp biết bao, trời cũng mới, đất cũng mới, ánh xuân càng tươi sáng, thành thị nông thôn nơi nơi thêm rạng rỡ”."),
]
L8_AUTHOR = ("（作者：阮畅）", "(Tác giả: Nguyễn Sướng)")
L8_NOTES = [
 ("对内改革、对外开放", "Cải cách đối nội, mở cửa đối ngoại", [
   ("1978年12月中国提出的政策，“对内改革”指在中国内部进行政治、经济、教育、科技等方面的改革；“对外开放”指中国积极主动地扩大对外经济交往，包括引进外资、引进先进的技术设备、设立经济特区、开放沿海城市等。",
    "Chính sách Trung Quốc đề ra vào tháng 12 năm 1978. “Cải cách đối nội” là cải cách trong nội bộ Trung Quốc về chính trị, kinh tế, giáo dục, khoa học kỹ thuật…; “mở cửa đối ngoại” là Trung Quốc chủ động mở rộng giao lưu kinh tế với bên ngoài, gồm thu hút vốn nước ngoài, nhập thiết bị kỹ thuật tiên tiến, lập đặc khu kinh tế, mở cửa các thành phố ven biển, v.v.")]),
 ("大锅饭", "Ăn chung nồi cơm lớn (indiscriminate egalitarianism)", [
   ("比喻平均主义的分配现象。“大锅饭”包括两个方面：一是企业不管经营好坏、盈利还是亏损，工资照发；二是在企业内部或农村，干多干少、干好干坏，都不会影响个人分配，存在严重的平均主义。",
    "Ví von hiện tượng phân phối theo chủ nghĩa bình quân. “Nồi cơm lớn” gồm hai mặt: một là doanh nghiệp dù kinh doanh tốt hay xấu, lãi hay lỗ, lương vẫn trả như cũ; hai là trong nội bộ doanh nghiệp hoặc ở nông thôn, làm nhiều hay ít, làm tốt hay xấu đều không ảnh hưởng đến phần phân phối của cá nhân, tồn tại chủ nghĩa bình quân nghiêm trọng.")]),
 ("则", "则 (liên từ, văn viết)", [
   ("连词，书面语。本课用于小句内部，表示假设关系，相当于“一个生产队，（人）少的话，是几十人，多的话，是上百人、几百人”。例如：别人提意见是好事，有则改之，无则加勉。",
    "Liên từ, văn viết. Trong bài này dùng bên trong tiểu cú, biểu thị quan hệ giả thiết, tương đương “một đội sản xuất, (người) ít thì là vài chục người, nhiều thì là hàng trăm, vài trăm người”. Ví dụ: Người khác góp ý là việc tốt, có thì sửa, không có thì càng cố gắng.")]),
 ("家庭联产承包责任制", "Chế độ khoán trách nhiệm theo hộ gia đình (household contract responsibility system)", [
   ("农民以家庭为单位向集体经济组织承包土地等生产资料和生产任务的农业生产责任制形式。农民可按照合同规定自主地进行生产和经营，经营收入部分上缴，其余归农户。",
    "Hình thức chế độ trách nhiệm sản xuất nông nghiệp, trong đó nông dân lấy hộ gia đình làm đơn vị nhận khoán đất đai và các tư liệu sản xuất khác cùng nhiệm vụ sản xuất từ tổ chức kinh tế tập thể. Nông dân có thể tự chủ sản xuất, kinh doanh theo hợp đồng, một phần thu nhập nộp lên, phần còn lại thuộc về hộ nông dân.")]),
 ("棉花", "Bông (cotton)", [("农作物，果实是重要的纺织原料。", "Cây nông nghiệp, quả của nó là nguyên liệu dệt quan trọng.")]),
 ("函授", "Đào tạo từ xa, hàm thụ", [
   ("运用通信方式进行远距离教育。20世纪80年代中国的函授教育主要是听广播和函授相结合。",
    "Dùng phương thức thông tin liên lạc để giáo dục từ xa. Giáo dục hàm thụ ở Trung Quốc thập niên 80 chủ yếu là kết hợp nghe đài phát thanh với học hàm thụ (qua tài liệu gửi).")]),
 ("红", "Nổi tiếng, được ưa chuộng", [
   ("指受人重视或欢迎。例如：她可是学校的大红人。／这位歌手现在很红。／这部电影红了好几个演员。",
    "Chỉ việc được người ta coi trọng hoặc yêu thích. Ví dụ: Cô ấy là người nổi tiếng của trường. / Ca sĩ này bây giờ rất nổi. / Bộ phim này làm nổi mấy diễn viên.")]),
 ("摇滚", "Nhạc rock (rock and roll)", [("一种流行音乐。", "Một thể loại nhạc đại chúng.")]),
 ("发展才是硬道理", "Phát triển mới là chân lý cứng (Development is the absolute principle)", [
   ("“发展”的观念，早在20世纪80年代就已经形成，1992年邓小平将其归纳为“发展才是硬道理”，意思是发展是解决一切问题的关键。",
    "Quan niệm “phát triển” đã hình thành từ thập niên 80 của thế kỷ 20; năm 1992 Đặng Tiểu Bình đúc kết thành “phát triển mới là chân lý cứng”, nghĩa là phát triển là chìa khóa giải quyết mọi vấn đề.")]),
 ("科学技术是第一生产力", "Khoa học kỹ thuật là lực lượng sản xuất hàng đầu (Science and technology constitute a primary productive force)", [
   ("由邓小平1988年提出，突出强调科学技术对社会发展的重要性。",
    "Do Đặng Tiểu Bình nêu ra năm 1988, nhấn mạnh tầm quan trọng của khoa học kỹ thuật đối với sự phát triển xã hội.")]),
 ("深圳", "Thâm Quyến", [("城市名，在中国南部，是中国改革开放后建立的第一个经济特区。", "Tên một thành phố ở miền Nam Trung Quốc, là đặc khu kinh tế đầu tiên được thành lập sau cải cách mở cửa.")]),
]
L8_QS = [
 ("熟读第一段，最好背诵下来。", "Đọc thuộc đoạn đầu, tốt nhất là học thuộc lòng."),
 ("“大锅饭”是怎么回事？", "“Ăn chung nồi cơm lớn” là chuyện gì?"),
 ("注意“A则……，B则……”的用法。", "Chú ý cách dùng “A则……，B则……”."),
 ("实行“家庭联产承包责任制”后，农民有什么变化？农民的生活有什么变化？", "Sau khi thực hiện “chế độ khoán hộ gia đình”, nông dân có thay đổi gì? Đời sống của nông dân có thay đổi gì?"),
 ("说说“80年代全民读书”的景象。", "Hãy nói về cảnh “toàn dân đọc sách” thập niên 80."),
 ("说说广播英语的教学情况。", "Hãy nói về tình hình dạy tiếng Anh qua đài phát thanh."),
 ("“如饥似渴”是什么意思？", "“如饥似渴” có nghĩa là gì?"),
 ("人们是怎样关注女排比赛的？", "Mọi người theo dõi các trận đấu của đội bóng chuyền nữ như thế nào?"),
 ("中国女排代表的时代精神是什么？", "Tinh thần thời đại mà đội bóng chuyền nữ Trung Quốc đại diện là gì?"),
 ("为什么说“80年代是流行音乐的时代”？", "Vì sao nói “thập niên 80 là thời đại của nhạc đại chúng”?"),
 ("歌坛上的“西北风”是什么意思？", "“Gió Tây Bắc” trong làng ca nhạc có nghĩa là gì?"),
 ("用自己的话介绍一下80年代中国最重要的变化。", "Hãy dùng lời của mình giới thiệu thay đổi quan trọng nhất của Trung Quốc thập niên 80."),
 ("熟读最后一段。要不，干脆背诵下来？", "Đọc thuộc đoạn cuối. Hay là học thuộc luôn nhé?"),
]
L8_FIX = {  # câu 八 bị mờ ở bản cũ → khôi phục từ tr.138
 "old_zh": "姐姐因为家里旁边说[…]了学习,她一边工作,一边上夜校,完成了大专学业。",
 "new_zh": "姐姐因为家里穷耽误了学习，她一边工作，一边上夜校，完成了大专学业。",
 "new_vi": "Chị gái vì nhà nghèo mà lỡ dở việc học, vừa làm việc vừa học trường buổi tối, hoàn thành chương trình cao đẳng.",
}

# ───────────────────────── BÀI 2 (题解, ảnh không có số trang) ─────────────────────────
L2_TIJIE = ("周有光先生是中国千千万万知识分子当中的一个，他既普通，也不普通。说他普通，是因为他和别人没什么区别；说他不普通，不仅因为他在经济学，特别是语言文字学和中外文化领域做出的学术贡献，也在于他跨世纪活了112岁。",
            "Ông Chu Hữu Quang là một trong hàng nghìn hàng vạn trí thức Trung Quốc, ông vừa bình thường, lại vừa không bình thường. Nói ông bình thường, là vì ông chẳng có gì khác người khác; nói ông không bình thường, không chỉ vì những đóng góp học thuật của ông trong kinh tế học, đặc biệt là ngôn ngữ văn tự học và lĩnh vực văn hóa Trung Quốc – nước ngoài, mà còn vì ông sống xuyên thế kỷ, thọ 112 tuổi.")
