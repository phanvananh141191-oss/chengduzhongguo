#!/usr/bin/env python3
# Dựng lại Tong_hop_3_giao_trinh_D1_D2_KY.html từ bản sao lưu + lớp giao diện chung (ULAY)
import re,json,sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
SRC='/home/user/chengduzhongguo/backup/Tong_hop_3_giao_trinh_D1_D2_KY.truoc-khi-dong-nhat.html'
OUT=sys.argv[1] if len(sys.argv)>1 else '/home/user/chengduzhongguo/Tong_hop_3_giao_trinh_D1_D2_KY.html'
def rd(n): return open(os.path.join(HERE,n),encoding='utf-8').read()
def must_replace(s,old,new,count=1,label=''):
    if old not in s: raise SystemExit('KHÔNG TÌM THẤY mẫu thay thế: '+(label or old[:60]))
    return s.replace(old,new,count)

t=open(SRC,encoding='utf-8').read()
toc=json.loads(re.search(r'id="toc-data">(.*?)</script>',t,re.S).group(1))
NAMES=toc['books']
LES={'fz':{},'ky':{},'ld':{}}
for p in toc['parts']:
    for g in p['groups']:
        for it in g['items']:
            k=it['key']; b=k.split(':')[0]
            if b=='fz': LES['fz'][k.split(':')[1]]={'zh':it['zh'],'vi':it.get('vi','')}
            elif b=='ky' and re.match(r'ky:s\d+$',k): LES['ky'][k.split(':')[1]]={'zh':it['zh'],'vi':it.get('vi','')}
            elif b=='ld' and k.startswith('ld:l:'): LES['ld'][k.split(':')[2]]={'zh':it['zh'],'vi':it.get('vi','')}

