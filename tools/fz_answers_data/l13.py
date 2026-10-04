# -*- coding: utf-8 -*-
ANS = {
 1: dict(guard='因其在专业方面', show=[
   ("大卫接到了<b>一个从中国打来的陌生</b>电话。", "David nhận được một cuộc điện thoại lạ gọi từ Trung Quốc."),
   ("他住在<b>学校宽敞明亮的、有简单电器的</b>宿舍里。", "Anh sống trong ký túc xá của trường rộng rãi, sáng sủa, có đồ điện đơn giản."),
   ("这是<b>朋友送的一本有趣的汉语故事</b>书。", "Đây là quyển truyện tiếng Hán thú vị do bạn tặng."),
   ("她是<b>一位给人留下很深印象的聪明漂亮的女</b>同学。", "Cô là một nữ sinh thông minh xinh đẹp, để lại ấn tượng sâu sắc.")], note='Thứ tự định ngữ gợi ý (số lượng → thuộc về/đặc điểm → tính chất → trung tâm ngữ).'),
 2: dict(guard='于是他们决定做个小游戏', show=[
   ("<b>因天气原因</b>，周末的讲座被取消了。", "Do thời tiết, buổi giảng cuối tuần bị hủy."),
   ("我们这个小山村<b>因风景优美</b>，被喜爱大自然的游客热情追捧。", "Làng núi nhỏ này vì phong cảnh đẹp nên được du khách yêu thiên nhiên đón nhận nhiệt tình."),
   ("因具有极强的感染力，《黄河大合唱》<b>被誉为经典</b>。", "Do có sức lay động rất mạnh, 《Hoàng Hà đại hợp xướng》 được ca ngợi là tác phẩm kinh điển."),
   ("太极拳因能强身健体，<b>被越来越多的人喜爱</b>。", "Thái cực quyền vì rèn luyện thể chất nên được ngày càng nhiều người yêu thích.")], note='Đáp án gợi ý (因A，被B).'),
 3: dict(guard='各自把这个学生的名字写下来，然后', show=[
   ("新年晚会上，同学们<b>各自表演了拿手的节目</b>。", "Trong buổi tiệc năm mới, các bạn mỗi người biểu diễn một tiết mục sở trường."),
   ("生日那天，我们<b>各自许了愿</b>。", "Ngày sinh nhật, hai chị em mỗi người ước một điều."),
   ("上完课，同学们<b>各自回宿舍了</b>。", "Học xong, các bạn ai về ký túc xá nấy."),
   ("父母<b>支持我们各自的兴趣爱好</b>。", "Bố mẹ ủng hộ sở thích riêng của từng người chúng tôi.")], note='Đáp án gợi ý (各自).'),
 4: dict(guard='省得', show=[
   ("现在是旅游旺季，我配了两副眼镜，<b>省得坏了没得用</b>。", "Tôi làm hai cặp kính, đỡ lúc hỏng không có mà dùng."),
   ("骑车去吧，<b>省得迟到</b>。", "Đi xe đạp đi, kẻo muộn."),
   ("看电视声音小点儿，<b>省得邻居不高兴</b>。", "Xem tivi nhỏ tiếng thôi, kẻo hàng xóm khó chịu."),
   ("你要是来，先打个电话，<b>省得白跑一趟</b>。", "Nếu bạn đến, gọi điện trước, kẻo đi uổng công."),
   ("天气不好，带把伞，<b>省得淋雨</b>。", "Thời tiết xấu, mang ô, kẻo bị ướt mưa."),
   ("多吃点儿，<b>省得饿</b>。", "Ăn nhiều chút, kẻo đói.")], note='Đáp án gợi ý (省得 = để khỏi, kẻo).'),
 5: dict(guard='一、字词知识与练习', show=[
   ("馒 mán：馒头。词语：馒头、花卷馒头。", "Bánh bao không nhân. Từ: màn thầu."),
   ("饿 è：肚子空，想吃东西。词语：饥饿、饿死、挨饿。", "Đói. Từ: đói khát, chết đói, nhịn đói."),
   ("馍 mó：用面粉做的主食。词语：馍馍、白面馍。", "Bánh làm từ bột mì. Từ: bánh mì hấp, bánh bột trắng."),
   ("饼 bǐng：扁圆形的面食。词语：饼干、月饼、烙饼。", "Bánh dẹt tròn. Từ: bánh quy, bánh trung thu, bánh áp chảo.")], note='Đáp án gợi ý (tra từ điển).'),
 6: dict(guard='二、参考注释', refill=['听|用耳朵接收声音','接听','聆听|静听','听众','听诊器','观众|听众','大众化','当众','众口难调'], show=[
   ("“听”的意思是：用耳朵接收声音。", "“听” nghĩa là: dùng tai tiếp nhận âm thanh."),
   ("(一) (1) <b>接听</b> · (2) <b>聆听/静听</b> · (3) <b>听众</b> · (4) <b>听诊器</b>", "Điền: 接听 · 聆听 · 听众 · 听诊器"),
   ("(二) (1) <b>观众</b> · (2) <b>大众化</b> · (3) <b>当众</b> · (4) <b>众口难调</b>", "Điền: 观众 · 大众化 · 当众 · 众口难调")], note='Đáp án gợi ý, có chấm tự động theo các từ trên.'),
 7: dict(guard='三、选择合适的词语填空', refill=['博学','颇','渊博','一流','勉励','出色','杰出'], show=[
   ("一位<b>博学</b>的家庭教师 · 成长<b>颇</b>有帮助 · 学识<b>渊博</b> · <b>一流</b>人才 · <b>勉励</b>自己 · <b>出色</b>的研究成果 · <b>杰出</b>的贡献", "Điền: 博学 · 颇 · 渊博 · 一流 · 勉励 · 出色 · 杰出")], note='Đáp án suy ra từ ngữ cảnh và bảng từ.'),
 8: dict(guard='四、用指定词语或格式完成句子', show=[
   ("他举起酒杯向帮助过他的亲朋好友<b>致谢</b>，表达深深的感激之情。", "Anh nâng ly cảm tạ người thân bạn bè từng giúp mình, bày tỏ lòng biết ơn sâu sắc."),
   ("去南方旅游，一定要<b>留意天气变化</b>，及时带上雨伞。", "Đi du lịch miền Nam nhất định phải để ý thời tiết, kịp mang ô."),
   ("苏州、杭州美景名满天下，素有“人间天堂”<b>之誉</b>。", "Cảnh đẹp Tô Châu, Hàng Châu nổi tiếng thiên hạ, vốn được mệnh danh “thiên đường nhân gian”."),
   ("很久没有欣赏晚霞了，更没有工夫静下来<b>聆听大自然的声音</b>。", "Lâu rồi không ngắm hoàng hôn, càng không có thời gian lặng xuống lắng nghe tiếng thiên nhiên."),
   ("我昨天刚说以后不再吃快餐了，你今天就<b>用快餐来引诱我</b>，放心，我是不会动心的。", "Hôm qua tôi vừa nói sẽ không ăn đồ ăn nhanh nữa, hôm nay bạn đã dùng nó để cám dỗ tôi, yên tâm, tôi sẽ không lung lay."),
   ("听说保单的第一条就明确告知客户<b>享有十天</b>“犹豫期”，对吗？", "Nghe nói điều khoản đầu của hợp đồng bảo hiểm nêu rõ khách hàng được hưởng “thời gian cân nhắc” mười ngày, đúng không?"),
   ("<b>因随意采摘</b>野花，就会<b>被罚款</b>。", "Vì tùy tiện hái hoa dại, sẽ bị phạt tiền."),
   ("在汉语口语表达方面，她<b>表现得很出色</b>。", "Về khẩu ngữ tiếng Hán, cô thể hiện rất xuất sắc.")], note='Đáp án gợi ý.'),
 9: dict(guard='五、用指定词语完成对话', show=[
   ("但也提醒你啊，<b>要警惕骄傲情绪</b>，只要有了骄傲之心，就很容易退步。", "Cũng nhắc bạn, phải cảnh giác với tính kiêu ngạo, hễ có lòng kiêu ngạo thì dễ thụt lùi."),
   ("你这办法<b>真高明</b>，双方都很满意，不得不佩服！", "Cách của bạn thật cao tay, hai bên đều hài lòng, phải khâm phục!"),
   ("<b>别管闲事了</b>，人家是夫妻，没准一会儿就好了。", "Đừng xen vào chuyện người ta, họ là vợ chồng, biết đâu lát nữa lại hòa."),
   ("跑一趟超市就多买点儿，<b>省得以后再跑</b>。", "Đi siêu thị một chuyến thì mua nhiều chút, đỡ phải đi lại."),
   ("好，咱们<b>后会有期，多多珍重</b>。", "Được, chúng ta hẹn ngày gặp lại, bảo trọng nhé."),
   ("是啊，<b>他们每天限量供应</b>，不然，很多人排队都买不上。", "Ừ, họ bán giới hạn mỗi ngày, nếu không nhiều người xếp hàng cũng không mua được."),
   ("<b>未必通不过</b>，人家公司也是根据自己的岗位要求招人，主要还是看你符合不符合人家的要求。", "Chưa chắc không qua, họ tuyển theo yêu cầu vị trí, chủ yếu xem bạn có phù hợp không."),
   ("<b>她很有学问</b>，文史地、数理化，包括外语，什么问题都难不倒她。", "Cô ấy rất học rộng, văn sử địa, toán lý hóa, kể cả ngoại ngữ, vấn đề gì cũng khó không nổi cô.")], note='Đáp án gợi ý.'),
 10: dict(guard='六、用指定词语改写句子', show=[
   ("明天还得来，你今天就别回去了，<b>省得</b>来回跑多累。", "Mai còn phải đến, hôm nay bạn đừng về, kẻo đi lại mệt."),
   ("他童年时，父亲<b>正值壮年</b>，在一家科研单位工作，只记得父亲天天早出晚归，周末才能在家待一天。", "Thời thơ ấu của anh, cha đang tuổi sung sức, làm ở một đơn vị nghiên cứu, chỉ nhớ cha sớm đi tối về, cuối tuần mới ở nhà một ngày."),
   ("据说，全球互联网<b>领袖</b>下周要召开一个重要会议。", "Nghe nói các lãnh đạo Internet toàn cầu tuần sau sẽ họp một cuộc họp quan trọng."),
   ("要玩儿这个游戏，你就得<b>守规则</b>。", "Muốn chơi trò này thì bạn phải tuân thủ luật."),
   ("他十四岁就离开家，到国外<b>求学</b>了。", "Mười bốn tuổi anh đã rời nhà, ra nước ngoài du học."),
   ("他是一个<b>博学</b>的人，数学、物理、地理、历史，没有他不会的。", "Anh là người uyên bác, toán, lý, địa, sử, không gì anh không biết.")], note='Đáp án gợi ý.'),
 11: dict(guard='七、在理解课文', show=[("Hai câu mở: tóm tắt nội dung bức thư của Hồ Thích gửi bà Ngô Kiện Hùng bằng lời của bạn, và tự giới thiệu theo vai Ngô Kiện Hùng dựa vào bài khóa — không có đáp án cố định.", "")], note='Bài trả lời tự do.'),
 12: dict(guard='八、参考提示', show=[
   ("A：<b>“有”的意思到底有哪些呢</b>？（表示探究）", "“有” rốt cuộc có những nghĩa nào?"),
   ("A：明白了。<b>此外</b>，<b>“有”还可以表示估量、达到</b>，如“有谁去、有一米长、那棵树有五层楼那么高”。（表示补充）", "Hiểu rồi. Ngoài ra, “有” còn biểu thị ước lượng, đạt tới."),
   ("B：<b>没错</b>。（表示同意）", "Đúng thế."),
   ("A：<b>这是为什么呢</b>？（表示探究）", "Đó là vì sao?"),
   ("A：声誉、权利、自由？<b>应该是吧</b>。（表示不确定）", "Danh tiếng, quyền lợi, tự do? Chắc là vậy."),
   ("B：<b>没错，除了这些</b>，还有义务、地位，再有也不会太多了。（表示补充）", "Đúng, ngoài những thứ này còn có nghĩa vụ, địa vị."),
   ("B：<b>太对了</b>！（表示同意）", "Quá đúng!")], note='Đáp án gợi ý (đúng chức năng ghi trong ngoặc).'),
 13: dict(guard='十、阅读短文', fill=['C','D','B','A','E'], show=[
   ("(1) <b>C</b> 昨儿整整一天若有所失", "(1) C — hôm qua cả ngày thấy như mất mát gì"),
   ("(2) <b>D</b> 我愈来愈爱你了", "(2) D — ba càng ngày càng yêu con"),
   ("(3) <b>B</b> 我不是说你应当时时刻刻觉得自己了不起", "(3) B — ba không nói con phải lúc nào cũng thấy mình giỏi"),
   ("(4) <b>A</b> 还有一大半要你自己来做了", "(4) A — còn một nửa lớn phải do chính con làm"),
   ("(5) <b>E</b> 那么你这朵花一定能开得更美，更丰满，更有力，更长久", "(5) E — thì đóa hoa của con nhất định sẽ nở đẹp, đầy đặn, mạnh mẽ và bền lâu hơn")], note='Đáp án suy ra từ ngữ cảnh (câu 3 là câu còn lại sau khi loại các câu khác).'),
 14: dict(guard='十一、拓展学习', show=[("Gợi ý từ có chữ “自”: 自信、自觉、自由、自然、自己、自学、自省、自豪、自责、自立、自私、自从、自古。", "Gợi ý: tự tin, tự giác, tự do, tự nhiên, bản thân, tự học, tự xét mình, tự hào, tự trách, tự lập, ích kỷ, kể từ, từ xưa…"),
                                             ("Các câu còn lại: bài mở rộng, không có đáp án cố định.", "")], note='Bài mở rộng.'),
}
