"""Tạo audio ElevenLabs cho manifest (tools/audio_extract.py). Không làm lại file đã có (so hash văn bản).
  export ELEVENLABS_API_KEY=...        # khoá API
  export (giọng chọn theo manifest: từ vựng xoay vòng 5 giọng; bài khoá một giọng mỗi bài/nhóm bài chung câu dài)
  python3 tools/audio_gen.py --dry                 # chỉ đếm ký tự/ước tính dung lượng
  python3 tools/audio_gen.py --only fz/l01         # chạy theo tiền tố id (fz/l01/w, ky, ld/l03 …)
  python3 tools/audio_gen.py --limit 20            # thử vài file
"""
import os, sys, json, time, argparse, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
ROOT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'audio')
MAN = os.path.join(ROOT, 'manifest.json'); IDX = os.path.join(ROOT, 'index.json')
API = 'https://api.elevenlabs.io/v1'
sys.path.insert(0, os.path.dirname(__file__))
from audio_voices import VOICES
FMT = 'mp3_22050_32'            # ~4 KB/giây, đủ rõ cho giọng đọc; đổi mp3_44100_64 nếu muốn chất lượng cao

def call(path, key, body=None):
    path = path.replace('/user/subscription', '/user/subscription')
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body is not None else None,
                                 headers={'xi-api-key': key, 'Content-Type': 'application/json', 'Accept': 'audio/mpeg' if body is not None else 'application/json'})
    return urllib.request.urlopen(req, timeout=120).read()

def one(it, key, voice_unused, model, idx):
    voice = VOICES[it['voice']]
    out = os.path.join(ROOT, it['file'] + '.mp3'); os.makedirs(os.path.dirname(out), exist_ok=True)
    for a in range(5):
        try:
            data = call('/text-to-speech/%s?output_format=%s' % (voice, FMT), key,
                        {'text': it['text'], 'model_id': model, 'language_code': 'zh',
                         'voice_settings': {'stability': 0.55, 'similarity_boost': 0.8, 'speed': 0.9 if it['kind'] == 't' else 0.85}})
            open(out, 'wb').write(data); idx[it['file']] = it['hash']; return len(data)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503): time.sleep(2 ** (a + 1)); continue
            raise RuntimeError('%s: HTTP %d %s' % (it['id'], e.code, e.read()[:200]))
    raise RuntimeError(it['id'] + ': hết lượt thử')

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dry', action='store_true'); ap.add_argument('--voices', action='store_true')
    ap.add_argument('--only', default=''); ap.add_argument('--kind', default='', help='w = chỉ từ vựng, t = chỉ bài khoá'); ap.add_argument('--limit', type=int, default=0); ap.add_argument('--model', default='eleven_v4')
    ap.add_argument('--workers', type=int, default=3); a = ap.parse_args()
    key = os.environ.get('ELEVENLABS_API_KEY', '')
    if a.voices:
        for v in json.loads(call('/voices', key))['voices']: print(v['voice_id'], v['name'], v.get('labels', {}).get('language', ''), sep='\t')
        return
    items = json.load(open(MAN, encoding='utf-8'))
    idx = json.load(open(IDX)) if os.path.exists(IDX) else {}
    seen = set(); todo = []
    for i in items:     # mỗi file mp3 (từ/câu trùng giữa các giáo trình) chỉ tạo một lần
        if not i['id'].startswith(a.only) or (a.kind and i['kind'] != a.kind) or i['file'] in seen: continue
        seen.add(i['file'])
        if idx.get(i['file']) != i['hash'] or not os.path.exists(os.path.join(ROOT, i['file'] + '.mp3')): todo.append(i)
    prio = lambda i: 0 if i['kind'] == 'w' else (0 if i['book'] != 'ky' else (1 if i.get('speaker') else 2))
    todo.sort(key=prio)                     # fz, ld → hội thoại ky → phần còn lại của ky
    if a.limit: todo = todo[:a.limit]
    chars = sum(len(i['text']) for i in todo)
    print('Cần tạo: %d file · %d ký tự · ước tính ~%.0f MB, ~%.1f giờ audio' % (len(todo), chars, chars / 4.5 * 4 / 1024, chars / 4.5 / 3600))
    if a.dry: return
    voice = ''
    if not key: sys.exit('Thiếu ELEVENLABS_API_KEY')
    done = 0
    def run(it):
        nonlocal done
        n = one(it, key, voice, a.model, idx); done += 1
        if done % 25 == 0: json.dump(idx, open(IDX, 'w'), indent=0); print(done, '/', len(todo), flush=True)
        return n
    def remaining():
        try:
            d = json.loads(call('/user/subscription', key)); return d['character_limit'] - d['character_count']
        except Exception: return 10 ** 9
    tot = 0; stopped = None
    with ThreadPoolExecutor(a.workers) as ex:
        for k in range(0, len(todo), 60):          # từng lô 60 file; dừng khi sắp hết hạn mức ký tự
            batch = todo[k:k + 60]; need = sum(len(i['text']) for i in batch)
            if remaining() < need + 300: stopped = k; break
            tot += sum(ex.map(run, batch))
    if stopped is not None: print('DỪNG vì sắp hết hạn mức ký tự: còn %d file chưa tạo' % (len(todo) - stopped))
    json.dump(idx, open(IDX, 'w'), indent=0); print('Xong %d file, %.1f MB' % (done, tot / 1048576))
main()
