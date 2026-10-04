"""Giao diện web: nội dung bài học rộng hết khung (không giới hạn 860px) và cỡ chữ mặc định 14pt (≈18,67px) cho cả 3 giáo trình.
Chạy cuối build_v4.sh.  Dùng: python3 tools/ui_fullwidth.py <html>"""
import re, sys
PT14 = 18.67      # 14pt = 14 × 96/72 px
def main(path):
    h = open(path, encoding='utf-8').read(); n = {}
    def sub(pat, rep, key):
        nonlocal h
        h, c = re.subn(pat, rep, h); n[key] = n.get(key, 0) + c
    sub(r'main\{max-width:860px!important;margin:0 auto!important;padding:(\d+(?:px)?) 20px 96px!important', r'main{max-width:none!important;margin:0!important;padding:\1 clamp(14px,2.2vw,40px) 96px!important', 'main860')
    sub(r'main\{max-width:820px;margin:auto;padding:16px\}', 'main{max-width:none;margin:0;padding:16px}', 'main820')
    sub(r'\.wrap\{max-width:1180px;margin:0 auto;padding:0 18px\}', '.wrap{max-width:none;margin:0;padding:0 clamp(14px,2.2vw,40px)}', 'ldwrap')
    sub(r'SC=\{ky:18,fz:16\.5,ld:1\.02\}', 'SC={ky:%s,fz:%s,ld:%.3f}' % (PT14, PT14, PT14 / 16), 'SC')
    sub(r'\{--fs:calc\(18px\*var\(--u-scale,1\)\)\}', '{--fs:calc(%spx*var(--u-scale,1))}' % PT14, 'ky_fs')
    sub(r'body\{font-size:calc\(16\.5px\*var\(--u-scale,1\)\)!important\}', 'body{font-size:calc(%spx*var(--u-scale,1))!important}' % PT14, 'fz_fs')
    open(path, 'w', encoding='utf-8').write(h); print('ui_fullwidth:', n)
if __name__ == '__main__': main(sys.argv[1])
