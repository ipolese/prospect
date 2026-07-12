#!/usr/bin/env python3
"""Preview somente leitura, limitado ao diretório sites/."""

from __future__ import annotations

import argparse
import mimetypes
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ALLOWED = {".html", ".css", ".js", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".woff", ".woff2"}


def resolve_public_path(root: Path, raw: str) -> Path:
    path = urllib.parse.unquote(raw.split("?", 1)[0]).lstrip("/")
    if path in {"", "index.html"}:
        return root
    candidate = (root / path).resolve()
    resolved_root = root.resolve()
    if candidate != resolved_root and resolved_root not in candidate.parents:
        raise ValueError("caminho fora da raiz pública")
    if candidate.is_symlink():
        raise ValueError("links simbólicos não são permitidos")
    return candidate


def handler_for(root: Path):
    class PreviewHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            try:
                path = resolve_public_path(root, self.path)
            except ValueError:
                return self.send_error(403)
            if path == root.resolve():
                body = b"Prospector preview: abra /sites/[slug]/[slug].html\n"
                return self.respond(200, "text/plain; charset=utf-8", body)
            if not path.is_file() or path.suffix.lower() not in ALLOWED:
                return self.send_error(404)
            mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
            self.respond(200, mime, path.read_bytes())

        def respond(self, status: int, mime: str, body: bytes) -> None:
            self.send_response(status)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Cache-Control", "no-store")
            self.end_headers(); self.wfile.write(body)

        def log_message(self, *_): pass

    return PreviewHandler


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve exclusivamente os previews do Prospector")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8766)
    parser.add_argument("--dir", default=".", help="raiz do workspace; somente sites/ será exposto")
    args = parser.parse_args()
    if args.host not in {"127.0.0.1", "localhost"}:
        parser.error("por segurança, o preview aceita apenas 127.0.0.1/localhost")
    workspace = Path(args.dir).expanduser().resolve()
    sites = workspace / "sites"
    sites.mkdir(parents=True, exist_ok=True)
    print(f"Preview em http://127.0.0.1:{args.port}/sites/")
    ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(workspace)).serve_forever()


if __name__ == "__main__": main()
