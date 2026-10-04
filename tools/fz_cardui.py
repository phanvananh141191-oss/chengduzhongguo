"""Đợt 1 giao diện bài tập (theo đề xuất UI): khung thẻ chung cho fz — đầu thẻ (huy hiệu dạng bài + chấm trạng thái),
chân thẻ (nút Kiểm tra nổi bật), thanh tiến độ số chữ cho khung viết. Không đổi dữ liệu, không đổi khoá lưu.
Dùng: python3 tools/fz_cardui.py <html>"""
import re, sys, json

CSS = """
.card.ex.xc{padding:0;overflow:hidden;border-radius:12px}
.card.ex.xc>.xb{padding:12px 16px 14px}
.xh{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:10px 16px;border-bottom:1px solid var(--bd);background:var(--u-card,var(--card))}
.xh .xbd{font-size:.78rem;padding:2px 10px;border-radius:99px;background:var(--u-hl,#e8efe9);color:var(--acc,#17685c);font-weight:600;white-space:nowrap}
.xh .xst{font-size:.82rem;color:var(--mut,#777);display:inline-flex;align-items:center;gap:6px}
.xh .xst:before{content:"";width:8px;height:8px;border-radius:50%;background:var(--mut,#999)}
.xc[data-st=doing] .xst:before{background:#d98a00}.xc[data-st=checked] .xst:before{background:#1a8f4a}
.xc[data-st=checked]{border-color:#1a8f4a55}
.xc .uxb{display:flex;gap:8px;flex-wrap:wrap;align-items:center;justify-content:flex-end;margin:12px 0 0;padding-top:10px;border-top:1px solid var(--bd)}
.xc .uxb .b:first-child{background:var(--acc,#17685c);color:#fff;border-color:var(--acc,#17685c);font-weight:600}
.xc .uxb .sc{margin-right:auto;margin-left:0}
.xc .uin{margin:12px 0}
.wr .wbar{height:6px;border-radius:3px;background:var(--bd);overflow:hidden;margin:6px 0}.wr .wbar>i{display:block;height:100%;width:0;background:var(--acc,#17685c);transition:width .2s}.wr .wbar>i.full{background:#1a8f4a}
"""

JS = r"""
(function(){
var TYPES=[[/排序/,'排序'],[/连线/,'连线'],[/改写/,'改写'],[/完成对话|对话/,'完成对话'],[/完成句子/,'完成句子'],[/选词|选择合适|选择最合适|填空/,'选词填空'],[/写一写|写作/,'写一写'],[/课本剧|分享/,'表演·分享'],[/阅读|短文/,'阅读'],[/拓展/,'拓展'],[/回答|理解课文|问题/,'问答'],[/字词|新词语|注释|字源/,'字词'],[/想一想|思考/,'想一想']];
function sec(c){var r='',hs=c.closest('section')?c.closest('section').querySelectorAll('h2'):[];for(var i=0;i<hs.length;i++){if(hs[i].compareDocumentPosition(c)&4)r=hs[i].textContent}return r}
function typeOf(t){for(var i=0;i<TYPES.length;i++)if(TYPES[i][0].test(t))return TYPES[i][1];return '练习'}
function status(c){
  var v=false;c.querySelectorAll('input.uw,input[data-a],textarea').forEach(function(x){if((x.value||'').trim())v=true});
  if(c.querySelector('.ans:not([hidden])'))return 'checked';
  return v?'doing':'todo'}
var LAB={todo:'Chưa làm',doing:'Đang làm',checked:'Đã kiểm tra'};
function setSt(c,s){c.dataset.st=s;var e=c.querySelector('.xst');if(e)e.textContent=LAB[s]}
function run(){
 document.querySelectorAll('.card.ex').forEach(function(c){
  if(c.classList.contains('xc'))return;
  var h=c.querySelector('h3'),t=h?h.textContent:(c.previousElementSibling&&c.previousElementSibling.tagName==='H3'?c.previousElementSibling.textContent:'');
  if(!c.querySelector('.uxb')&&!c.querySelector('textarea'))return;
  var kids=[].slice.call(c.childNodes),b=document.createElement('div');b.className='xb';
  kids.forEach(function(k){b.appendChild(k)});
  var hd=document.createElement('div');hd.className='xh';
  hd.innerHTML='<span class="xbd"></span><span class="xst"></span>';hd.firstChild.textContent=/综合注释/.test(sec(c))?'语法·练习':(/走进课文/.test(sec(c))?'课文·问答':typeOf(t));
  c.appendChild(hd);c.appendChild(b);c.classList.add('xc');
  setSt(c,status(c));
  c.addEventListener('input',function(){if(c.dataset.st!=='checked')setSt(c,status(c))});
  c.addEventListener('click',function(e){var x=e.target.closest&&e.target.closest('.uxb .b');if(!x)return;var tx=x.textContent;
    setTimeout(function(){if(/Kiểm tra|Xem đáp án|Ẩn đáp án/.test(tx)){setSt(c,/Ẩn đáp án/.test(tx)?status(c):'checked')}else if(/Làm lại/.test(tx))setSt(c,'todo')},60)});
 });
 document.querySelectorAll('.wr').forEach(function(w){
  if(w.querySelector('.wbar'))return;var t=w.querySelector('textarea'),mn=+w.dataset.min||0;if(!t||!mn)return;
  var bar=document.createElement('div');bar.className='wbar';bar.innerHTML='<i></i>';t.parentNode.insertBefore(bar,t.nextSibling);
  function u(){var n=t.value.replace(/\s/g,'').length,i=bar.firstChild;i.style.width=Math.min(100,100*n/mn)+'%';i.className=n>=mn?'full':''}
  t.addEventListener('input',u);u()});
}
function go(){setTimeout(run,900);setTimeout(run,2500)}
if(document.readyState==='complete')go();else addEventListener('load',go);
})();
"""

def main(path):
    h = open(path, encoding='utf-8').read()
    m = re.search(r'(<script type="application/json" id="src-fz">)(.*?)(</script>)', h, re.S)
    d = json.loads(m.group(2))
    if '.card.ex.xc{' not in d:
        d = d.replace('</style>', CSS + '</style>', 1)
        i = d.rfind('</body>')
        d = d[:i] + '<script>' + JS + '</script>' + d[i:]
    h = h[:m.start(2)] + json.dumps(d, ensure_ascii=False).replace('<', '\\u003c') + h[m.end(2):]
    open(path, 'w', encoding='utf-8').write(h)
    print('fz_cardui: đã chèn')

if __name__ == '__main__':
    main(sys.argv[1])
