from __future__ import annotations

from collections import deque
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import threading
import time
from typing import Any
from urllib.parse import urlparse

try:
    import zmq
except ImportError:  # pragma: no cover
    zmq = None


class FusionUiState:
    def __init__(self, *, retention_sec: float = 15.0, event_limit: int = 200) -> None:
        self.retention_sec = retention_sec
        self.video_streams: dict[str, dict[str, Any]] = {}
        self.events: deque[dict[str, Any]] = deque(maxlen=event_limit)
        self.lock = threading.RLock()

    def add_video_frame(self, payload: dict[str, Any]) -> None:
        now = time.time()
        title = str(payload.get("title") or "MindBridge Camera")
        item = {
            "title": title,
            "frame_base64": payload.get("frame_base64", ""),
            "mime_type": payload.get("mime_type") or "image/jpeg",
            "source": payload.get("source") or "MindBridge",
            "metadata": payload.get("metadata") or {},
            "timestamp": now,
        }
        with self.lock:
            self.video_streams[title] = item
            self._prune_locked(now)

    def add_event(self, topic: str, payload: Any) -> None:
        with self.lock:
            self.events.appendleft(
                {
                    "topic": topic,
                    "payload": payload,
                    "timestamp": time.time(),
                }
            )

    def snapshot(self) -> dict[str, Any]:
        now = time.time()
        with self.lock:
            self._prune_locked(now)
            return {
                "video_streams": list(self.video_streams.values()),
                "events": list(self.events),
                "server_time": now,
            }

    def _prune_locked(self, now: float) -> None:
        stale = [
            title
            for title, item in self.video_streams.items()
            if now - float(item.get("timestamp", 0.0)) > self.retention_sec
        ]
        for title in stale:
            self.video_streams.pop(title, None)


HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MindBridge Fusion</title>
  <style>
    :root { color-scheme: dark; font-family: Arial, sans-serif; }
    body { margin: 0; background: #111318; color: #eef2f7; }
    header { padding: 14px 18px; border-bottom: 1px solid #2a2f3a; display: flex; justify-content: space-between; align-items: center; }
    main { display: grid; grid-template-columns: minmax(320px, 2fr) minmax(320px, 1fr); gap: 16px; padding: 16px; }
    section { background: #181c23; border: 1px solid #2a2f3a; border-radius: 8px; overflow: hidden; }
    h2 { font-size: 15px; margin: 0; padding: 10px 12px; border-bottom: 1px solid #2a2f3a; }
    .videos { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 12px; padding: 12px; }
    .video { background: #0f1217; border: 1px solid #2a2f3a; border-radius: 6px; overflow: hidden; }
    .video img { width: 100%; display: block; background: #080a0d; }
    .meta { padding: 8px 10px; font-size: 12px; color: #b6c0cf; display: flex; justify-content: space-between; gap: 8px; }
    .events { max-height: calc(100vh - 120px); overflow: auto; padding: 8px; }
    .event { border-bottom: 1px solid #2a2f3a; padding: 8px 4px; font-size: 12px; }
    .topic { color: #7cc7ff; font-weight: 700; }
    pre { margin: 6px 0 0; white-space: pre-wrap; word-break: break-word; color: #d9e2ef; }
    .muted { color: #8b96a8; font-size: 12px; }
    @media (max-width: 900px) { main { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <header>
    <strong>MindBridge Fusion</strong>
    <span id="status" class="muted">connecting...</span>
  </header>
  <main>
    <section>
      <h2>Video</h2>
      <div id="videos" class="videos"></div>
    </section>
    <section>
      <h2>ZMQ Events</h2>
      <div id="events" class="events"></div>
    </section>
  </main>
  <script>
    const videosEl = document.getElementById("videos");
    const eventsEl = document.getElementById("events");
    const statusEl = document.getElementById("status");
    function fmtTime(ts) {
      if (!ts) return "-";
      return new Date(ts * 1000).toLocaleTimeString();
    }
    async function refresh() {
      try {
        const res = await fetch("/api/state", {cache: "no-store"});
        const data = await res.json();
        statusEl.textContent = "updated " + fmtTime(data.server_time);
        videosEl.innerHTML = "";
        for (const item of data.video_streams || []) {
          const card = document.createElement("div");
          card.className = "video";
          const img = document.createElement("img");
          img.src = `data:${item.mime_type || "image/jpeg"};base64,${item.frame_base64 || ""}`;
          const meta = document.createElement("div");
          meta.className = "meta";
          meta.innerHTML = `<span>${item.title || "Video"}</span><span>${item.source || ""} ${fmtTime(item.timestamp)}</span>`;
          card.appendChild(img);
          card.appendChild(meta);
          videosEl.appendChild(card);
        }
        eventsEl.innerHTML = "";
        for (const event of data.events || []) {
          const row = document.createElement("div");
          row.className = "event";
          const payload = JSON.stringify(event.payload, null, 2);
          row.innerHTML = `<div><span class="topic">${event.topic}</span> <span class="muted">${fmtTime(event.timestamp)}</span></div><pre></pre>`;
          row.querySelector("pre").textContent = payload;
          eventsEl.appendChild(row);
        }
      } catch (err) {
        statusEl.textContent = "offline";
      }
    }
    refresh();
    setInterval(refresh, 500);
  </script>
</body>
</html>
"""


def make_handler(state: FusionUiState) -> type[BaseHTTPRequestHandler]:
    class FusionUiHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            path = urlparse(self.path).path
            if path == "/":
                self._send_bytes(HTML.encode("utf-8"), "text/html; charset=utf-8")
                return
            if path in {"/api/state", "/api/video-streams", "/api/events"}:
                self._send_json(state.snapshot())
                return
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")

        def do_POST(self) -> None:
            path = urlparse(self.path).path
            if path != "/api/video-stream":
                self.send_error(HTTPStatus.NOT_FOUND, "Not found")
                return
            try:
                payload = self._read_json()
                state.add_video_frame(payload)
                self._send_json({"status": "ok"})
            except Exception as exc:
                self.send_error(HTTPStatus.BAD_REQUEST, str(exc))

        def log_message(self, format: str, *args: Any) -> None:
            return

        def _read_json(self) -> dict[str, Any]:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            payload = json.loads(raw.decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("JSON root must be an object")
            return payload

        def _send_json(self, payload: dict[str, Any]) -> None:
            self._send_bytes(
                json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                "application/json; charset=utf-8",
            )

        def _send_bytes(self, payload: bytes, content_type: str) -> None:
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)

    return FusionUiHandler


def start_zmq_listener(state: FusionUiState, addr: str) -> threading.Thread | None:
    if not addr:
        return None
    if zmq is None:
        raise RuntimeError("Fusion ZMQ listener requires pyzmq.")

    def _worker() -> None:
        context = zmq.Context.instance()
        sock = context.socket(zmq.SUB)
        sock.setsockopt(zmq.RCVHWM, 100)
        sock.setsockopt(zmq.LINGER, 0)
        sock.connect(addr)
        sock.setsockopt_string(zmq.SUBSCRIBE, "")
        while True:
            try:
                message = sock.recv_string()
                topic, _, raw_payload = message.partition(" ")
                try:
                    payload = json.loads(raw_payload) if raw_payload else {}
                except json.JSONDecodeError:
                    payload = raw_payload
                state.add_event(topic or "message", payload)
            except Exception as exc:
                state.add_event("fusion.listener.error", {"message": str(exc)})
                time.sleep(0.5)

    thread = threading.Thread(target=_worker, daemon=True)
    thread.start()
    return thread


def serve_ui(
    *,
    host: str = "127.0.0.1",
    port: int = 8765,
    zmq_sub_addr: str = "tcp://127.0.0.1:8899",
) -> None:
    state = FusionUiState()
    start_zmq_listener(state, zmq_sub_addr)
    server = ThreadingHTTPServer((host, port), make_handler(state))
    print(f"[FusionUI] http://{host}:{port}")
    print(f"[FusionUI] ZMQ SUB {zmq_sub_addr}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
