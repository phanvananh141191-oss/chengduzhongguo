"""Đóng gói audio bài khoá theo từng bài: assets/audio/pack/<sách>-l<NN>.js (mỗi bài một file; shell nạp theo yêu cầu).
Định dạng:  window.__AP=window.__AP||{}; __AP["fz-l03"]={"fz/l03/t001":"data:audio/mpeg;base64,…", …};
Dùng: python3 tools/audio_pack.py"""
import json, os, base64, collections
ROOT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'audio')
def main():
    man = json.load(open(os.path.join(ROOT, 'manifest.json'), encoding='utf-8'))
    by = collections.defaultdict(list)
    for i in man:
        if i['kind'] == 't': by[(i['book'], i['lesson'])].append(i)
    out = os.path.join(ROOT, 'pack'); os.makedirs(out, exist_ok=True); tot = 0
    for (b, n), L in sorted(by.items()):
        d = {}
        for i in L:
            f = os.path.join(ROOT, i['file'] + '.mp3')
            if os.path.exists(f): d[i['id']] = 'data:audio/mpeg;base64,' + base64.b64encode(open(f, 'rb').read()).decode()
        key = '%s-l%02d' % (b, n)
        js = 'window.__AP=window.__AP||{};__AP[%s]=%s;' % (json.dumps(key), json.dumps(d))
        open(os.path.join(out, key + '.js'), 'w').write(js); tot += len(js)
        print('%s: %d file, %.1f MB' % (key, len(d), len(js) / 1048576))
    print('Tổng %.1f MB' % (tot / 1048576))
if __name__ == '__main__': main()
