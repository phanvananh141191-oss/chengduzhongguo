# Cách học: ảnh minh hoạ + thẻ hướng dẫn cho từng giáo trình (dựng bằng HTML, ảnh nhúng base64)
import base64,html
G={
'fz':dict(c='#147d6c',kick='01 / Giáo trình tổng hợp',t='Phát triển Hán ngữ',sub='Học từ, cấu trúc, nghe hiểu và diễn đạt ý bài khóa.',alt='Phát triển Hán ngữ: 6 bước học một bài',
 steps=[('Quét bài','Tự thử từ và cấu trúc. Phần đã biết đi nhanh; chỉ học sâu chỗ còn hổng.'),('Đọc & nghe bài khóa','Nắm ý chính; nghe đoạn mới 3–5 phút trước khi xem lời thoại. Đóng sách kể lại.'),('Chọn từ mới','Ưu tiên từ cần dùng hoặc gặp nhiều. Bắt đầu tối đa 12 thẻ mỗi bài trung cấp.'),('Dùng ngữ pháp','Tự đặt câu mới với cấu trúc quan trọng; sửa một lỗi dễ nhầm bằng cặp sai–đúng.'),('Làm bài tập','Chọn bài nhớ lại, bài nghe ngắn và bài tự nói/viết. Tối đa 20 phút trong giờ học sách.'),('Đóng sách kiểm tra','Nói lại ý chính và dùng cấu trúc trong câu của mình; có thể ghi âm tối đa 5 câu.')],
 rv=('Ôn & kiểm tra','Ôn thẻ tối đa 20 phút/ngày. Sau ít nhất 7 ngày, thử dùng lại nội dung cũ. Cứ 5 bài làm 20 câu trộn, hướng tới 16/20.'),
 nh='Ngày 60 phút học song song: tối đa 25 phút cho sách này.'),
'ky':dict(c='#7953b6',kick='02 / Khẩu ngữ',t='Khẩu ngữ thời đại mới',sub='Mỗi bài hoàn thành một nhiệm vụ nói bằng lời của mình.',alt='Khẩu ngữ thời đại mới: 5 bước học một bài',
 steps=[('Xem nhiệm vụ','Đọc phần nhiệm vụ (iPRODUCE) trước. Gạch 3 ý muốn nói; lập ý tối đa 3 phút.'),('Lấy cụm cần dùng','Xem phần chuẩn bị (iPREPARE). Nghe hội thoại khi chưa nhìn chữ, rồi kiểm bằng lời thoại.'),('Rút khung diễn đạt','Chọn 2–3 khung để nêu ý, giải thích, phản bác hoặc nhượng bộ. Không học thuộc cả hội thoại.'),('Nói và ghi âm','Kể lại ngắn, rồi trả lời nhiệm vụ không đọc giấy. Nghe lại và sửa sau khi nói xong.'),('Ôn bằng miệng','Nhìn tình huống gợi ý, nói khung phù hợp và đặt thêm một câu mới.')],
 rv=('Ôn & kiểm tra','Sau ít nhất 48 giờ, nói lại không nhìn giấy. Mỗi tuần ghi âm 5 phút với câu hỏi mới; kiểm thời lượng, độ tự nhiên và cách dùng khung.'),
 nh='Ngày 60 phút: ghi khoảng 90 giây; ngày 90 phút: 2–3 phút. Phần khẩu ngữ tối đa 45 phút khi học song song.'),
'ld':dict(c='#276b9d',kick='04 / Đọc hiểu',t='Lạc Độc',sub='Tập 3–6: đọc bài lạ, nắm ý chính và vận dụng kỹ năng đọc.',alt='Lạc Độc – Đọc hiểu: 5 bước học một bài',
 steps=[('Đọc lần đầu','Tắt pinyin và audio, bấm giờ, chưa tra từ. Đọc xong tự nêu ý chính.'),('Đọc kỹ','Tra từ thực sự cản hiểu. Nói lại tối đa 2 câu khó bằng tiếng Trung đơn giản.'),('Áp dụng kỹ năng','Chọn 1–2 kỹ năng trong bài và dùng ngay trên văn bản thực hành.'),('Đóng sách tóm tắt','Ghi âm 3–4 câu tiếng Trung nêu ý chính; dùng ít nhất một cấu trúc vừa học.'),('Ôn từ trong câu','Từ chỉ cần để đọc thì luyện nhận nghĩa. Từ sắp nói/viết mới tập tự tạo câu.')],
 rv=('Ôn & kiểm tra','Ngày 7 và 30: đóng sách nhắc lại ý chính. Sau mỗi 3 bài, thay một buổi bằng bài đọc lạ tối đa 20 phút, tra tối đa 8 từ.'),
 nh='Nếu hiểu dưới 3/4 ý chính, chọn bài dễ hơn. Đọc bài lạ ngoài sách 3 lần/tuần, mỗi lần tối đa 15 phút.'),
}
def build(rd_bin):
    e=html.escape; parts=[]
    for b,g in G.items():
        img='data:image/webp;base64,'+base64.b64encode(rd_bin('nguon/cach-hoc/%s.webp'%b)).decode()
        st=''.join('<li><b>%s</b><span>%s</span></li>'%(e(a),e(d)) for a,d in g['steps'])
        parts.append('<div class="gd-pg" data-gb="%s" hidden style="--gc:%s"><img class="gd-img" src="%s" alt="%s" loading="lazy"><div class="gd-card"><div class="gd-hd"><small>%s</small><h3>%s</h3><p>%s</p></div><div class="gd-bd"><h4>Mở sách → làm gì?</h4><ol>%s</ol><div class="gd-rv"><b>%s</b><span>%s</span></div><p class="gd-nh"><b>Nhớ</b> %s</p><p class="gd-ft">Một bài học = một đầu ra tự kiểm tra được</p></div></div></div>'%(b,g['c'],img,e(g['alt']),e(g['kick']),e(g['t']),e(g['sub']),st,e(g['rv'][0]),e(g['rv'][1]),e(g['nh'])))
    return '<div id="gdback"></div><div id="gd" role="dialog" aria-modal="true" aria-label="Cách học" hidden><div class="gd-top"><b>Cách học</b><button class="tbn" id="gdx" aria-label="Đóng">✕</button></div><div class="gd-sc">'+''.join(parts)+'</div></div>'
