/* ===== ULAY · Khuôn bài học chung (đầu bài · 5 tab · Xem toàn bài) ===== */
var ULAY=(function(){
var CFG=window.ULCFG||{book:'',name:'',lessons:{}};
var PANES=[['ov','Tổng quan'],['vo','Từ vựng'],['tx','Bài khóa / Hội thoại'],['gr','Ngữ pháp / Mẫu câu'],['pr','Luyện tập'],['ex','Bổ sung']];
var HRX=/[㐀-鿿]/;
var uid=0,SCROLLER=null;
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!==undefined)e.textContent=x;return e}
function arr(l){return Array.prototype.slice.call(l)}
function txtNoRt(n){var s='',w=document.createTreeWalker(n,NodeFilter.SHOW_TEXT,{acceptNode:function(t){return t.parentElement&&t.parentElement.closest('rt,script,style,[hidden],.ul-pydup')?2:1}});while(w.nextNode())s+=w.currentNode.nodeValue;return s}

/* ----- gắn nhãn khối chủ yếu là chữ Hán (để cỡ chữ 22–24px, dòng thoáng cho pinyin) ----- */
var BLK={DIV:1,P:1,UL:1,OL:1,LI:1,TABLE:1,H1:1,H2:1,H3:1,H4:1,SECTION:1,BLOCKQUOTE:1,DL:1,TBODY:1,TR:1,THEAD:1,DETAILS:1,ARTICLE:1,HEADER:1,MAIN:1,NAV:1,ASIDE:1,FOOTER:1,FIGURE:1,FORM:1,PRE:1,HR:1,BUTTON:1};
function leafBlock(e){for(var c=e.firstElementChild;c;c=c.nextElementSibling){if(BLK[c.tagName])return false}return true}
function tagZh(root){
  if(!root)return;
  var list=root.querySelectorAll('p,li,td,.ln,div,dd,span.han');
  for(var i=0;i<list.length;i++){var e=list[i];
    if(e.classList.contains('ul-zh')||e.classList.contains('ul-vi-line'))continue;
    if(!leafBlock(e))continue;
    if(e.closest('h1,h2,h3,h4,th,summary,button,.ul-tabs,.ul-head,#optp')||!e.closest('.ul-pb,.ul-plain'))continue;
    var raw=txtNoRt(e);if(/[\u2500-\u257f]/.test(raw)){e.classList.add('ul-diagram');continue}
    var s=raw.replace(/\s+/g,'');if(s.length<2)continue;
    var z=0,l=0;for(var k=0;k<s.length;k++){var ch=s.charCodeAt(k);if(ch>=0x3400&&ch<=0x9fff)z++;else if((ch>=65&&ch<=90)||(ch>=97&&ch<=122)||ch>=0xc0&&ch<=0x1ef9&&!(ch>=0x2000&&ch<=0x2fff))l++}
    if(z>=2&&z>=l){e.classList.add('ul-zh')}}
}
/* pinyin chép tay trùng với ruby (ghi chú .n chỉ gồm pinyin) -> ẩn hiển thị, giữ dữ liệu */
var PYX=/^[a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜüA-Z\s·'’\-]+$/;var TONE=/[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]/;
var SYL=/^(?:(?:zh|ch|sh|[bpmfdtnlgkhjqxrzcsyw])?[aeiouüvāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]+(?:ng|n|r)?['’]?)+$/i;
function pyLine(t){t=t.replace(/[“”"()（）,.;:?!，。；：？！…\/·\-—\d]/g,' ').trim();if(!t)return false;var w=t.split(/\s+/);if(w.length<3)return false;
  for(var i=0;i<w.length;i++){if(!SYL.test(w[i]))return false}return true}
/* pinyin chép tay trùng với ruby (ghi chú .n / dòng nghiêng chỉ gồm pinyin) -> ẩn hiển thị, giữ dữ liệu */
function pyDup(root){root=root||document;
  arr(root.querySelectorAll('.n')).forEach(function(n){var t=n.textContent.trim();if(t&&TONE.test(t)&&PYX.test(t))n.classList.add('ul-pydup')});
  arr(root.querySelectorAll('i,em,small')).forEach(function(n){if(n.querySelector('*'))return;var t=n.textContent.trim();
    if(t.length>8&&TONE.test(t)&&pyLine(t)&&n.closest('.ul-pb')&&!n.closest('.ul-pyraw'))n.classList.add('ul-pydup')})}

/* ----- dựng khuôn bài ----- */
function addNodes(host,items){
  var n=0;
  (items||[]).forEach(function(it){
    if(it==null)return;
    if(typeof it==='string'){var t=document.createElement('template');t.innerHTML=it;if(t.content.childNodes.length){host.appendChild(t.content);n++}}
    else{host.appendChild(it);if(!(it.nodeType===3&&!it.nodeValue.trim()))n++}
  });
  return n;
}
function hasContent(pb){for(var c=pb.firstChild;c;c=c.nextSibling){if(c.nodeType===1&&!c.classList.contains('ul-dup'))return true;if(c.nodeType===3&&c.nodeValue.trim())return true}return false}
/* cfg: {id,key,num,zhEl|zhText,vi,buckets:{ov,vo,tx,gr,pr,ex:[node|html]}, head:[extra header nodes], pane, scroller} */
function mount(host,cfg){
  uid++;var L=el('div','ul-lesson');L.setAttribute('data-ul-lesson',cfg.key||'');L.setAttribute('data-ul-book',CFG.book);
  var H=el('header','ul-head');
  if(cfg.crumb)H.appendChild(cfg.crumb);
  var kk=el('p','ul-kick',(CFG.name||'')+(cfg.num?' · Bài '+cfg.num:''));kk.setAttribute('data-nopy','');H.appendChild(kk);
  if(cfg.zhEl){wrapNo(cfg.zhEl);H.appendChild(cfg.zhEl)}
  else{var h=el('h1','ul-title');h.textContent=cfg.zhText||'';H.appendChild(h)}
  if(cfg.vi)H.appendChild(el('p','ul-vi',cfg.vi));
  L.appendChild(H);
  var T=el('div','ul-tabs');T.setAttribute('role','tablist');T.setAttribute('aria-label','Các phần của bài');
  var P=el('div','ul-panes');
  var first=null;
  PANES.forEach(function(p,i){
    var id='ul-'+uid+'-'+p[0];
    var items=(cfg.buckets||{})[p[0]]||[];
    if(p[0]==='ex'&&!items.length)return;
    var sec=el('div','ul-pane');sec.id=id+'-p';sec.setAttribute('role','tabpanel');sec.setAttribute('data-pane',p[0]);sec.setAttribute('aria-labelledby',id+'-t');
    var ph=el('h2','ul-ph',p[1]);sec.appendChild(ph);
    var pb=el('div','ul-pb');sec.appendChild(pb);
    addNodes(pb,items);
    var empty=!hasContent(pb);if(empty)sec.classList.add('ul-empty');
    P.appendChild(sec);
    var b=el('button','',p[1]);b.type='button';b.id=id+'-t';b.setAttribute('role','tab');b.setAttribute('data-pane',p[0]);b.setAttribute('aria-controls',id+'-p');b.setAttribute('aria-selected','false');b.tabIndex=-1;
    if(empty)b.classList.add('ul-t-empty');
    T.appendChild(b);
  });
  L.appendChild(T);L.appendChild(P);
  if(cfg.append)cfg.append.forEach(function(n){L.appendChild(n)});
  host.appendChild(L);
  T.addEventListener('click',function(e){var b=e.target.closest('button[data-pane]');if(b)activate(L,b.getAttribute('data-pane'),true)});
  T.addEventListener('keydown',function(e){
    var bs=arr(T.querySelectorAll('button')),i=bs.indexOf(document.activeElement);if(i<0)return;
    var n=-1;if(e.key==='ArrowRight')n=(i+1)%bs.length;else if(e.key==='ArrowLeft')n=(i-1+bs.length)%bs.length;else if(e.key==='Home')n=0;else if(e.key==='End')n=bs.length-1;
    if(n>=0){e.preventDefault();bs[n].focus();activate(L,bs[n].getAttribute('data-pane'),true)}});
  tagZh(L);pyDup(L);
  activate(L,cfg.pane||'ov',false);
  return L;
}
function activate(L,pane,scroll){
  var any=false;
  arr(L.querySelectorAll(':scope>.ul-panes>.ul-pane')).forEach(function(s){var on=s.getAttribute('data-pane')===pane;if(on)any=true;s.classList.toggle('on',on)});
  if(!any){pane='ov';var f=L.querySelector(':scope>.ul-panes>.ul-pane');if(f){f.classList.add('on');pane=f.getAttribute('data-pane')}}
  arr(L.querySelectorAll(':scope>.ul-tabs>button')).forEach(function(b){var on=b.getAttribute('data-pane')===pane;b.setAttribute('aria-selected',on?'true':'false');b.tabIndex=on?0:-1;if(on&&scroll!==undefined){try{b.scrollIntoView({block:'nearest',inline:'nearest'})}catch(e){}}});
  L.setAttribute('data-pane',pane);
  var sec=L.querySelector(':scope>.ul-panes>.ul-pane.on');
  if(window.UPY&&sec)UPY.enqueue(sec,true);
  if(scroll){var tabs=L.querySelector('.ul-tabs'),sc=scroller(L);
    if(sc===window){var top=tabs.getBoundingClientRect().top+window.pageYOffset;if(window.pageYOffset>top)window.scrollTo(0,top)}
    else{var tb=tabs.getBoundingClientRect().top-sc.getBoundingClientRect().top+sc.scrollTop;if(sc.scrollTop>tb)sc.scrollTop=tb}}
  document.dispatchEvent(new CustomEvent('ul-pane',{detail:{lesson:L,pane:pane}}));
}
function scroller(L){var e=L.closest('#lm');return e||window}
function paneOf(node){var p=node&&node.closest?node.closest('.ul-pane'):null;return p}
/* mở đúng tab chứa phần tử (dùng cho tìm kiếm / nhảy tới) */
function reveal(node){var p=paneOf(node);if(!p)return;var L=p.closest('.ul-lesson');if(L&&!p.classList.contains('on'))activate(L,p.getAttribute('data-pane'),false)}
/* ẩn tiền tố "第N课" ở h1 (số bài đã có ở dòng đầu bài) nhưng giữ nguyên trong DOM */
function wrapNo(h1){
  if(!h1||h1.querySelector('.ul-no'))return;
  var acc='',nodes=arr(h1.childNodes),grp=[];
  for(var i=0;i<nodes.length;i++){var n=nodes[i];
    if(n.nodeType===3){var v=n.nodeValue,m=(acc+v).match(/^第\d+课[\s\u3000]*/);
      if(m){var cut=m[0].length-acc.length;if(cut<v.length){var rest=n.splitText(cut);grp.push(n);break}grp.push(n);acc+=v;break}
      acc+=v;grp.push(n)}
    else{acc+=txtNoRt(n);grp.push(n);if(/^第\d+课[\s\u3000]*$/.test(acc))break}
    if(acc.length>12)return}
  if(!/^第\d+课/.test(acc))return;
  var sp=document.createElement('span');sp.className='ul-no';h1.insertBefore(sp,grp[0]);grp.forEach(function(g){sp.appendChild(g)})}
/* thẻ ngữ pháp kiểu <b>cấu trúc</b><br>giải thích<br>例：ví dụ -> nhãn Cấu trúc · Giải thích · Ví dụ · Lưu ý (chỉ gắn nhãn, không đổi chữ) */
function gram(root){
  arr(root.querySelectorAll('.card')).forEach(function(card){
    if(card.classList.contains('ul-gram')||card.parentNode&&card.parentNode.closest('.card'))return;
    var f=card.firstElementChild;if(!f||f.tagName!=='B'||card.firstChild!==f)return;
    var lines=[[]];arr(card.childNodes).forEach(function(n){
      if(n.nodeType===1&&n.tagName==='BR'){lines.push([]);return}
      if(n.nodeType===1&&/^(DIV|OL|UL|TABLE|BUTTON)$/.test(n.tagName)){lines.push([n]);lines.push([]);return}
      lines[lines.length-1].push(n)});
    lines=lines.filter(function(l){return l.length});
    if(lines.length<2)return;
    var seenEx=false,kinds=lines.map(function(l,i){
      if(l.length===1&&l[0].nodeType===1&&/^(DIV|OL|UL|TABLE|BUTTON)$/.test(l[0].tagName))return '';
      var t=l.map(function(x){return x.nodeType===3?x.nodeValue:txtNoRt(x)}).join('').trim();
      if(i===0)return 'ct';
      if(/^(试一试|练一练|Thử)/.test(t))return '';
      if(/^(注意|注：|注:|Lưu ý|Chú ý)/.test(t))return 'ln';
      if(/^(例|\(\d+\)|\d+[\.、])/.test(t)){seenEx=true;return 'vd'}
      return seenEx?'':'gt'});
    if(kinds.indexOf('gt')<0&&kinds.indexOf('vd')<0)return;
    var LAB={ct:'Cấu trúc',gt:'Giải thích',vd:'Ví dụ',ln:'Lưu ý'};
    card.classList.add('ul-gram');
    var anchor=null;
    lines.forEach(function(l,i){var k=kinds[i];if(!k)return;
      var d=document.createElement('div');d.className='ul-gf ul-gf-'+k;d.setAttribute('data-gl',LAB[k]);
      l[0].parentNode.insertBefore(d,l[0]);l.forEach(function(n){d.appendChild(n)})});
    /* BR còn lại giữa các dòng đã được thay bằng khối; bỏ BR thừa */
    arr(card.querySelectorAll(':scope>br')).forEach(function(b){b.remove()})
  })}
function lesson(){return document.querySelector('.ul-lesson')}
function currentLesson(root){var a=(root||document).querySelector('.ul-lesson');return a}
function lessonInfo(key){return (CFG.lessons||{})[key]||null}
return {mount:mount,wrapNo:wrapNo,gram:gram,activate:activate,reveal:reveal,tagZh:tagZh,pyDup:pyDup,PANES:PANES,cfg:CFG,lessonInfo:lessonInfo,el:el,arr:arr,txt:txtNoRt,paneOf:paneOf,currentLesson:currentLesson}
})();
