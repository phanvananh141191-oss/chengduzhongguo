function vtBuild(tb,opt){
  opt=opt||{};
  var ths=tb.querySelectorAll('th');if(!ths.length)return false;
  var keys=[];for(var i=0;i<ths.length;i++)keys.push(vtKey(ths[i].textContent));
  if(keys.indexOf('w')<0||keys.indexOf('m')<0)return false;
  var rows=[].slice.call(tb.querySelectorAll('tr')).filter(function(r){return r.querySelector('td')});
  var data=[],odd=[],badge=[].slice.call(tb.querySelectorAll('th .nb')).map(function(n){return n.cloneNode(true)});
  rows.forEach(function(r){var cells=[].slice.call(r.cells);
    if(cells.length!==keys.length){odd.push(r);return}
    var o={cls:{}};cells.forEach(function(td,i){var k=keys[i];if(!k)return;o[k]={nodes:vtMove(td),td:td};o.cls[k]=td.className});data.push(o)});
  if(keys.indexOf('t')<0&&keys.indexOf('x')>=0){data.forEach(function(o){var x=o.x;if(!x)return;var n=x.nodes;
      if(n.length&&n[0].nodeType===1&&n[0].tagName==='I'){o.t={nodes:[document.createTextNode(n[0].textContent)]};n=n.slice(1);
        if(n.length&&n[0].nodeType===3){n[0].nodeValue=n[0].nodeValue.replace(/^\s*[·•]\s*/,'');if(!n[0].nodeValue)n=n.slice(1)}x.nodes=n}})}
  if(opt.posFrom){data.forEach(function(o){if(o.t)return;var w=vtWord(o.w.td),ps=w.split('/'),p=null;
      for(var i=0;i<ps.length&&!p;i++){var e=opt.posFrom[ps[i]];if(e)p=e}if(p)o.t={nodes:[document.createTextNode(p)]}})}
  function em(d){return !d||vtEmpty({textContent:d.nodes.map(function(x){return x.textContent}).join('')})}
  var XK=opt.xAs||'x';
  var anyX=XK==='x'&&data.some(function(o){return !em(o.x)});
  function det(o){
    var it=[];
    if(!em(o.t))it.push(['Loại từ',o.t.nodes,'']);
    if(!em(o.hv))it.push(['Hán Việt',o.hv.nodes,'hv']);
    if(XK==='note'&&!em(o.x))it.push(['Ghi chú',o.x.nodes,'']);
    if(!em(o.e))it.push(['English',o.e.nodes,'k-e']);
    if(!it.length)return null;
    var d=document.createElement('details');d.className='ul-det';var sm=document.createElement('summary');sm.textContent='Chi tiết';d.appendChild(sm);
    var dl=document.createElement('dl');
    it.forEach(function(x){var dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=x[0];if(x[2]==='k-e')dt.className='k-e';dd.className=x[2];x[1].forEach(function(n){dd.appendChild(n)});dl.appendChild(dt);dl.appendChild(dd)});
    d.appendChild(dl);return d}
  var dets=data.map(det),anyD=dets.some(function(d){return !!d});
  var cols=['n','w','m'];if(anyX)cols.push('x');if(anyD)cols.push('d');
  var H={n:'#',w:'Từ vựng',m:'Nghĩa tiếng Việt',x:'Ví dụ',d:'Chi tiết'};
  var nt=document.createElement('table');nt.className='ul-vt';nt.setAttribute('data-vtb','1');
  nt.innerHTML='<thead><tr>'+cols.map(function(k){return '<th class="c-'+k+'">'+H[k]+'</th>'}).join('')+'</tr></thead>';
  if(badge.length){var mh=nt.querySelector('th.c-m');badge.forEach(function(b){mh.appendChild(document.createTextNode(' '));mh.appendChild(b)})}
  var bd=document.createElement('tbody');nt.appendChild(bd);
  data.forEach(function(o,ri){var tr=document.createElement('tr');
    cols.forEach(function(k){var td=document.createElement('td');td.className='c-'+k+(k==='m'&&opt.semantic?' mv':'')+(k==='w'&&o.cls.w&&/\bw\b/.test(o.cls.w)?' w':'');
      if(k==='n')td.textContent=o.n?o.n.td.textContent.trim():String(ri+1);
      else if(k==='w'){o.w.nodes.forEach(function(x){td.appendChild(x)});
        if(o.p&&!em(o.p)){var sp=document.createElement('span');sp.className='ul-pyraw';sp.setAttribute('aria-hidden','true');o.p.nodes.forEach(function(x){sp.appendChild(x)});td.appendChild(sp)}}
      else if(k==='m'){if(!em(o.m))o.m.nodes.forEach(function(x){td.appendChild(x)})}
      else if(k==='x'){if(!em(o.x))o.x.nodes.forEach(function(x){td.appendChild(x)})}
      else if(k==='d'){if(dets[ri])td.appendChild(dets[ri])}
      tr.appendChild(td)});
    bd.appendChild(tr)});
  odd.forEach(function(r){var tr=document.createElement('tr'),td=document.createElement('td');td.colSpan=cols.length;td.className='c-x';[].slice.call(r.cells).forEach(function(c){vtMove(c).forEach(function(x){td.appendChild(x);td.appendChild(document.createTextNode(' '))})});tr.appendChild(td);bd.appendChild(tr)});
  var host=tb.parentNode;
  if(host&&host.tagName==='DIV'&&/\b(w|tw)\b/.test(host.className)){host.classList.add('vtw');host.replaceChild(nt,tb);return nt}
  var wrap=document.createElement('div');wrap.className='vtw';tb.parentNode.insertBefore(wrap,tb);wrap.appendChild(nt);tb.remove();return nt}
