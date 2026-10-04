"""P8: đổi key mục lục sang quy ước mới {book}:{loại}{số}; giữ key cũ làm alias;
di chuyển khoá localStorage (u3xb:u3x:<sách>:<bài>:… và u3xb:ans:<sách>:<bài>:…).
Dùng: python3 tools/rekey.py <html>   (sửa tại chỗ)"""
import re, sys, json

def mapping():
    m = {}
    for i in range(1, 15):
        m['fz:l%d' % i] = 'fz:l%02d' % i
    m['fz:lg'] = 'fz:grammar-index'; m['fz:lv'] = 'fz:word-index'
    m['ky:s0'] = 'ky:intro'
    for i in range(1, 13):
        m['ky:s%d' % i] = 'ky:l%02d' % i
        m['ld:l:%d' % i] = 'ld:l%02d' % i
        m['kb:lessons/%02d.md' % i] = 'kb:l%02d' % i
    m['ky:s13'] = 'ky:word-index'
    m['ld:v:les'] = 'ld:hub'
    for a, b in [('mor','morpheme'),('for','formal'),('pat','pattern'),('chk','chunk'),
                 ('par','parsing'),('scn','scanning'),('map','skillmap'),('gap','gap')]:
        m['ld:v:' + a] = 'ld:bank-' + b
    return m

BRIDGE_OLD = r"""window.addEventListener('message',function(e){var d=e.data;if(!d||typeof d!=='object'||!d.u3x||!ok(e))return;"""
BRIDGE_NEW = r"""var NEWID=__NEWID__,OLDID={};for(var _o in NEWID)OLDID[NEWID[_o]]=_o;
function mapk(k,tbl){var p=k.split(':');if(p.length>=3&&(p[0]==='u3x'||p[0]==='ans')){var a=tbl[p[1]+':'+p[2]];if(a){var q=a.split(':');p[1]=q[0];p[2]=q.slice(1).join(':');return p.join(':')}}return k}
function toStore(k){return mapk(k,NEWID)}function toFrame(k){return mapk(k,OLDID)}
function migrate(){try{var del=[],add=[];for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);if(k.indexOf(P)!==0)continue;var f=k.slice(P.length),n=toStore(f);if(n!==f)add.push([k,P+n])}
add.forEach(function(x){if(localStorage.getItem(x[1])===null)localStorage.setItem(x[1],localStorage.getItem(x[0]));localStorage.removeItem(x[0])})}catch(x){}}
function migrate2(){try{var mv=[];for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);if(/^(u3x|ans):(fz|ky|ld|kb):/.test(k))mv.push(k)}
mv.forEach(function(k){var n=P+toStore(k);if(localStorage.getItem(n)===null)localStorage.setItem(n,localStorage.getItem(k));localStorage.removeItem(k)})}catch(x){}}
migrate();migrate2();
window.addEventListener('message',function(e){var d=e.data;if(!d||typeof d!=='object'||!d.u3x||!ok(e))return;"""

def main(path):
    h = open(path, encoding='utf-8').read()
    M = mapping()
    # 1) toc-data
    m = re.search(r'(<script type="application/json" id="toc-data">)(.*?)(</script>)', h, re.S)
    toc = json.loads(m.group(2))
    n = 0
    def walk(o):
        nonlocal n
        if isinstance(o, dict):
            k = o.get('key')
            if isinstance(k, str) and k in M and 'fk' not in o:
                o['fk'] = k.split(':', 1)[1]; o['key'] = M[k]; n += 1
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(toc)
    new = json.dumps(toc, ensure_ascii=False).replace('<', '\\u003c')
    h = h[:m.start(2)] + new + h[m.end(2):]
    # 2) shell JS
    a = "var BYKEY={};FLAT.forEach(function(it,i){it.i=i;BYKEY[it.key]=it});"
    assert a in h
    h = h.replace(a, a + "var ALIAS=" + json.dumps(M) + ";for(var _a in ALIAS)if(BYKEY[ALIAS[_a]])BYKEY[_a]=BYKEY[ALIAS[_a]];")
    b = "var book=it.book,tgt=key.slice(key.indexOf(':')+1);"
    assert b in h
    h = h.replace(b, "var book=it.book,tgt=it.fk||it.key.slice(it.key.indexOf(':')+1);")
    c = "tg=kk[0].slice(kk[0].indexOf(':')+1)+"
    assert c in h
    h = h.replace(c, "tg=(itn.fk||itn.key.slice(itn.key.indexOf(':')+1))+")
    # 3) cầu nối lưu trữ
    assert BRIDGE_OLD in h
    h = h.replace(BRIDGE_OLD, BRIDGE_NEW.replace('__NEWID__', json.dumps({k.split(':',1)[0]+':'+k.split(':',1)[1]: M[k] for k in M if k.startswith(('fz:l','ky:s','ld:l:'))} and {k: M[k] for k in M if k.startswith(('fz:','ky:'))}, separators=(',', ':'))))
    # load: trả khoá dạng cũ cho khung; set/del: đổi sang khoá mới
    h = h.replace("o[k.slice(P.length)]=localStorage.getItem(k)", "o[toFrame(k.slice(P.length))]=localStorage.getItem(k)")
    h = h.replace("localStorage.setItem(P+d.k,d.v)", "localStorage.setItem(P+toStore(d.k),d.v)")
    h = h.replace("localStorage.removeItem(P+d.k)", "localStorage.removeItem(P+toStore(d.k))")
    # 3b) mọi khung có UEX: khi nằm trong khung ngoài thì luôn lưu qua cầu nối (để khoá được đổi tên thống nhất)
    for bk in ('fz', 'ky', 'ld', 'kb'):
        mm = re.search(r'(<script type="application/json" id="src-%s">)(.*?)(</script>)' % bk, h, re.S)
        dd = json.loads(mm.group(2))
        pr = "catch(e){bridge=true}\nvar onParent" if False else "localStorage.removeItem('u3x:probe')}catch(e){bridge=true}"
        if pr in dd and 'bridge=true}try{if(window.parent' not in dd:
            dd = dd.replace(pr, pr + "try{if(window.parent&&window.parent!==window)bridge=true}catch(e){}")
            h = h[:mm.start(2)] + json.dumps(dd, ensure_ascii=False).replace('<', '\\u003c') + h[mm.end(2):]
    # 4) khung fz: ô đáp án phải đợi cầu nối nạp xong mới điền lại giá trị đã lưu
    m = re.search(r'(<script type="application/json" id="src-fz">)(.*?)(</script>)', h, re.S)
    d = json.loads(m.group(2))
    o = 't.value=UEX.ls.getItem(t.dataset.k)||""'
    if o in d:
        d = d.replace(o, 'UEX.ready(function(){if(!t.value)t.value=UEX.ls.getItem(t.dataset.k)||""})')
        h = h[:m.start(2)] + json.dumps(d, ensure_ascii=False).replace('<', '\\u003c') + h[m.end(2):]
    open(path, 'w', encoding='utf-8').write(h)
    print('rekey: %d key mục lục đổi' % n)

if __name__ == '__main__':
    main(sys.argv[1])
