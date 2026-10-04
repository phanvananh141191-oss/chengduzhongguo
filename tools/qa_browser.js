// S12 layout-snapshot + S6 (ruby chạy lúc chạy) + kiểm tràn ngang. Cần: python3 -m http.server 8765
const {chromium}=require('playwright');const fs=require('fs');
const U='http://localhost:8765/Tong_hop_3_giao_trinh_D1_D2_KY_v4.html';
const pages=['fz:l05','fz:l08','ky:l04','ky:l08','ld:l01','kb:l04'];
const views=[['desktop',1280,800],['mobile',390,844]];const themes=['light','dark'];
(async()=>{
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',args:['--no-sandbox']});
const rows=[];const errs=[];
for(const [vn,w,h] of views)for(const th of themes){
  const ctx=await b.newContext({viewport:{width:w,height:h},deviceScaleFactor:1,isMobile:vn==='mobile'});
  const p=await ctx.newPage();p.on('pageerror',e=>errs.push(vn+th+': '+e.message));
  await p.goto(U);await p.evaluate(t=>{localStorage.clear();localStorage.setItem('u3-set',JSON.stringify({theme:t,py:true,scale:1}))},th);
  for(const k of pages){
    await p.goto(U+'#'+k);await p.reload();await p.waitForTimeout(3500);
    const name=`${k.replace(':','_')}_${vn}_${th}.png`;
    await p.screenshot({path:'reports/anh/qa/'+name});
    const shell=await p.evaluate(()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,theme:document.documentElement.getAttribute('data-u-theme')}));
    let fr=null;for(const f of p.frames()){if(f===p.mainFrame())continue;
      const r=await f.evaluate(()=>({vis:document.body&&document.body.offsetWidth>0&&innerHeight>0,sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,ruby:document.querySelectorAll('ruby').length,rt0:[...document.querySelectorAll('ruby')].filter(r=>{const t=r.querySelector('rt');return !t||!t.textContent.trim()}).length,theme:document.documentElement.getAttribute('data-u-theme')})).catch(()=>null);
      const on=await f.frameElement().then(e=>e.evaluate(x=>x.classList.contains('on'))).catch(()=>false);
      if(r&&on)fr=r}
    rows.push({k,vn,th,shell,fr,name})}
  await ctx.close()}
await b.close();
fs.writeFileSync('/tmp/qa_browser.json',JSON.stringify({rows,errs},null,1));
let md='\n## S12 · layout-snapshot và S6 (ruby lúc chạy)\n\nẢnh: `reports/anh/qa/` (6 trang × desktop/mobile × sáng/tối = %n ảnh).\n\n| trang | khung | giao diện | tràn ngang shell | tràn ngang khung | ruby | `<rt>` rỗng | theme shell/khung |\n|---|---|---|---|---|---|---|---|\n'.replace('%n',rows.length);
for(const r of rows){const so=r.shell.sw>r.shell.cw+1,fo=r.fr&&r.fr.sw>r.fr.cw+1;
 md+=`| ${r.k} | ${r.vn} | ${r.th} | ${so?'**CÓ**':'không'} | ${r.fr?(fo?'**CÓ** '+r.fr.sw+'>'+r.fr.cw:'không'):'?'} | ${r.fr?r.fr.ruby:'?'} | ${r.fr?r.fr.rt0:'?'} | ${r.shell.theme}/${r.fr?r.fr.theme:'?'} |\n`}
md+='\nLỗi JS trang: '+(errs.length?errs.join('; '):'không')+'\n';
fs.writeFileSync('/tmp/qa_s12.md',md);console.log(md);
})();
