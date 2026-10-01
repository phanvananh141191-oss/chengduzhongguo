#!/usr/bin/env python3
# Dùng kho từ vựng (CSV) làm nguồn pinyin / Hán Việt cho bài 9–14 và bổ sung từ điển pinyin cho chữ còn thiếu.
import csv,os,re,itertools
HERE=os.path.dirname(os.path.abspath(__file__))
CSV=os.path.join(HERE,'nguon','kho-tu-vung-obsidian.csv')
_rows=None
def rows():
    global _rows
    if _rows is None:
        _rows={}
        for r in csv.DictReader(open(CSV,encoding='utf-8-sig')):
            _rows[r['hanzi'].strip()]=r
    return _rows
TONE={'ā':'a','á':'a','ǎ':'a','à':'a','ē':'e','é':'e','ě':'e','è':'e','ī':'i','í':'i','ǐ':'i','ì':'i','ō':'o','ó':'o','ǒ':'o','ò':'o','ū':'u','ú':'u','ǔ':'u','ù':'u','ǖ':'v','ǘ':'v','ǚ':'v','ǜ':'v','ü':'v'}
def base(s): return ''.join(TONE.get(c,c) for c in s.lower())
INI=['zh','ch','sh','b','p','m','f','d','t','n','l','g','k','h','j','q','x','r','z','c','s','y','w','']
FIN=['a','o','e','i','u','v','ai','ei','ao','ou','an','en','ang','eng','ong','ia','ie','iao','iu','ian','in','iang','ing','iong','ua','uo','uai','ui','uan','un','uang','ueng','ve','van','vn','er','io']
VALID=set(i+f for i in INI for f in FIN)|{'r','n','ng','m','hm','hng'}
def splits(b,pos=0,memo=None):
    # mọi cách tách chuỗi (đã bỏ dấu) thành âm tiết hợp lệ -> danh sách các list độ dài
    if memo is None: memo={}
    if pos==len(b): return [[]]
    if pos in memo: return memo[pos]
    out=[]
    for L in range(min(6,len(b)-pos),0,-1):
        s=b[pos:pos+L]
        if s in VALID:
            for rest in splits(b,pos+L,memo): out.append([L]+rest)
    memo[pos]=out; return out
def syllables(word,py):
    """tách pinyin của một từ thành đúng len(word) âm tiết; không chắc chắn -> None"""
    py=py.strip().replace('’',"'")
    groups=[g for g in re.split(r"[\s\-·']+",py) if g]
    n=len(word)
    # mỗi nhóm: các cách tách
    opts=[]
    for g in groups:
        b=base(g)
        sp=splits(b)
        if not sp: return None
        opts.append(sp)
    for combo in itertools.product(*[range(len(o)) for o in opts]):
        parts=[opts[i][c] for i,c in enumerate(combo)]
        if sum(len(p) for p in parts)==n:
            res=[]
            for g,p in zip(groups,parts):
                pos=0
                for L in p: res.append(g[pos:pos+L]); pos+=L
            return res
        if len(combo)>2000: break
    return None
def lookup(w):
    return rows().get(w)
