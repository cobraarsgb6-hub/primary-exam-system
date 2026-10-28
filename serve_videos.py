#!/usr/bin/env python3
"""
High-Performance Local Video Streaming Server for Primary School Assessment Portal
- Supports HTTP 206 Partial Content (Byte-Range requests for seamless video scrubbing)
- Fully CORS-enabled (Access-Control-Allow-Origin: *) for Google Apps Script Web App
- Serves metadata at /api/videos
- Fallback web player at http://127.0.0.1:8085/
"""

import os
import json
import re
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

PORT = 8085
VIDEOS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos", "arabic")
CATALOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "youtube_catalog.json")

class VideoStreamingHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, HEAD, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Range, Content-Type, Accept")
        self.send_header("Access-Control-Expose-Headers", "Content-Range, Content-Length, Accept-Ranges")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # 1. API: List available videos
        if path == "/api/videos":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            
            catalog = {}
            if os.path.exists(CATALOG_PATH):
                try:
                    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
                        for item in json.load(f):
                            vid_id = item["url"].split("v=")[-1]
                            catalog[vid_id] = item
                except Exception:
                    pass

            videos = []
            if os.path.exists(VIDEOS_DIR):
                for f in os.listdir(VIDEOS_DIR):
                    if f.endswith(".mp4"):
                        vid_id = os.path.splitext(f)[0]
                        full_path = os.path.join(VIDEOS_DIR, f)
                        meta = catalog.get(vid_id, {})
                        videos.append({
                            "id": vid_id,
                            "filename": f,
                            "size_bytes": os.path.getsize(full_path),
                            "size_mb": round(os.path.getsize(full_path) / (1024*1024), 2),
                            "title": meta.get("title", f"Video {vid_id}"),
                            "channel": meta.get("author", "Local Video"),
                            "stream_url": f"http://127.0.0.1:{PORT}/stream/{f}"
                        })

            self.wfile.write(json.dumps(videos, ensure_ascii=False, indent=2).encode("utf-8"))
            return

        # 2. Stream video file with 206 Partial Content support
        if path.startswith("/stream/"):
            filename = urllib.parse.unquote(path[len("/stream/"):])
            filepath = os.path.join(VIDEOS_DIR, filename)

            if not os.path.isfile(filepath):
                self.send_error(404, "Video file not found")
                return

            file_size = os.path.getsize(filepath)
            range_header = self.headers.get("Range")

            if range_header:
                # Handle Range: bytes=start-end
                match = re.match(r"bytes=(\d+)-(\d*)", range_header)
                if match:
                    start = int(match.group(1))
                    end = int(match.group(2)) if match.group(2) else file_size - 1
                    end = min(end, file_size - 1)
                    content_length = end - start + 1

                    self.send_response(206)
                    self.send_header("Content-Type", "video/mp4")
                    self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
                    self.send_header("Content-Length", str(content_length))
                    self.send_header("Accept-Ranges", "bytes")
                    self.end_headers()

                    with open(filepath, "rb") as f:
                        f.seek(start)
                        chunk_size = 64 * 1024
                        bytes_to_send = content_length
                        while bytes_to_send > 0:
                            read_len = min(chunk_size, bytes_to_send)
                            chunk = f.read(read_len)
                            if not chunk:
                                break
                            self.wfile.write(chunk)
                            bytes_to_send -= len(chunk)
                    return

            # Full file request
            self.send_response(200)
            self.send_header("Content-Type", "video/mp4")
            self.send_header("Content-Length", str(file_size))
            self.send_header("Accept-Ranges", "bytes")
            self.end_headers()

            with open(filepath, "rb") as f:
                while chunk := f.read(64 * 1024):
                    self.wfile.write(chunk)
            return

        # 3. Simple web dashboard
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>بوابة تشغيل الفيديوهات التعليمية المباشرة</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 24px; }}
    h1 {{ color: #38bdf8; text-align: center; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; max-width: 1200px; margin: 0 auto; }}
    .card {{ background: #1e293b; border-radius: 12px; padding: 16px; border: 1px solid #334155; }}
    video {{ width: 100%; border-radius: 8px; background: #000; margin-top: 8px; }}
    .badge {{ background: #0284c7; color: #fff; font-size: 11px; padding: 2px 8px; border-radius: 6px; }}
  </style>
</head>
<body>
  <h1>🎬 بوابة تشغيل الفيديوهات التعليمية المباشرة (Offline Direct Stream)</h1>
  <p style="text-align: center; color: #94a3b8;">الخادم يعمل بنجاح على المنفذ {PORT} ويوفر بث MP4 مباشر وسريع مع دعم التقديم والتأخير.</p>
  <div class="grid" id="video-grid">
    <p style="text-align:center;">جاري تحميل قائمة الفيديوهات...</p>
  </div>
  <script>
    fetch('/api/videos').then(r=>r.json()).then(data=>{{
      const grid = document.getElementById('video-grid');
      grid.innerHTML = data.map(v => `
        <div class="card">
          <span class="badge">${{v.size_mb}} MB</span>
          <h4 style="margin: 8px 0; font-size: 14px;">${{v.title}}</h4>
          <p style="color: #94a3b8; font-size: 12px; margin: 4px 0;">القناة: ${{v.channel}}</p>
          <video controls preload="metadata" playsinline src="${{v.stream_url}}"></video>
        </div>
      `).join('');
    }});
  </script>
</body>
</html>"""
        self.wfile.write(html.encode("utf-8"))

def run():
    server = HTTPServer(("0.0.0.0", PORT), VideoStreamingHandler)
    print(f"🚀 Video Streaming Server running on http://127.0.0.1:{PORT}")
    print(f"📁 Serving videos from: {VIDEOS_DIR}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")

if __name__ == "__main__":
    run()