def patch_bridge(s,book):
    # --- UPY: gom từ nhiều chữ vào một cụm không ngắt dòng ---
    s=must_replace(s,"var NQ=[],busy=false","var LS=[];\nvar NQ=[],busy=false",label='UPY LS') if False else s
    s=must_replace(s,"function seg(r){","var LS=[];\nfunction seg(r){",label='seg')
    s=must_replace(s,"  return syl;\n}\nfunction esc(s)","  LS=segs;return syl;\n}\nfunction esc(s)",label='seg return')
    old_html=s[s.index("function html(t){"):s.index("function annot(tn)")]
    new_html="""function html(t){var out='',last=0,m;HRUN.lastIndex=0;
  while((m=HRUN.exec(t))){out+=esc(t.slice(last,m.index));var r=m[0],syl=seg(r),sg=LS,q,j,a,b,w;
    for(q=0;q<sg.length;q++){a=sg[q][0];b=sg[q][1];w='';
      for(j=a;j<b;j++)w+=syl[j]?'<ruby class="u-r">'+r[j]+'<rt data-p="'+syl[j]+'"></rt></ruby>':r[j];
      out+=(b-a>1)?'<span class="u-w">'+w+'</span>':w}
    last=m.index+r.length}
  return out+esc(t.slice(last))}
"""
    s=s.replace(old_html,new_html)
    # --- bảng từ vựng chuẩn ---
    a=s.index("function vtKey(h){"); b=s.index("function vtWord(td)")
    s=s[:a]+rd('vt_key.js')+s[b:]
    a=s.index("function vtBuild(tb,opt){"); b=s.index("var vtObs=false;")
    s=s[:a]+rd('vt_build.js')+s[b:]
    s=must_replace(s,"if(BOOK==='fz'){document.querySelectorAll('section.les table:not([data-vtb])').forEach(function(tb){vtBuild(tb,{})});return}",
      "if(BOOK==='fz'){document.querySelectorAll('section.les table:not([data-vtb])').forEach(function(tb){vtBuild(tb,{xAs:'x'})});return}\n  if(BOOK==='ky'){document.querySelectorAll('section table.vt:not([data-vtb])').forEach(function(tb){vtBuild(tb,{xAs:'x'})});return}",label='normVocab')
    s=must_replace(s,"vtBuild(tb,{semantic:true,posFrom:pos})","vtBuild(tb,{semantic:true,posFrom:pos,xAs:'note'})",label='ld vt')
    # --- cài đặt: Xem toàn bài, Hiện dịch, font ---
    s=must_replace(s,"  applyOpt(s.opt||{});\n}","  de.classList.toggle('ul-all',!!s.all);de.classList.toggle('ul-notr',s.tr===false);de.classList.toggle('ul-serif',!!(s.opt&&s.opt.ff==='serif'));\n  var o=Object.assign({},s.opt||{});if(s.tr!==undefined){o.tv=!!s.tr;o.dv=!!s.tr}\n  applyOpt(o);\n}",label='apply')
    # --- caps ---
    s=must_replace(s,"return {nt:!!a.querySelector('.vn'),lc:!!a.querySelector('.tn'),tv:!!a.querySelector('.tr'),dv:!!a.querySelector('.ln.lv:not(td .ln)'),en:!!a.querySelector('.vtb .c-e')}}",
      "return {nt:!!a.querySelector('.vn'),lc:!!a.querySelector('.tn'),en:!!a.querySelector('.ul-vt .k-e'),tr:!!a.querySelector('.tr,.ln.lv'),all:!!a.querySelector('.ul-lesson'),ff:1}}",label='caps fz')
    s=must_replace(s,"if(BOOK==='ld'){var r=active();return {hp:1,hh:vis('.hv',r),hm:vis('.mv',r),ff:1}}\n  return {};",
      "if(BOOK==='ld'){var r=active();return {hp:1,hh:vis('.hv',r),hm:vis('.mv',r),ff:1,tr:!!(r&&r.querySelector('.svi')),all:!!(r&&r.querySelector('.ul-lesson'))}}\n  var k=active();return {ff:1,tr:false,all:!!(k&&k.querySelector('.ul-lesson'))};",label='caps ld/ky')
    # --- tìm kiếm: mở đúng tab, bỏ tiêu đề tab khỏi chỉ mục ---
    s=must_replace(s,"setTimeout(function(){r[2].scrollIntoView({block:'center'});","setTimeout(function(){if(window.ULAY)ULAY.reveal(r[2]);r[2].scrollIntoView({block:'center'});",label='reveal')
    s=must_replace(s,"function(e){if(e.querySelector('p,li,.ln,.note,td'))return;","function(e){if(e.classList.contains('ul-ph')||e.querySelector('p,li,.ln,.note,td'))return;",label='index')
    # --- sau khi nhận init: gắn nhãn chữ Hán + ẩn pinyin trùng ---
    s=must_replace(s,"UPY.start(m.dict,document.body,active());if(m.go)go(m.go)}","UPY.start(m.dict,document.body,active());if(window.ULAY){ULAY.tagZh(document.body);ULAY.pyDup(document.body)}if(m.go)go(m.go)}",label='init')
    return s

