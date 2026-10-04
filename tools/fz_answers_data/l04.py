# -*- coding: utf-8 -*-
ANS = {
 10: dict(guard='五、用指定词语或格式完成对话', show=[
   ("当然有，<b>就看我的了</b>。", "Đương nhiên có, cứ xem tôi đây."),
   ("<b>你上下打量了我半天</b>，您还没认出我是谁？", "Bác nhìn tôi từ trên xuống dưới mãi mà vẫn chưa nhận ra tôi là ai sao?"),
   ("我觉得<b>他已经意识到了</b>，他一直看手表。", "Tôi thấy anh ấy đã nhận ra rồi, anh ấy cứ nhìn đồng hồ mãi."),
   ("咱们好久不见，<b>你再忙也得陪我吃顿饭</b>。", "Lâu rồi chúng ta mới gặp, bạn bận đến mấy cũng phải ăn với tôi bữa cơm."),
   ("我这不是<b>迫切想知道结果吗</b>。", "Tôi đây chẳng phải là sốt ruột muốn biết kết quả sao."),
   ("<b>本以为会很无聊，没想到特别好玩儿</b>。", "Vốn tưởng sẽ rất chán, không ngờ rất vui."),
   ("你站在<b>路边张望什么</b>？", "Bạn đứng bên đường ngóng nhìn gì thế?")],
   note='Đây là đáp án gợi ý: câu hoàn thành hợp ngữ pháp và dùng đúng từ/cấu trúc yêu cầu; có thể có nhiều cách nói khác.'),
 11: dict(guard='六、用指定词语或格式改写句子', show=[
   ("不来不知道，一来才发现这个地方真美。", "Không đến không biết, đến rồi mới thấy nơi này thật đẹp."),
   ("秋风阵阵，树叶纷纷飘落下来。", "Gió thu từng đợt, lá cây lũ lượt rơi xuống."),
   ("刚被批评了一顿，他却若无其事，好像挨批评的不是他。", "Vừa bị phê bình một trận, anh ấy lại làm như không có chuyện gì, cứ như người bị phê bình không phải là anh."),
   ("出版社的这一系列介绍历史文化知识的书很受欢迎。", "Loạt sách giới thiệu kiến thức lịch sử văn hóa này của nhà xuất bản rất được hoan nghênh."),
   ("这只小猫很顽皮，闲不住，一会儿蹲在那儿想抓小鸟，一会儿玩自己的尾巴。", "Chú mèo con này rất nghịch, không chịu ngồi yên, lúc thì ngồi xổm định vồ chim, lúc thì nghịch đuôi mình."),
   ("电影散场了，大家依次走出电影院，还在议论着电影中的情节。", "Phim tan, mọi người lần lượt đi ra khỏi rạp, vẫn còn bàn tán về tình tiết trong phim."),
   ("这位建筑大师设计的作品别出心裁，所以多次获奖。", "Tác phẩm của vị kiến trúc sư bậc thầy này rất độc đáo, nên đã nhiều lần đoạt giải.")],
   note='Đáp án gợi ý; có thể viết lại theo cách khác miễn dùng đúng từ/cấu trúc đã chỉ định.'),
 12: dict(guard='七、在理解课文', show=[
   ("Diễn theo nhóm: một người đóng ông cụ, một người đóng bà cụ đang ngủ, người còn lại đóng người kể (“Bà ấy ngủ rồi, tôi làm gì đây nhỉ?”); dựng theo trình tự: chụp ảnh → đeo kính lão → đội mũ Giáng sinh → bà tỉnh → cả hàng khách cười.", ""),
   ("Gợi ý: 我喜欢这位老先生，因为他童心未泯、幽默，用开玩笑的方式表达对老伴儿的爱。", "Gợi ý: Tôi thích cụ ông, vì cụ còn giữ tâm hồn trẻ thơ, hài hước, dùng trò đùa để thể hiện tình yêu với bạn đời."),
   ("Bài thực hành, không có đáp án cố định: cả lớp chọn 5 đạo cụ, thảo luận 10 phút, đặt tên vở kịch, diễn và bình chọn giải.", "")],
   note='Bài hoạt động/ý kiến cá nhân — chỉ là gợi ý.'),
 13: dict(guard='八、参考提示词语', show=[
   ("喜欢！他很幽默，总能把大家逗乐，跟他在一起很开心。", "Thích! Ông ấy rất hài hước, luôn làm mọi người bật cười, ở bên ông ấy rất vui."),
   ("有，我爷爷就是这样的人，他七十多岁了，还爱跟孙子一起玩游戏。", "Có, ông nội tôi là người như vậy, ông hơn bảy mươi tuổi mà vẫn thích chơi game cùng cháu."),
   ("<b>我希望能像他那样</b>，因为我爱我的家人。", "Tôi mong có thể như ông ấy, vì tôi yêu gia đình mình."),
   ("<b>原来是这样啊</b>，我还以为是人的性格决定的呢。", "Thì ra là vậy, tôi còn tưởng là do tính cách con người quyết định cơ."),
   ("周先生的幽默<b>跟“老顽童”的不一样</b>，他的幽默更含蓄、更有智慧。", "Sự hài hước của ông Chu không giống “ngoan đồng”: hàm súc và thông tuệ hơn."),
   ("不管什么样的幽默，<b>我都希望它能让身边的人开心</b>。", "Bất kể kiểu hài hước nào, tôi đều mong nó làm người quanh mình vui."),
   ("等我练好了，教教你，<b>我希望能让你也变得幽默</b>。", "Đợi tôi luyện giỏi rồi sẽ dạy bạn, mong là bạn cũng sẽ trở nên hài hước.")],
   note='Đáp án gợi ý; mỗi chỗ cần đúng chức năng ghi trong ngoặc (thích, khẳng định, hy vọng, chợt hiểu, so sánh).'),
 14: dict(guard='九、写一写', show=[
   ("Dàn ý gợi ý (≥280 chữ): ① giới thiệu một “ông lão ngoan đồng” quanh bạn (登 / 赶忙 / 掏…) ② kể một chuyện cụ thể bằng cấu trúc 不V……，一V…… và 以 ③ nêu cảm nghĩ, dùng 看A的.", "")],
   note='Bài viết tự do — không có đáp án cố định.'),
 15: dict(guard='十、阅读短文', show=[
   ("Câu 1–2: bài tự học — ghi lại chữ/câu chưa hiểu (ví dụ 一见钟情, 订婚, 出洋相…), hỏi thầy hoặc thảo luận.", ""),
   ("Câu 3 (gợi ý): 钱锺书（1910—1998）、杨绛（1911—2016），著名作家、学者夫妇，代表作有《围城》《我们仨》等。", "Gợi ý: Tiền Chung Thư, Dương Giáng, cặp vợ chồng nhà văn, học giả nổi tiếng; tác phẩm tiêu biểu gồm 《Vi thành》, 《Chúng tôi ba người》…")],
   note='Bài đọc mở rộng/chia sẻ; thông tin câu 3 là gợi ý bổ sung, không phải đáp án của sách.'),
 16: dict(guard='十一、拓展学习', show=[
   ("Bài kể chuyện cá nhân — không có đáp án cố định.", ""),
   ("Gợi ý thành ngữ có chữ “未”: 童心未泯、一事未成、未雨绸缪、意犹未尽、方兴未艾、前所未有、始终未渝。", "Gợi ý: tâm hồn trẻ thơ chưa mất; chưa làm nên việc gì; lo xa phòng bị; ý còn chưa hết; đang lên chưa dừng; chưa từng có; trước sau không đổi.")],
   note='Gợi ý thành ngữ để bạn tra nghĩa và chia sẻ.'),
}
