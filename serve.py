from __future__ import annotations

import argparse
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from brain.base import SensoryState
from brain.toy import ToyBrain

ROOT = (Path(__file__).parent / "web").resolve()
BRAIN = ToyBrain()


class Handler(SimpleHTTPRequestHandler):
    def do_POST(self) -> None:
        if urlparse(self.path).path != "/api/act":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length))
            sensory = SensoryState(
                bearing=float(payload["bearing"]),
                distance=float(payload["distance"]),
            )
            action = BRAIN.act(sensory)
            self.send_json(
                {
                    "action": action,
                    "controller": type(BRAIN).__name__,
                    "biological": False,
                    "bearing": sensory.bearing,
                    "distance": sensory.distance,
                }
            )
        except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
            self.send_json({"error": str(exc)}, status=400)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/status":
            self.send_json(
                {
                    "controller": type(BRAIN).__name__,
                    "biological": False,
                    "api": "v0.3",
                }
            )
            return
        super().do_GET()

    def send_json(self, payload: dict, status: int = 200) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def translate_path(self, path: str) -> str:
        requested = urlparse(path).path.lstrip("/") or "index.html"
        candidate = (ROOT / requested).resolve()
        try:
            candidate.relative_to(ROOT)
        except ValueError:
            return str(ROOT / "__not_found__")
        return str(candidate)

    def end_headers(self) -> None:
        if urlparse(self.path).path.endswith((".js", ".css", ".html", "/")):
            self.send_header("Cache-Control", "no-store")
        super().end_headers()


def make_server(port: int) -> ThreadingHTTPServer:
    try:
        return ThreadingHTTPServer(("127.0.0.1", port), Handler)
    except PermissionError:
        if port == 0:
            raise
        print(f"Port {port} is blocked by Windows; choosing a free local port instead.")
        return ThreadingHTTPServer(("127.0.0.1", 0), Handler)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    server = make_server(args.port)
    actual_port = server.server_address[1]
    print(f"FlyBrain World v0.3: http://localhost:{actual_port}")
    print(f"Brain controller: {type(BRAIN).__name__} (biological=False)")
    server.serve_forever()