def patch_uex(s):
    s=must_replace(s,"cards.push(Card(c,'u3x:'+book+':'+sec.id+':e'+(i++),upd))","cards.push(Card(c,'u3x:'+book+':'+sec.id+':e'+(c.hasAttribute('data-ux-i')?c.getAttribute('data-ux-i'):i++),upd))",label='uex key')
    s=must_replace(s,"var anc=o.after&&sec.querySelector(o.after);\n    if(anc)anc.parentNode.insertBefore(box,anc.nextSibling);\n    else if(first)",
      "var anc=o.after&&sec.querySelector(o.after),into=sec.querySelector('.ul-pane[data-pane=\"pr\"]>.ul-pb');\n    if(into)into.insertBefore(box,into.firstChild);\n    else if(anc)anc.parentNode.insertBefore(box,anc.nextSibling);\n    else if(first)",label='uex into')
    s=must_replace(s,"setTimeout(function(){fin(null)},600)","setTimeout(function(){fin(null)},3000)",label='uex timeout')
    # tiến độ: tách rõ Đã làm / Làm đúng
    s=must_replace(s,"""      if(T)parts.push('Ô đúng '+O+'/'+T);
      if(n)parts.push('Mục đã làm '+d+'/'+n);
      var w=W.filter(function(x){var t=x.querySelector('textarea');return t&&t.value.trim()}).length;
      if(W.length)parts.push('Bài viết '+w+'/'+W.length);
      txt.textContent='Tiến độ: '+parts.join(' · ');""","""      if(n)parts.push(['Đã làm',d+'/'+n+' mục']);
      if(T)parts.push(['Làm đúng',O+'/'+T+' ô']);
      var w=W.filter(function(x){var t=x.querySelector('textarea');return t&&t.value.trim()}).length;
      if(W.length)parts.push(['Bài viết',w+'/'+W.length]);
      txt.textContent='';parts.forEach(function(p){var m=el('span','ul-m'),b=el('b',null,p[0]),v=el('span',null,p[1]);m.appendChild(b);m.appendChild(v);txt.appendChild(m)});""",label='uex upd')
    s=must_replace(s,"bAll=btn('Làm lại cả bài');","bAll=btn('Làm lại cả bài');bAll.title='Xóa bài làm của tất cả mục trong bài này (bài viết giữ nguyên)';",label='uex all')
    s=must_replace(s,"bR=btn('Làm lại');","bR=btn('Làm lại');bR.title='Xóa bài làm của mục này';",label='uex reset')
    # đánh dấu đã luyện cho dạng không có đáp án
    s=must_replace(s,"if(type==='discuss'){bD=btn('✓ Đã làm');","if(type==='discuss'||type==='tick'){bD=btn('Đánh dấu đã luyện');bD.setAttribute('aria-pressed','false');",label='uex mark')
    s=must_replace(s,"function lab(){if(bS)bS.textContent=revealed?'Ẩn đáp án':'Xem đáp án';if(bD)bD.classList.toggle('act',!!st.d)}","function lab(){if(bS)bS.textContent=revealed?'Ẩn đáp án':'Xem đáp án';if(bD){bD.classList.toggle('act',!!st.d);bD.setAttribute('aria-pressed',st.d?'true':'false')}}",label='uex lab')
    s=must_replace(s,"var done=type==='fill'?!!st.c:type==='tick'?stat().done:!!st.d;","var done=type==='fill'?!!st.c:type==='tick'?(stat().done||!!st.d):!!st.d;",label='uex done')
    return s

def embed(book,src):
    css='<style id="ul-css">\n'+rd('ul.css')+'\n'+(rd('ul_%s.css'%book) if os.path.exists(os.path.join(HERE,'ul_%s.css'%book)) else '')+'</style>'
    cfg={'book':book,'name':NAMES[book],'lessons':LES[book]}
    js='<script id="ul-core">window.ULCFG='+json.dumps(cfg,ensure_ascii=False)+';\n'+rd('ul_core.js')+'</script>\n'+('' if book=='ld' else '<script id="ul-adapter">'+rd('ul_%s.js'%book)+'</script>\n')
    src=must_replace(src,'</head>',css+'</head>',label=book+' head')
    # chèn cuối body (sau các script sẵn có)
    i=src.rindex('</body>')
    return src[:i]+js+src[i:]

def process(book,src):
    # patch bridge (script chứa UPY) và UEX
    def fix(m):
        body=m.group(2)
        if 'var UPY=(function(){' in body: body=patch_bridge(body,book)
        if 'var UEX=(function(){' in body: body=patch_uex(body)
        if 'const LES=' in body and 'function tab(t)' in body: body=body+rd('ul_ld.js')
        return m.group(1)+body+m.group(3)
    src=re.sub(r'(<script[^>]*>)(.*?)(</script>)',fix,src,flags=re.S)
    return embed(book,src)

out=t
for book in ['fz','ky','ld']:
    m=re.search(r'(<script type="application/json" id="src-%s">)(.*?)(</script>)'%book,out,re.S)
    s=json.loads(m.group(2))
    s=process(book,s)
    enc=json.dumps(s,ensure_ascii=False).replace('<','\\u003c')
    out=out[:m.start(2)]+enc+out[m.end(2):]
# vỏ
sh=os.path.join(HERE,'shell_patch.py')
if os.path.exists(sh):
    ns={'out':out,'must_replace':must_replace,'rd':rd}
    exec(open(sh,encoding='utf-8').read(),ns); out=ns['out']
open(OUT,'w',encoding='utf-8').write(out)
print('ghi',OUT,len(out))
