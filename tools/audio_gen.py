"""Tạo audio ElevenLabs cho manifest (tools/audio_extract.py). Không làm lại file đã có (so hash văn bản).
  export ELEVENLABS_API_KEY=...        # khoá API
  export ELEVENLABS_VOICE_ID=...       # giọng nói tiếng Trung (python3 tools/audio_gen.py --voices để xem)
  python3 tools/audio_gen.py --dry                 # chỉ đếm ký tự/ước tính dung lượng
  python3 tools/audio_gen.py --only fz/l01         # chạy theo tiền tố id (fz/l01/w, ky, ld/l03 …)
  python3 tools/audio_gen.py --limit 20            # thử vài file
"""
import os, sys, json, time, argparse, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
ROOT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'audio')
MAN = os.path.join(ROOT, 'manifest.json'); IDX = os.path.join(ROOT, 'index.json')
API = 'https://api.elevenlabs.io/v1'
FMT = 'mp3_22050_32'            # ~4 KB/giây, đủ rõ cho giọng đọc; đổi mp3_44100_64 nếu muốn chất lượng cao

def call(path, key, body=None):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body is not None else None,
                                 headers={'xi-api-key': key, 'Content-Type': 'application/json', 'Accept': 'audio/mpeg'})
    return urllib.request.urlopen(req, timeout=120).read()

def one(it, key, voice, model, idx):
    out = os.path.join(ROOT, it['id'] + '.mp3'); os.makedirs(os.path.dirname(out), exist_ok=True)
    for a in range(5):
        try:
            data = call('/text-to-speech/%s?output_format=%s' % (voice, FMT), key,
                        {'text': it['text'], 'model_id': model, 'language_code': 'zh',
                         'voice_settings': {'stability': 0.55, 'similarity_boost': 0.8, 'speed': 0.9 if it['kind'] == 't' else 0.85}})
            open(out, 'wb').write(data); idx[it['id']] = it['hash']; return len(data)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503): time.sleep(2 ** (a + 1)); continue
            raise RuntimeError('%s: HTTP %d %s' % (it['id'], e.code, e.read()[:200]))
    raise RuntimeError(it['id'] + ': hết lượt thử')

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dry', action='store_true'); ap.add_argument('--voices', action='store_true')
    ap.add_argument('--only', default=''); ap.add_argument('--limit', type=int, default=0); ap.add_argument('--model', default='eleven_multilingual_v2')
    ap.add_argument('--workers', type=int, default=3); a = ap.parse_args()
    key = os.environ.get('ELEVENLABS_API_KEY', '')
    if a.voices:
        for v in json.loads(call('/voices', key))['voices']: print(v['voice_id'], v['name'], v.get('labels', {}).get('language', ''), sep='\t')
        return
    items = json.load(open(MAN, encoding='utf-8'))
    idx = json.load(open(IDX)) if os.path.exists(IDX) else {}
    todo = [i for i in items if i['id'].startswith(a.only) and idx.get(i['id']) != i['hash']
            or (i['id'].startswith(a.only) and not os.path.exists(os.path.join(ROOT, i['id'] + '.mp3')))]
    if a.limit: todo = todo[:a.limit]
    chars = sum(len(i['text']) for i in todo)
    print('Cần tạo: %d file · %d ký tự · ước tính ~%.0f MB, ~%.1f giờ audio' % (len(todo), chars, chars / 4.5 * 4 / 1024, chars / 4.5 / 3600))
    if a.dry: return
    voice = os.environ.get('ELEVENLABS_VOICE_ID', '')
    if not key or not voice: sys.exit('Thiếu ELEVENLABS_API_KEY hoặc ELEVENLABS_VOICE_ID')
    done = 0
    def run(it):
        nonlocal done
        n = one(it, key, voice, a.model, idx); done += 1
        if done % 25 == 0: json.dump(idx, open(IDX, 'w'), indent=0); print(done, '/', len(todo), flush=True)
        return n
    with ThreadPoolExecutor(a.workers) as ex: tot = sum(ex.map(run, todo))
    json.dump(idx, open(IDX, 'w'), indent=0); print('Xong %d file, %.1f MB' % (done, tot / 1048576))
main()
