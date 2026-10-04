const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p=await b.newPage();p.on('pageerror',e=>console.log('ERR',e.message.slice(0,200)));
await p.goto('file:///tmp/fz3.html');await p.waitForTimeout(3000);
const r=await p.evaluate(()=>({l1:document.querySelector('#l1 .vt')?.innerHTML,l2:document.querySelector('#l2 .vt')?.innerHTML}));
fs.writeFileSync('/tmp/claude-0/vt.json',JSON.stringify(r));console.log(r.l1?.length,r.l2?.length);await b.close()})();