CSS='''
#gdback{position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:200;display:none}
#gd{position:fixed;z-index:201;top:0;bottom:0;right:0;width:min(560px,100%);background:var(--u-bg);color:var(--u-fg);display:flex;flex-direction:column;box-shadow:-8px 0 30px rgba(0,0,0,.25)}
#gd[hidden]{display:none}
body.gd-on #gdback{display:block}
.gd-top{display:flex;align-items:center;justify-content:space-between;padding:8px 12px;border-bottom:1px solid var(--u-line);font-size:16px}
.gd-sc{overflow:auto;padding:12px;flex:1;-webkit-overflow-scrolling:touch}
.gd-pg[hidden]{display:none}
.gd-img{display:block;width:100%;max-width:420px;height:auto;margin:0 auto 14px;border-radius:14px;background:#fff}
.gd-card{border-radius:20px;overflow:hidden;background:var(--u-card);border:1px solid var(--u-line)}
.gd-hd{background:var(--gc);color:#fff;padding:16px 18px}
.gd-hd small{display:block;font-weight:700;text-transform:uppercase;opacity:.9;font-size:12px}
.gd-hd h3{margin:4px 0;font-size:24px;line-height:1.2;text-transform:uppercase}
.gd-hd p{margin:0;font-size:14px;opacity:.95}
.gd-bd{padding:14px 14px 16px}
.gd-bd h4{margin:2px 4px 10px;color:var(--gc);font-size:13px;text-transform:uppercase}
.gd-bd ol{list-style:none;margin:0;padding:0;counter-reset:g;display:grid;gap:8px}
.gd-bd li{counter-increment:g;position:relative;background:var(--u-ghost);border-radius:12px;padding:10px 12px 10px 52px;display:grid;gap:2px}
.gd-bd li::before{content:counter(g);position:absolute;left:12px;top:12px;width:28px;height:28px;border-radius:50%;background:var(--gc);color:#fff;display:grid;place-items:center;font-weight:700;font-size:14px}
.gd-bd li b{text-transform:uppercase;font-size:14px}.gd-bd li span{font-size:14px;opacity:.8;line-height:1.5}
.gd-rv{margin-top:12px;background:var(--gc);color:#fff;border-radius:12px;padding:12px 14px;display:grid;gap:4px;font-size:14px;line-height:1.5}.gd-rv b{text-transform:uppercase}
.gd-nh{margin:12px 4px 0;font-size:14px;line-height:1.5;opacity:.85}.gd-nh b{color:var(--gc);text-transform:uppercase;margin-right:8px}
.gd-ft{margin:12px 4px 0;font-weight:700;font-size:13px;color:var(--gc)}
@media(max-width:560px){#gd{width:100%}}
'''
JS='''
(function(){var d=document.getElementById('gd');if(!d)return;
function bk(){return document.documentElement.getAttribute('data-bk')||''}
function open(){var b=bk();var pgs=d.querySelectorAll('.gd-pg'),any=false;pgs.forEach(function(p){var on=p.getAttribute('data-gb')===b;p.hidden=!on;any=any||on});if(!any)pgs[0].hidden=false;d.hidden=false;document.body.classList.add('gd-on');d.querySelector('.gd-sc').scrollTop=0;document.getElementById('gdx').focus()}
function close(){d.hidden=true;document.body.classList.remove('gd-on');var t=document.getElementById('t-guide');if(t){t.setAttribute('aria-expanded','false');t.focus()}}
document.addEventListener('click',function(e){var t=e.target;if(t.closest&&t.closest('#t-guide')){e.stopPropagation();document.getElementById('t-guide').setAttribute('aria-expanded','true');open();return}if(t.id==='gdx'||t.id==='gdback')close()},true);
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!d.hidden)close()});
})();
'''
