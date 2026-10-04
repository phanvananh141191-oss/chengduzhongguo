# -*- coding: utf-8 -*-
ANS = {
 1: dict(guard='六月天', show=[
   ("雨给人带来凉爽，雪给人带来惊喜，<b>相比之下，我更喜欢雪</b>。", "Mưa mang lại cho người ta sự mát mẻ, tuyết mang lại bất ngờ; so ra tôi thích tuyết hơn."),
   ("这款手机款式好，质量不错，价格也还行，<b>相比之下，别的牌子就差一些</b>。", "Mẫu điện thoại này kiểu dáng đẹp, chất lượng tốt, giá cũng ổn; so ra các hãng khác kém hơn một chút."),
   ("老李有经验，但遇事容易着急；小李经验没有老李多，但遇到紧急事情能够冷静处理。<b>相比之下，小李更适合处理紧急的事情</b>。", "So ra, Tiểu Lý thích hợp hơn để xử lý việc khẩn cấp."),
   ("<b>这件衣服的蓝色我最喜欢</b>，相比之下，别的颜色的我都不太喜欢。", "Màu xanh của chiếc áo này tôi thích nhất, so ra các màu khác tôi đều không thích lắm.")], note='Đáp án gợi ý (相比之下).'),
 2: dict(guard='秋天是个迷人', show=[
   ("人无远虑，必有近忧。", "Người không biết lo xa tất sẽ có phiền muộn trước mắt."),
   ("良言一句三冬暖，恶语伤人六月寒。", "Một lời tử tế ấm ba mùa đông, lời ác làm tổn thương lạnh cả tháng sáu."),
   ("听君一席话，胜读十年书。", "Nghe bạn nói một buổi còn hơn đọc sách mười năm.")], note='Các câu đầy đủ như trên (tục ngữ/thành ngữ), kèm nghĩa tiếng Việt.'),
 3: dict(guard='各种各样的水果', show=[
   ("苹果<b>不大不小</b>，每人一个。", "Táo không to không nhỏ, mỗi người một quả."),
   ("这种纸不薄不厚，<b>写字正合适</b>。", "Loại giấy này không mỏng không dày, viết vừa đẹp."),
   ("这条裤子不肥不瘦，不长不短，<b>穿着正合适</b>。", "Chiếc quần này không rộng không chật, không dài không ngắn, mặc vừa vặn.")], note='Đáp án gợi ý (不A不B).'),
 4: dict(guard='就这一点来说', show=[
   ("这里好玩儿的地方太多了，我玩儿不过来。", "Ở đây chỗ vui nhiều quá, tôi chơi không xuể."),
   ("展品太多了，我看不过来。", "Hiện vật trưng bày quá nhiều, tôi xem không xuể."),
   ("消息一堆，我回不过来。", "Tin nhắn một đống, tôi trả lời không xuể."),
   ("天上的星星太多了，我数不过来。", "Sao trên trời nhiều quá, tôi đếm không xuể."),
   ("买的东西太多，我一个人拿不过来。", "Đồ mua nhiều quá, một mình tôi xách không xuể."),
   ("我刚到中国，新鲜事太多，适应不过来。", "Tôi mới đến Trung Quốc, chuyện mới lạ quá nhiều, thích ứng không kịp.")], note='Đáp án gợi ý (V不过来).'),
 5: dict(guard='就……来说', show=[
   ("就幽默感来说，我爸比我妈强。", "Xét về óc hài hước, bố tôi hơn mẹ tôi."),
   ("就卫生条件来说，这家宾馆很不错。", "Xét về điều kiện vệ sinh, khách sạn này rất tốt."),
   ("就价格来说，这款手机很划算。", "Xét về giá, chiếc điện thoại này rất hời."),
   ("就身高来说，他当篮球运动员很合适。", "Xét về chiều cao, anh ấy làm vận động viên bóng rổ rất hợp."),
   ("就爱好来说，我更愿意去旅游。", "Xét về sở thích, tôi muốn đi du lịch hơn."),
   ("就口味来说，我更喜欢吃辣的。", "Xét về khẩu vị, tôi thích đồ cay hơn.")], note='Đáp án gợi ý (就……来说).'),
 6: dict(guard='一、字词知识与练习', show=[
   ("晓 xiǎo：天亮；知道、明白。词语：拂晓、晓得、家喻户晓。", "Tảng sáng; biết, hiểu. Từ: rạng đông, biết, nhà nhà đều biết."),
   ("早 zǎo：清晨；时间在前的。词语：早上、早晨、早餐、早已。", "Sáng sớm; sớm. Từ: buổi sáng, bữa sáng, đã từ lâu."),
   ("暇 xiá：空闲。词语：闲暇、无暇、暇时。", "Rảnh rỗi. Từ: lúc nhàn rỗi, không rảnh, thời gian rảnh."),
   ("昭 zhāo：明显、显著。词语：昭示、昭然若揭、昭雪。", "Rõ ràng, sáng tỏ. Từ: chỉ rõ, rõ như ban ngày, rửa oan.")], note='Đáp án gợi ý (tra từ điển).'),
 7: dict(guard='二、参考注释', refill=['新的|刚出现的','新手','新颖|新奇','尝新','温故知新','独创','独到','独木桥','独自'], show=[
   ("“新”的意思是：刚出现的、新的。", "“新” nghĩa là: mới xuất hiện, mới."),
   ("(1) <b>新手</b>司机 · (2) 十分<b>新颖</b>独特 · (3) 快来<b>尝新</b> · (4) <b>温故知新</b>的感觉", "Điền: 新手 · 新颖 · 尝新 · 温故知新"),
   ("(二) (1) <b>独创</b> · (2) <b>独到</b>的见解 · (3) <b>独木桥</b> · (4) <b>独自</b>一人", "Điền: 独创 · 独到 · 独木桥 · 独自")], note='Đáp án gợi ý, có chấm tự động theo các từ trên.'),
 8: dict(guard='三、想一想下面两类词语', refill=['长长','凉凉','明晃晃','厚厚','暖洋洋|热乎乎','黑洞洞|黑乎乎','深深','紧紧','喜洋洋','香喷喷'], show=[
   ("长长的小路 · 凉凉的 · 明晃晃的太阳 · 厚厚一层 · 暖洋洋的 · 黑洞洞的 · 深深地印在心里 · 紧紧地抓住 · 喜洋洋的节日气氛 · 香喷喷的饭菜", "Dài dằng dặc · mát mát · chói chang · dày một lớp · ấm áp · tối om · khắc sâu · nắm chặt · không khí hân hoan · cơm canh thơm phức")],
   note='Nhóm A (AA): 长长 凉凉 厚厚 深深 紧紧; nhóm B (ABB): 明晃晃 暖洋洋 黑洞洞 喜洋洋 香喷喷.'),
 9: dict(guard='四、选择合适的词语或格式填空', refill=['温暖','播种','炎热','哗哗','闷热','凉爽','清新','庄稼','吃不过来','各种各样','赛过','心醉'], show=[
   ("沐浴着<b>温暖</b>的春风，农民开始<b>播种</b>下一年的希望。转眼就是<b>炎热</b>的夏天，<b>哗哗</b>地下了一场大雨，人们一下子摆脱了长夏的<b>闷热</b>，享受着雨后的<b>凉爽</b>和空气的<b>清新</b>，<b>庄稼</b>也喝足了水，长得更快了。秋天到了，……不仅有<b>吃不过来</b>的葡萄、苹果等<b>各种各样</b>的水果，……美得<b>赛过</b>天堂，美得让人<b>心醉</b>！", "Điền: 温暖 · 播种 · 炎热 · 哗哗 · 闷热 · 凉爽 · 清新 · 庄稼 · 吃不过来 · 各种各样 · 赛过 · 心醉")], note='Đáp án suy ra từ ngữ cảnh và bảng từ.'),
 10: dict(guard='五、用指定词语或格式完成句子', show=[
   ("很遗憾，这次实验因为准备不充分，<b>宣告失败了</b>。", "Rất tiếc, lần thí nghiệm này do chuẩn bị chưa đầy đủ nên tuyên bố thất bại."),
   ("百合花<b>极其普通</b>，她没有漂亮的颜色，没有吸引人的身姿，几乎没人注意到她的存在。", "Hoa bách hợp vô cùng bình thường…"),
   ("快帮帮我，我就有两只手，这么多东西，我<b>拿不过来</b>了。", "Giúp tôi với, tôi chỉ có hai tay, nhiều đồ thế này tôi xách không xuể."),
   ("刚吃完火锅，你再拿出多<b>可口的菜</b>，我也吃不下了。", "Vừa ăn xong lẩu, bạn có mang ra món ngon đến mấy tôi cũng không ăn nổi."),
   ("<b>熬过</b>考试周，我们就可以去公园放松放松了。", "Chịu đựng qua tuần thi, chúng ta có thể ra công viên thư giãn."),
   ("这所小学每天早上免费给孩子们<b>供应牛奶</b>，保证孩子们的身体健康。", "Trường tiểu học này mỗi sáng cung cấp sữa miễn phí cho các em để đảm bảo sức khỏe."),
   ("当我在电脑前学习时，小猫会<b>时不时跑过来趴在键盘上</b>。", "Khi tôi học trước máy tính, chú mèo thỉnh thoảng lại chạy đến nằm lên bàn phím."),
   ("我最喜欢看她笑，<b>她的笑容迷人极了</b>。", "Tôi thích nhất nhìn cô ấy cười, nụ cười của cô ấy thật quyến rũ.")], note='Đáp án gợi ý.'),
 11: dict(guard='六、用指定词语完成对话', show=[
   ("汉语<b>里这叫“闷热”</b>。", "Trong tiếng Hán cái này gọi là “闷热” (oi bức)."),
   ("这里却<b>格外凉爽</b>。", "Còn ở đây lại mát mẻ lạ thường."),
   ("<b>真遗憾啊</b>，以后有机会再来北京，我专门陪你去。", "Tiếc thật, sau này có dịp lại đến Bắc Kinh, tôi sẽ đặc biệt đưa bạn đi."),
   ("据说有<b>三十八度</b>。", "Nghe nói lên đến 38 độ."),
   ("用什么词语形容<b>秋天的色彩</b>？", "Dùng từ gì để miêu tả sắc màu mùa thu?"),
   ("苏州、杭州就是<b>人间天堂</b>啊。", "Tô Châu, Hàng Châu chính là thiên đường nơi trần thế."),
   ("好老师就是这样，<b>有独特的魅力</b>。", "Thầy giỏi là như vậy, có sức hút riêng.")], note='Đáp án gợi ý.'),
 12: dict(guard='七、用指定词语或格式改写句子', show=[
   ("母亲在孩子心中的地位是<b>无可替代的</b>。", "Vị trí của người mẹ trong lòng con là không gì thay thế được."),
   ("比赛现场，球迷<b>的紧张赛过了</b>参加比赛的球员。", "Tại hiện trường, sự căng thẳng của cổ động viên còn hơn cả cầu thủ."),
   ("中国女排以前<b>曾</b>连续五次获得世界冠军。", "Đội bóng chuyền nữ Trung Quốc trước đây từng năm lần liên tiếp vô địch thế giới."),
   ("昨天一口气把十集电视剧都看完了，真<b>过瘾</b>。", "Hôm qua xem một mạch hết mười tập phim, thật đã."),
   ("<b>就保暖来说</b>，这种面料更适合做冬装。", "Xét về giữ ấm, loại vải này hợp may đồ mùa đông hơn."),
   ("漫山遍野的百合花开了，<b>数也数不过来</b>。", "Hoa bách hợp nở khắp núi đồi, đếm cũng không xuể."),
   ("这种冰激凌的口味<b>很独特</b>。", "Hương vị loại kem này rất độc đáo.")], note='Đáp án gợi ý.'),
 13: dict(guard='八、在理解课文', show=[("Câu hỏi mở theo bài khóa: nêu điểm giống/khác của mùa đông Nam – Bắc và kể lại mùa bạn ấn tượng nhất bằng lời của mình (có thể dùng 相比之下, 就……来说, 不A不B).", "")], note='Bài trả lời tự do.'),
 14: dict(guard='九、参考提示', show=[
   ("还没确定，<b>心里总是拿不定主意</b>。（表示感受）", "Vẫn chưa chắc, trong lòng cứ phân vân mãi."),
   ("这个学校世界排名<b>不高不低</b>，评价一般。（表示评价）", "Trường này xếp hạng thế giới không cao không thấp, đánh giá trung bình."),
   ("是的，<b>就专业来说</b>，大家还是很认可的。（表示评价）", "Đúng, xét về chuyên ngành thì mọi người vẫn công nhận."),
   ("中国话<b>管这个叫</b>“吃着碗里的，看着锅里的”。（管A叫B）", "Tiếng Trung gọi chuyện này là “ăn trong bát, nhìn trong nồi”.")], note='Đáp án gợi ý.'),
 15: dict(guard='十、与大家分享', show=[("Bài thực hành: giới thiệu mùa đẹp nhất ở quê bạn, kèm ảnh làm PPT — không có đáp án cố định.", "")], note='Bài thực hành.'),
 16: dict(guard='十一、阅读短文', fill=['B','D','C','E','A'], show=[
   ("(1) <b>B</b> 一年到头都有故事", "(1) B — quanh năm đều có chuyện"),
   ("(2) <b>D</b> 就是满满一大篮子", "(2) D — là đầy cả một giỏ lớn"),
   ("(3) <b>C</b> 小麦成熟了", "(3) C — lúa mì chín rồi"),
   ("(4) <b>E</b> 到处都晾晒着收获的粮食", "(4) E — khắp nơi phơi lương thực thu hoạch"),
   ("(5) <b>A</b> 等池塘里的冰冻结实了", "(5) A — đợi băng trong ao đóng chắc")], note='Đáp án suy ra từ ngữ cảnh đoạn văn; câu tự học không có đáp án.'),
 17: dict(guard='十二、拓展学习', show=[("Bài mở rộng (tìm lời bài 《四季歌》 của Nhật; tìm câu tương tự “六月天，孩子脸” trong tiếng mẹ đẻ) — không có đáp án cố định.", "")], note='Bài mở rộng.'),
}
