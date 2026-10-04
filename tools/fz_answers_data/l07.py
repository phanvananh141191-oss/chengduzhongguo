# -*- coding: utf-8 -*-
SENT = [("B", "Các nhà thơ nước ta thích ví cầu vòm như cầu vồng."), ("E", "…hàng chục, hàng trăm, thậm chí hàng nghìn năm bắc hùng vĩ qua sông ngòi."), ("C", "Trong đó nổi tiếng nhất phải kể đến cầu Triệu Châu."), ("A", "Cây cầu cổ này lại khôi phục sức sống trẻ trung."), ("D", "Đủ thấy sự kiên cố của nó.")]
CHOICE = dict(show=[("(1) <b>B</b> 我国的诗人爱把拱桥比作虹。", "(1) B — Các nhà thơ nước ta thích ví cầu vòm như cầu vồng."),
                    ("(2) <b>E</b> 能几十年几百年甚至上千年雄跨在江河之上。", "(2) E — …có thể hùng vĩ bắc qua sông ngòi hàng chục, hàng trăm, thậm chí hàng nghìn năm."),
                    ("(3) <b>C</b> 其中最著名的当数赵州桥。", "(3) C — Trong đó nổi tiếng nhất phải kể đến cầu Triệu Châu."),
                    ("(4) <b>A</b> 这座古桥又恢复了青春。", "(4) A — Cây cầu cổ này lại khôi phục sức sống trẻ trung."),
                    ("(5) <b>D</b> 足见它的坚固。", "(5) D — Đủ thấy sự kiên cố của nó.")], note='Đáp án suy ra từ ngữ cảnh đoạn văn.')
