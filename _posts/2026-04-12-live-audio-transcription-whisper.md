---
layout: post
title: "Live Audio Transcription on a $0 Server Using Whisper"
permalink: /post/live-audio-transcription-whisper/
read_time: 6
---

While building [daylog](https://github.com/aag1091-alt/daylog) — a private voice diary app — I needed a way to transcribe audio from a phone in near real-time, running entirely on my own server. No OpenAI API, no Google, no third-party services. Just a microphone, a chunk of audio, and text back.

Here's how I built it, what I learned, and the open-source service I extracted from it.

---

## The problem

The browser's [MediaRecorder API](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder) lets you record audio in chunks. You can set a timeslice — every N milliseconds, it fires an `ondataavailable` event with a blob of audio. Send that blob to a server, get back a transcript, show it to the user. Simple enough in theory.

The tricky parts:

1. **WebM chunks are not standalone files.** The first chunk from `MediaRecorder` contains the WebM file header. Every subsequent chunk is raw audio data with no header. If you send chunk #2 to ffmpeg on its own, it can't decode it — it has no context for what codec, sample rate, or format to expect. I spent an embarrassing amount of time debugging silent transcriptions before I found this.

2. **Whisper is slow on CPU.** The original `openai-whisper` package uses PyTorch and takes 15–30 seconds to transcribe a 5-second chunk on a shared CPU VM. That's not a live transcription experience — that's watching paint dry.

3. **First request is always slow.** Loading a 75MB model from disk takes 10–20 seconds. If you don't warm it up at startup, the first user request times out.

---

## The solutions

### WebM header problem

The fix: don't send individual chunks. Send the **full accumulated audio** on each event. Every transcription request becomes a valid, self-contained WebM file:

```js
const chunks = [];

recorder.ondataavailable = async (e) => {
  if (e.data.size < 1000) return;
  chunks.push(e.data);

  // Full accumulated audio = always a valid WebM file
  const snapshot = new Blob(chunks, { type: e.data.type });

  const form = new FormData();
  form.append("file", snapshot, "audio.webm");
  const res = await fetch("/transcribe", { method: "POST", body: form });
  const { transcript } = await res.json();
  setLiveTranscript(transcript); // replace, don't append
};
```

The trade-off: each request sends more data than the last. For a 60-second recording with 5-second chunks, the last request sends all 60 seconds. Acceptable for a personal tool, worth optimising for production.

### Whisper performance

The original `openai-whisper` package runs on PyTorch. [faster-whisper](https://github.com/SYSTRAN/faster-whisper) uses CTranslate2 as its backend — it's 2–4x faster on CPU and uses less memory. Combined with the `tiny` model and `int8` quantization, it transcribes a 5-second chunk in roughly 2–3 seconds on a `shared-cpu-1x` Fly.io machine.

```python
from faster_whisper import WhisperModel

model = WhisperModel("tiny", device="cpu", compute_type="int8")
segments, _ = model.transcribe("audio.webm", beam_size=1)
text = " ".join(seg.text.strip() for seg in segments).strip()
```

`beam_size=1` switches from beam search to greedy decoding. For short conversational audio it makes no meaningful difference to accuracy, but it's noticeably faster.

### Cold start

Bake the model into the Docker image. It adds ~75MB to the image size but eliminates the per-deploy download:

```dockerfile
RUN python3 -c "from faster_whisper import WhisperModel; WhisperModel('tiny', device='cpu', compute_type='int8')"
```

---

## The service

I extracted this into a standalone microservice: [whisper-live-transcribe](https://github.com/aag1091-alt/whisper-live-transcribe).

It's a single FastAPI endpoint:

```
POST /transcribe
Content-Type: multipart/form-data

file: <audio file>
→ { "transcript": "what you said" }
```

That's it. No auth, no database, no state. Drop it behind your existing API or deploy it standalone.

The full `main.py` is under 60 lines:

```python
@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    suffix = Path(file.filename or "audio.webm").suffix or ".webm"

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    def _run():
        try:
            model = _get_model()
            segments, _ = model.transcribe(tmp_path, beam_size=1)
            return " ".join(seg.text.strip() for seg in segments).strip()
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    text = await asyncio.to_thread(_run)
    return {"transcript": text}
```

`asyncio.to_thread` keeps Whisper's CPU-bound work off the event loop so the server stays responsive to other requests while transcribing.

---

## Deploying to Fly.io

```bash
git clone https://github.com/aag1091-alt/whisper-live-transcribe
cd whisper-live-transcribe
fly launch --name my-transcribe-service
fly deploy --local-only
```

Total cost: **$0/month** on Fly's free tier (1 shared-cpu-1x VM). The 1GB RAM config handles the model (~150MB for tiny + runtime overhead) with room to spare.

---

## Performance numbers

Measured on `shared-cpu-1x` with 1GB RAM:

| Model | Size | Latency per 5s chunk | Notes |
|---|---|---|---|
| tiny | 75MB | ~2–3s | Sweet spot for real-time UX |
| base | 145MB | ~5–8s | Better accuracy, noticeable lag |
| small | 460MB | ~15–20s | Needs 2GB RAM |

For a live transcription experience `tiny` is the right call. The accuracy is good enough for clear speech — it occasionally stumbles on names or technical terms, but for conversational audio it's reliable.

---

## What I ended up doing instead

After shipping this for daylog, I replaced it with the [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API) — `webkitSpeechRecognition` on iOS Safari uses Apple's on-device neural engine. Results are truly instant, word-by-word as you speak, and nothing leaves the device.

But the server-side approach is still the right choice when:
- You need it to work in non-Safari browsers
- Privacy requires avoiding Google's servers (Chrome's Web Speech API sends audio to Google)
- You're building a native app without browser APIs
- You want to run a different language model or fine-tune for a specific domain

The service is sitting open-source on GitHub if you want to use it. Swap in `base` or `small` for better accuracy, or point it at a GPU and `large-v3` for near-perfect transcription.

---

*[whisper-live-transcribe on GitHub](https://github.com/aag1091-alt/whisper-live-transcribe) — PRs welcome.*
