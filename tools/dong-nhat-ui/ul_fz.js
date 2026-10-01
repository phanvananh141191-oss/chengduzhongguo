/* ===== ULAY · bộ gom bài cho 发展汉语 (D2) ===== */
(function(){
var A=ULAY.arr;
function headPane(t,cur){
  t=t.replace(/\s+/g,' ').trim();
  if(/^Ghi chú của cô|^Ghi chú về phần còn thiếu/.test(t))return 'ex';
  if(/综合注释|Chú thích ngữ pháp|NGỮ PHÁP|语法练习|^Chú thích tổng hợp|^3\.\d/.test(t))return 'gr';
  if(/综合练习|Bài tập|BÀI TẬP|^[一二三四五六七八九十]+、|练习|阅读短文|拓展学习|Học mở rộng|^Trang \d+/.test(t))return 'pr';
  if(/走进课文|课文|Bài khóa|Vào bài đọc|Câu hỏi bên lề|边栏问题|^Chú thích \(注释|^注释|ĐÁP ÁN CÂU HỎI BÀI KHÓA/.test(t))return 'tx';
  if(/词语学习|词语表|Từ vựng/.test(t))return 'vo';
  if(/题解|Giới thiệu|Chú giải/.test(t))return 'ov';
  return cur;
}
A(document.querySelectorAll('section.les')).forEach(function(sec){
  var i=0;A(sec.querySelectorAll('.card.ex')).forEach(function(c){c.setAttribute('data-ux-i',i++)});
  var B={ov:[],vo:[],tx:[],gr:[],pr:[],ex:[]},cur='ov',h1=null;
  A(sec.children).forEach(function(n){
    if(n.tagName==='H1'){h1=n;return}
    if(n.tagName==='H2')cur=headPane(n.textContent,cur);
    B[cur].push(n)});
  var info=ULAY.lessonInfo(sec.id)||{};
  var Lz=ULAY.mount(sec,{key:sec.id,num:+sec.id.slice(1),zhEl:h1,vi:info.vi,buckets:B});
  var g=Lz.querySelector('[data-pane="gr"] .ul-pb');if(g)ULAY.gram(g);
});
})();