ANS = {
 0: dict(guard='中国值得介绍的桥', show=[
   ("他们俩关系特别好，好得没有秘密。", "Hai người họ quan hệ đặc biệt tốt, tốt đến mức không có bí mật."),
   ("我的房间特别小，小得只能放下一张床。", "Phòng tôi rất nhỏ, nhỏ đến mức chỉ đặt vừa một chiếc giường."),
   ("我特别恨他，恨得一辈子都不想看到他。", "Tôi hận anh ta vô cùng, hận đến mức cả đời không muốn nhìn thấy."),
   ("我特别爱读这本书，爱得吃饭也放不下。", "Tôi đặc biệt thích đọc cuốn sách này, thích đến mức ăn cơm cũng không rời tay."),
   ("上下班时间交通特别堵，堵得十几分钟一动不动。", "Giờ đi làm giao thông đặc biệt tắc, tắc đến mức hơn mười phút không nhúc nhích."),
   ("最近我特别忙，忙得没时间吃饭。", "Dạo này tôi đặc biệt bận, bận đến mức không có thời gian ăn cơm."),
   ("我特别想家，想得做梦都回到了家里。", "Tôi đặc biệt nhớ nhà, nhớ đến mức nằm mơ cũng về nhà.")], note='Đáp án gợi ý (X特别A，A得C).'),
 1: dict(guard='要不这样,我带你', show=[
   ("他好久没见的一个好朋友来了，<b>昨晚聊到很晚，他实在太困了</b>。", "Một người bạn tốt lâu ngày không gặp đến, tối qua họ chuyện trò đến khuya, anh ấy thật sự quá buồn ngủ."),
   ("对不起，<b>我明天晚上实在没有时间</b>。", "Xin lỗi, tối mai tôi thật sự không có thời gian."),
   ("<b>这本书实在太难读了</b>，我好不容易看了一页，就放那儿了。", "Cuốn sách này thật sự quá khó đọc, tôi vất vả lắm mới đọc được một trang rồi để đó."),
   ("嗯，这个电影<b>实在太感人了</b>。", "Ừ, bộ phim này thật sự quá cảm động.")], note='Đáp án gợi ý (实在 + tính từ/động từ biểu thị mức độ).'),
 2: dict(guard='赵州桥成为文物', show=[
   ("A：她哭半天了，我劝也不管用。 B：<b>要不这样，我去劝劝她吧</b>。", "Cô ấy khóc nửa ngày, tôi khuyên cũng không được. — Hay là thế này, để tôi đi khuyên."),
   ("A：书找不到了，作业还没做呢！ B：<b>要不这样，咱俩一起用我的书吧</b>。", "Không tìm thấy sách, bài tập còn chưa làm! — Hay là thế này, hai đứa mình dùng chung sách của tôi."),
   ("A：请问去故宫怎么走？我第一次来中国。 B：<b>要不这样，我正好也要去，顺路带着你吧</b>。", "Xin hỏi đi Cố Cung thế nào? Tôi lần đầu đến Trung Quốc. — Hay là thế này, tôi cũng đang đi, tiện đường dẫn bạn đi."),
   ("A：我想去南京旅游，可是买不到飞机票。 B：<b>要不这样，坐火车吧</b>，时间不长，也挺方便。", "Tôi muốn đi Nam Kinh nhưng không mua được vé máy bay. — Hay là đi tàu hỏa, thời gian không lâu, cũng tiện."),
   ("A：我不想放弃这么好的工作机会，又想读研究生。 B：<b>要不这样，把两种选择的优点都写出来，哪个优点多就选哪个</b>。", "Tôi không muốn bỏ cơ hội việc làm tốt, lại muốn học cao học. — Hay là viết ra ưu điểm của cả hai lựa chọn, bên nào nhiều ưu điểm hơn thì chọn."),
   ("A：小狗走丢了，找了好几天也没找到。 B：<b>要不这样，发个朋友圈吧，知道的人更多，找到的机会也多些</b>。", "Chó con đi lạc, tìm mấy ngày không thấy. — Hay là đăng lên Moments, nhiều người biết hơn thì có thêm cơ hội tìm thấy.")], note='Đáp án gợi ý.'),
 3: dict(guard='这些狮子大小不一', show=[
   ("我选这份工作，不光是因为有收入，更是因为能积累工作经验。", "Tôi chọn công việc này không chỉ vì có thu nhập mà còn vì tích lũy được kinh nghiệm."),
   ("他想在这里定居，不光因为离海近，更因为空气好。", "Anh ấy muốn định cư ở đây không chỉ vì gần biển mà còn vì không khí tốt."),
   ("我回到家乡当老师，不光是因为家人在这里，更是因为这里需要老师。", "Tôi về quê làm giáo viên không chỉ vì gia đình ở đó mà còn vì nơi này cần giáo viên."),
   ("我来中国，不只是为了找工作，更想游遍中国。", "Tôi đến Trung Quốc không chỉ để tìm việc mà còn muốn đi khắp Trung Quốc."),
   ("他去食堂打工，不光因为午饭免费，更是为了挣学费。", "Anh ấy đi làm thêm ở nhà ăn không chỉ vì bữa trưa miễn phí mà còn để kiếm học phí."),
   ("我支持你，不光因为我们是朋友，更因为你是对的。", "Tôi ủng hộ bạn không chỉ vì chúng ta là bạn mà còn vì bạn đúng.")], note='Đáp án gợi ý (不光……，更……).'),
 4: dict(guard='不一/各异', show=[
   ("猫的喜好不一，有的爱吃鱼，有的爱吃鸡肉，还有爱吃大白菜的。", "Sở thích của mèo mỗi con một khác: con thích cá, con thích thịt gà, lại có con thích cải thảo."),
   ("照片里的孩子们神态各异，可是个个都很可爱。", "Thần thái của các em trong ảnh mỗi em một vẻ, nhưng em nào cũng đáng yêu."),
   ("你看，天上的白云形态各异，有的像山，有的像花，有的像动物，太有意思啦。", "Nhìn kìa, mây trắng trên trời muôn hình muôn vẻ: đám giống núi, đám giống hoa, đám giống động vật, thú vị quá."),
   ("这些产品外观设计各异，功能不一，满足了各类消费者的需求。", "Các sản phẩm này thiết kế bề ngoài mỗi loại một kiểu, chức năng khác nhau, đáp ứng nhu cầu của nhiều loại khách hàng.")], note='Đáp án gợi ý (不一 / 各异).'),
 6: dict(guard='二、参考注释', refill=['表现|露出|显露','表现|露出|显露','显露|显现|显示','显摆|显耀','各显其能|大显身手|大显神通','显微镜','要点|简要|概要','次要'], show=[
   ("“显”的意思是：表现、露出。", "“显” nghĩa là: biểu hiện, lộ ra."),
   ("(一) (1) <b>显露/显现/显示</b> · (2) <b>显摆/显耀</b> · (3) <b>各显其能/大显身手</b> · (4) <b>显微镜</b>", "Điền: 显露 · 显摆 · 各显其能 · 显微镜"),
   ("(二) (1) 只记<b>要点</b>就可以 · (2) <b>次要</b>人物", "Điền: 要点 · 次要")], note='Đã bổ sung ô còn thiếu ở thẻ này.'),
 13: dict(guard='九、写一写', show=[("Dàn ý gợi ý (280–300 chữ): ① 介绍一座桥(如赵州桥)；② 它的<b>设计</b>与<b>建造</b>；③ <b>形态</b>优美，结构<b>坚固</b>，<b>实用</b>：<b>连接</b>两岸；④ 不光……，更……：评价它的价值。", "")], note='Bài viết tự do — chỉ là dàn ý gợi ý.'),
 14: dict(guard='中国石拱桥', refill=['B','E','C','A','D'], **CHOICE),
 15: dict(guard='选句填空', **CHOICE),
 16: dict(guard='十一、拓展学习', show=CHOICE['show'] + [("Câu 2–3: tự học — ghi lại chữ/câu chưa hiểu và hỏi thầy cô hoặc thảo luận.", "")], note='Câu 1 (选句填空) đáp án suy ra từ ngữ cảnh; câu 2–3 là bài tự học.'),
}
