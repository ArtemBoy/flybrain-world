from __future__ import annotations

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).parent / "web"

class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path: str) -> str:
        relative = path.split("?", 1)[0].split("#", 1)[0].lstrip("/") or "index.html"
        return str(ROOT / relative)

if __name__ == "__main__":
    print("FlyBrain World: http://localhost:8000")
    ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
