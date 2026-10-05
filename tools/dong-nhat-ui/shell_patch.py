# chạy trong build.py: biến `out` là HTML vỏ; dùng must_replace
import re
# ---- HTML: bỏ nút Tuỳ chọn khỏi thanh trên, thêm thanh công cụ học ----
a=out.index('  \n  <button class="ib" id="optb"') if '  \n  <button class="ib" id="optb"' in out else out.index('<button class="ib" id="optb"')
b=out.index('</header>',a)
old_block=out[a:b]
out=out[:a]+out[b:]
tools='''<div id="tools" class="tools" role="toolbar" aria-label="Công cụ học">
  <button class="tbn" id="t-py" aria-pressed="true" title="Hiện / ẩn pinyin trên chữ Hán"><span class="ti" aria-hidden="true">拼</span><span class="tl">Hiện pinyin</span></button>
  <button class="tbn" id="t-tr" aria-pressed="true" title="Hiện / ẩn bản dịch tiếng Việt dưới câu, đoạn"><span class="ti" aria-hidden="true">VI</span><span class="tl">Hiện dịch</span></button>
  <span class="tgrp" role="group" aria-label="Cỡ chữ"><button class="tbn" id="t-fm" aria-label="Chữ nhỏ hơn">A−</button><b id="t-fv" class="tv" aria-live="polite">100%</b><button class="tbn" id="t-fp" aria-label="Chữ lớn hơn">A+</button></span>
  <button class="tbn" id="t-all" aria-pressed="false" title="Đọc liên tục tất cả các phần của bài"><span class="tl">Xem toàn bài</span></button>
  <button class="tbn" id="optb" aria-haspopup="dialog" aria-expanded="false" aria-controls="optp" title="Tuỳ chọn: nền, font và các lớp nội dung"><span class="ti" aria-hidden="true">Aa</span><span class="tl">Tuỳ chọn</span></button>
  <div id="optp" class="opt" role="dialog" aria-label="Tuỳ chọn hiển thị"></div>
</div>
'''
out=must_replace(out,'</header>\n <div id="optback"></div>','</header>\n '+tools+' <div id="optback"></div>',label='tools html')
# ---- CSS ----
css='''
/* ---- thanh công cụ học (dùng chung 3 giáo trình) ---- */
.tools{position:relative;z-index:60;flex:none;display:flex;flex-wrap:wrap;align-items:center;gap:6px;padding:6px 12px;background:var(--u-card);border-bottom:1px solid var(--u-line)}
.tbn{border:1px solid var(--u-line);background:var(--u-card);color:var(--u-fg);border-radius:10px;min-height:40px;min-width:40px;padding:0 12px;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;gap:6px;font-size:14px;font-weight:600;flex:none}
.tbn:hover{background:var(--u-ghost)}
.tbn[aria-pressed=true],#optb[aria-expanded=true]{background:var(--u-fg);color:var(--u-bg);border-color:var(--u-fg)}
.tbn[disabled]{opacity:.4;cursor:default}
.tbn:focus-visible,.ib:focus-visible{outline:2px solid var(--u-ac);outline-offset:2px}
.tbn .ti{font-weight:800}
.tgrp{display:inline-flex;align-items:center;gap:0}
.tgrp .tbn{border-radius:10px 0 0 10px}.tgrp .tbn:last-child{border-radius:0 10px 10px 0}
.tgrp .tv{min-width:54px;height:40px;display:inline-grid;place-items:center;border:1px solid var(--u-line);margin:0 -1px;background:var(--u-ghost);font-size:13px;font-variant-numeric:tabular-nums}
.tools .opt{top:calc(100% + 6px)}
@media(max-width:899px){
  .tbn{min-height:44px;min-width:44px;padding:0 10px}
  .tgrp .tv{height:44px}
  .ib{height:44px;min-width:44px}
  .tools{gap:6px;padding:6px 8px}
  .it{min-height:48px}
}
@media(max-width:560px){.tbn{padding:0 9px}.tbn .ti{display:none}.tbn .tl{font-size:13px}.tools{justify-content:flex-start}}
</style></head>'''
out=must_replace(out,'</style></head>',css,label='shell css')
# bỏ quy tắc cũ ẩn nhãn "Tuỳ chọn" trên điện thoại (nút nay nằm ở thanh công cụ)
out=out.replace('@media(max-width:899px){#optb .dl{display:none}}','')
out=out.replace('@media(max-width:420px){.where .bk{display:none}.ib{min-width:34px;height:34px;padding:0 7px}}','@media(max-width:420px){.where .bk{display:none}.ib{padding:0 7px}}')
# ---- JS ----
out=must_replace(out,"var S={theme:null,py:true,scale:1,opt:null},CAPS={};","var S={theme:null,py:true,scale:1,opt:null,tr:true,all:false},CAPS={};",label='S')
out=must_replace(out,"['tv','Dịch tiếng Việt','bản dịch từng đoạn'],['dv','Dòng tiếng Việt','dòng dịch dưới từng câu'],","",label='layers')
old=out[out.index("  h+='<div class=\"orow\"><span>Cỡ chữ</span>"):out.index("  h+='<div class=\"orow\"><span>Nền</span>")]
out=out.replace(old,'')
out=must_replace(out,"  h+=sw('py','Pinyin trên chữ Hán','',S.py);\n","",label='py switch')
out=must_replace(out,"  renderOpts();\n}\n/* ---- khu Tuỳ chọn","  renderOpts();renderTools();\n}\nfunction renderTools(){\n  var c=(cur&&CAPS[cur.book])||{};\n  function pr(id,v){var b=$(id);if(b)b.setAttribute('aria-pressed',v?'true':'false')}\n  pr('t-py',S.py);pr('t-tr',S.tr);pr('t-all',S.all);\n  $('t-fv').textContent=Math.round(S.scale*100)+'%';\n  $('t-fm').disabled=S.scale<=.8;$('t-fp').disabled=S.scale>=1.5;\n  var tr=$('t-tr'),al=$('t-all');\n  tr.disabled=!c.tr;tr.title=c.tr?'Hiện / ẩn bản dịch tiếng Việt dưới câu, đoạn':'Phần này không có bản dịch đoạn để bật/tắt';\n  al.disabled=!c.all;al.title=c.all?'Đọc liên tục tất cả các phần của bài':'Chỉ dùng cho trang bài học';\n}\n/* ---- khu Tuỳ chọn",label='apply')
out=must_replace(out,"if(m.t==='caps'){CAPS[m.book]=m.caps||{};if(cur&&cur.book===m.book)renderOpts()}","if(m.t==='caps'){CAPS[m.book]=m.caps||{};if(cur&&cur.book===m.book){renderOpts();renderTools()}}",label='caps msg')
out=must_replace(out,"  if(t.closest('.fm')){S.scale","  if(t.closest('#t-py')){S.py=!S.py;apply();return}\n  if(t.closest('#t-tr')){if(!$('t-tr').disabled){S.tr=!S.tr;apply()}return}\n  if(t.closest('#t-all')){if(!$('t-all').disabled){S.all=!S.all;apply()}return}\n  if(t.closest('#t-fm')){S.scale=Math.max(.8,+(S.scale-.08).toFixed(2));apply();return}\n  if(t.closest('#t-fp')){S.scale=Math.min(1.5,+(S.scale+.08).toFixed(2));apply();return}\n  if(t.closest('.fm')){S.scale",label='click')
# setCur cũng cập nhật công cụ
out=must_replace(out,"  renderOpts();\n  document.querySelectorAll('.it')","  renderOpts();renderTools();\n  document.querySelectorAll('.it')",label='setCur')
# chú thích chân mục lục
out=must_replace(out,'Pinyin, cỡ chữ, nền và các lớp nội dung (dịch, nghĩa từ…) nằm ở nút <b>Tuỳ chọn</b> phía trên bên phải','Pinyin, dịch, cỡ chữ, <b>Xem toàn bài</b> và <b>Tuỳ chọn</b> nằm ở thanh công cụ phía trên nội dung',label='foot')

# ---- Cách học (ảnh minh hoạ + thẻ hướng dẫn) ----
import guide
out=must_replace(out,'<button class="tbn" id="optb"','<button class="tbn" id="t-guide" aria-haspopup="dialog" aria-expanded="false" title="Cách học giáo trình này (ảnh minh hoạ)"><span class="ti" aria-hidden="true">📖</span><span class="tl">Cách học</span></button>\n  <button class="tbn" id="optb"',label='guide btn')
out=must_replace(out,' <div id="optback"></div>',' <div id="optback"></div>\n '+guide.build(lambda n:open(os.path.join(HERE,n),'rb').read()),label='guide dlg')
out=must_replace(out,'</style></head>','<style id="gd-css">'+guide.CSS+'</style></head>',label='guide css')
out=must_replace(out,"function renderTools(){\n","function renderTools(){\n  document.documentElement.setAttribute('data-bk',cur?cur.book:'');\n",label='guide bk')
i=out.rindex('</body>'); out=out[:i]+'<script>'+guide.JS+'</script>'+out[i:]
