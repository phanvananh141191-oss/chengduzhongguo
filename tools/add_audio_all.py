"""Thanh nổi "▶ Đọc toàn bài / ▶ Đọc từ vựng" trong khung bài học fz, ky, ld: phát lần lượt các nút ▶ đang hiện
(câu bài khoá = button.aud.s, từ vựng = button.aud không .s), có Dừng, tự cuộn tới câu đang đọc.
Dùng: python3 tools/add_audio_all.py <html>   (chạy cuối build_v4.sh)"""
import re, sys, json
CSS = (".aall{position:fixed;right:12px;bottom:12px;z-index:50;display:flex;gap:6px;padding:6px;border-radius:99px;background:var(--card,#fff);border:1px solid var(--bd,#0003);box-shadow:0 2px 10px #0003;font-size:13px}"
       ".aall button{border:0;border-radius:99px;padding:.45em .9em;background:var(--acc,#17685c);color:#fff;cursor:pointer;font:inherit}.aall button.on{background:#b3402a}"
       ".aud.cur{outline:2px solid #e0a800;background:#fff3c4!important}@media print{.aall{display:none}}")
JS = r"""(function(){if(window.__aall)return;window.__aall=1;
var bar=document.createElement('div');bar.className='aall';
var bT=document.createElement('button'),bW=document.createElement('button');bT.type=bW.type='button';bT.textContent='▶ Đọc toàn bài';bW.textContent='▶ Đọc từ vựng';bar.appendChild(bT);bar.appendChild(bW);
var run=0,act=null,lab=null;
function vis(b){return !!(b.offsetParent||b.getClientRects().length)}
function list(sent){return [].filter.call(document.querySelectorAll(sent?'button.aud.s':'button.aud:not(.s)'),vis)}
function reset(){if(act){act.classList.remove('on');act.textContent=lab;act=null}document.querySelectorAll('.aud.cur').forEach(function(x){x.classList.remove('cur')})}
function halt(){run++;var c=document.querySelector('.aud.on');if(c)c.click();reset()}
function start(btn,sent,txt){if(act===btn){halt();return}halt();var q=list(sent);if(!q.length){btn.textContent='Chưa có audio';setTimeout(function(){btn.textContent=txt},1500);return}
 var my=++run;act=btn;lab=txt;btn.classList.add('on');btn.textContent='⏹ Dừng';var i=0;
 (function next(){if(my!==run)return;if(i>=q.length){reset();return}var b=q[i++];document.querySelectorAll('.aud.cur').forEach(function(x){x.classList.remove('cur')});b.classList.add('cur');
  try{b.scrollIntoView({block:'center',behavior:'smooth'})}catch(e){}
  b.click();var t0=Date.now(),on=false;
  var iv=setInterval(function(){if(my!==run){clearInterval(iv);return}var p=b.classList.contains('on');if(p)on=true;
   if((on&&!p)||(!on&&Date.now()-t0>6000)){clearInterval(iv);setTimeout(next,on?250:0)}},150)})()}
bT.onclick=function(){start(bT,true,'▶ Đọc toàn bài')};bW.onclick=function(){start(bW,false,'▶ Đọc từ vựng')};
function sync(){var s=list(true).length,w=list(false).length;bT.style.display=s?'':'none';bW.style.display=w?'':'none';bar.style.display=(s||w)?'':'none'}
document.body.appendChild(bar);var t=null;function sch(){clearTimeout(t);t=setTimeout(sync,300)}
new MutationObserver(sch).observe(document.body,{childList:true,subtree:true,attributes:true,attributeFilter:['class','style','open']});addEventListener('load',sync);sync()})();"""
def main(path):
    h = open(path, encoding='utf-8').read(); done = []
    for b in ('fz', 'ky', 'ld'):
        m = re.search(r'(<script type="application/json" id="src-%s">)(.*?)(</script>)' % b, h, re.S); d = json.loads(m.group(2))
        if '__aall' not in d:
            d = d.replace('</style>', CSS + '</style>', 1)
            i = d.rfind('</body>'); d = d[:i] + '<script>' + JS + '</script>' + d[i:]; done.append(b)
        h = h[:m.start(2)] + json.dumps(d, ensure_ascii=False).replace('<', '\\u003c') + h[m.end(2):]
    open(path, 'w', encoding='utf-8').write(h); print('add_audio_all:', done)
if __name__ == '__main__': main(sys.argv[1])
