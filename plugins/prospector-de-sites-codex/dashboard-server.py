#!/usr/bin/env python3
"""Dashboard local seguro do Prospector, sem dependências externas."""

from __future__ import annotations

import html
import json
import os
import secrets
import sqlite3
import threading
import time
import urllib.parse
import re
import webbrowser
from http import cookies
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

HOST = "127.0.0.1"
PORT = 8765
MAX_BODY = 256 * 1024
ROOT = Path(__file__).resolve().parent
DB = ROOT / "prospector.db"
CONFIG = ROOT / "prospector-config.json"
DASHBOARD = ROOT / "dashboard.html"
SITES = ROOT / "sites"
SESSION_TTL = 8 * 60 * 60

FIELDS = {
    "slug", "nome", "nicho", "cidade", "nota", "avaliacoes", "email", "telefone",
    "whatsapp", "placeId", "siteAntigo", "motivo", "status", "urlNova", "dataProposta", "valor",
    "obs", "contratoStatus", "contratoEm", "manutencao", "pago", "docCliente", "endCliente",
}
TEXT_FIELDS = FIELDS - {"nota", "avaliacoes", "valor", "manutencao", "pago"}
STATUS = {"novo", "redesenhado", "publicado-local", "publicado", "proposta-rascunho", "proposta", "respondeu", "negociacao", "fechado", "perdido", "descartado"}
CONTRACT_STATUS = {"pendente", "enviado", "assinado"}
CONFIG_FIELDS = {"nome", "cpfCnpj", "endereco", "cidadeUf", "email", "whatsapp"}
HOSTING_FIELDS = {"habilitado", "usuario", "dominio", "servidor", "porta", "pastaBase", "chaveSsh"}
SESSIONS: dict[str, tuple[str, float]] = {}
LOCK = threading.Lock()


def connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS leads(
      slug TEXT PRIMARY KEY, nome TEXT, nicho TEXT, cidade TEXT, nota REAL, avaliacoes INTEGER,
      email TEXT, telefone TEXT, whatsapp TEXT, placeId TEXT, siteAntigo TEXT, motivo TEXT,
      status TEXT DEFAULT 'novo', urlNova TEXT, dataProposta TEXT, valor REAL, obs TEXT,
      contratoStatus TEXT DEFAULT 'pendente', contratoEm TEXT, manutencao REAL, pago INTEGER DEFAULT 0,
      docCliente TEXT, endCliente TEXT,
      atualizado TEXT DEFAULT (datetime('now','localtime')))""")
    try: conn.execute("ALTER TABLE leads ADD COLUMN placeId TEXT")
    except sqlite3.OperationalError: pass
    conn.execute("""CREATE TABLE IF NOT EXISTS audit_log(
      id INTEGER PRIMARY KEY AUTOINCREMENT, lead_slug TEXT, evento TEXT NOT NULL,
      origem TEXT NOT NULL DEFAULT 'dashboard', antes_json TEXT, depois_json TEXT,
      criado_em TEXT DEFAULT (datetime('now','localtime')))""")
    return conn

def audit(conn: sqlite3.Connection, slug: str | None, event: str, before: Any, after: Any) -> None:
    conn.execute("INSERT INTO audit_log(lead_slug,evento,origem,antes_json,depois_json) VALUES(?,?,?,?,?)",
                 (slug, event, "dashboard", json.dumps(before, ensure_ascii=False), json.dumps(after, ensure_ascii=False)))


def read_config() -> dict[str, Any]:
    try:
        value = json.loads(CONFIG.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def write_config(value: dict[str, Any]) -> None:
    temp = CONFIG.with_suffix(".json.tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        os.chmod(temp, 0o600)
    except OSError:
        pass
    temp.replace(CONFIG)


def safe_slug(value: Any) -> str:
    value = str(value or "").strip().lower()
    if not value or len(value) > 80 or any(ch not in "abcdefghijklmnopqrstuvwxyz0123456789-" for ch in value):
        raise ValueError("slug inválido")
    return value


def safe_url(value: Any, *, optional: bool = True) -> str | None:
    if value in (None, "") and optional:
        return None
    value = str(value).strip()
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or len(value) > 2048:
        raise ValueError("URL deve usar HTTP ou HTTPS")
    return value


def clean_text(value: Any, limit: int = 4000) -> str | None:
    if value is None:
        return None
    value = str(value).replace("\x00", "").strip()
    return value[:limit]

def normalized_contact(value: Any) -> str:
    value = re.sub(r"^https?://", "", str(value or "").lower())
    return re.sub(r"[^a-z0-9]", "", value.replace("www.", ""))

def duplicate_slug(conn: sqlite3.Connection, lead: dict[str, Any]) -> str | None:
    keys = {normalized_contact(lead.get("siteAntigo")), normalized_contact(lead.get("telefone") or lead.get("whatsapp"))} - {""}
    if not keys: return None
    for row in conn.execute("SELECT slug,siteAntigo,telefone,whatsapp FROM leads"):
        if row[0] == lead.get("slug"): continue
        existing = {normalized_contact(row[1]), normalized_contact(row[2] or row[3])} - {""}
        if keys & existing: return row[0]
    return None


def validate_lead(payload: Any, *, partial: bool = False) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("objeto JSON esperado")
    unknown = set(payload) - FIELDS
    if unknown:
        raise ValueError("campos desconhecidos: " + ", ".join(sorted(unknown)))
    out: dict[str, Any] = {}
    for key, value in payload.items():
        if key == "slug":
            out[key] = safe_slug(value)
        elif key in {"siteAntigo", "urlNova"}:
            out[key] = safe_url(value)
        elif key == "status":
            if value not in STATUS:
                raise ValueError("status inválido")
            out[key] = value
        elif key == "contratoStatus":
            if value not in CONTRACT_STATUS:
                raise ValueError("status de contrato inválido")
            out[key] = value
        elif key in {"nota", "valor", "manutencao"}:
            out[key] = None if value in (None, "") else float(value)
            if key == "nota" and out[key] is not None and not 0 <= out[key] <= 5:
                raise ValueError("nota fora do intervalo")
            if key != "nota" and out[key] is not None and out[key] < 0:
                raise ValueError("valor negativo")
        elif key in {"avaliacoes", "pago"}:
            out[key] = 0 if value in (None, "") else int(value)
            if out[key] < 0 or (key == "pago" and out[key] not in {0, 1}):
                raise ValueError("inteiro inválido")
        else:
            out[key] = clean_text(value)
    if not partial and "slug" not in out:
        raise ValueError("slug obrigatório")
    return out


def public_lead(row: sqlite3.Row) -> dict[str, Any]:
    result = dict(row)
    # O template legado usa innerHTML. Codificar texto aqui bloqueia HTML ativo;
    # URLs e slugs já passaram por validação própria.
    for key in TEXT_FIELDS - {"slug", "siteAntigo", "urlNova", "status", "contratoStatus"}:
        if result.get(key) is not None:
            result[key] = html.escape(str(result[key]), quote=True)
    return result


def safe_site_path(raw_path: str) -> Path:
    decoded = urllib.parse.unquote(raw_path)
    relative = decoded.removeprefix("/sites/")
    candidate = (SITES / relative).resolve()
    root = SITES.resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError("caminho fora de sites")
    if candidate.is_symlink() or candidate.suffix.lower() not in {".html", ".css", ".js", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".woff", ".woff2"}:
        raise ValueError("arquivo não permitido")
    return candidate


class App(BaseHTTPRequestHandler):
    server_version = "ProspectorLocal/2"

    def send_security_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")

    def json_response(self, code: int, value: Any) -> None:
        body = json.dumps(value, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_security_headers()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def error_json(self, code: int, message: str) -> None:
        self.json_response(code, {"erro": message})

    def origin_ok(self) -> bool:
        origin = self.headers.get("Origin")
        host = self.headers.get("Host", "")
        return host in {f"{HOST}:{PORT}", f"localhost:{PORT}"} and (not origin or origin in {f"http://{HOST}:{PORT}", f"http://localhost:{PORT}"})

    def current_session(self) -> tuple[str, str] | None:
        jar = cookies.SimpleCookie(self.headers.get("Cookie", ""))
        sid = jar.get("prospector_session")
        if not sid:
            return None
        with LOCK:
            data = SESSIONS.get(sid.value)
        if not data or data[1] < time.time():
            return None
        return sid.value, data[0]

    def require_mutation_auth(self) -> bool:
        session = self.current_session()
        if not self.origin_ok() or not session or not secrets.compare_digest(self.headers.get("X-CSRF-Token", ""), session[1]):
            self.error_json(403, "origem, sessão ou CSRF inválido")
            return False
        return True

    def read_json(self) -> Any:
        if self.headers.get_content_type() != "application/json":
            raise ValueError("Content-Type deve ser application/json")
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ValueError("Content-Length inválido") from exc
        if length <= 0 or length > MAX_BODY:
            raise OverflowError("corpo vazio ou acima de 256 KB")
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def serve_dashboard(self) -> None:
        if not DASHBOARD.exists():
            return self.error_json(404, "dashboard.html ausente")
        sid, csrf = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
        with LOCK:
            SESSIONS[sid] = (csrf, time.time() + SESSION_TTL)
        bootstrap = '<meta name="prospector-csrf" content="' + csrf + '">'
        body = DASHBOARD.read_text(encoding="utf-8").replace("</head>", bootstrap + "</head>").encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Set-Cookie", f"prospector_session={sid}; HttpOnly; SameSite=Strict; Path=/; Max-Age={SESSION_TTL}")
        self.send_security_headers()
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; frame-src 'self' https:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def serve_site(self) -> None:
        try:
            path = safe_site_path(self.path.split("?", 1)[0])
        except ValueError as exc:
            return self.error_json(403, str(exc))
        if not path.is_file():
            return self.error_json(404, "arquivo ausente")
        mime = {".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml"}.get(path.suffix.lower(), "application/octet-stream")
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_security_headers()
        # Sites de clientes são conteúdo não confiável. O sandbox torna a
        # origem do iframe opaca, impedindo acesso ao cookie/API do dashboard,
        # mesmo quando a página contém JavaScript coletado ou editado.
        if path.suffix.lower() == ".html":
            self.send_header(
                "Content-Security-Policy",
                "sandbox allow-scripts; default-src 'self' https: data:; "
                "img-src 'self' https: data:; style-src 'self' 'unsafe-inline' https:; "
                "font-src 'self' https: data:; connect-src 'none'; "
                "frame-ancestors 'self'",
            )
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]
        if path in {"/", "/dashboard.html"}:
            return self.serve_dashboard()
        if path == "/dashboard-app.js":
            app = ROOT / "dashboard-app.js"
            if not app.is_file(): return self.error_json(404, "dashboard-app.js ausente")
            body = app.read_bytes(); self.send_response(200); self.send_header("Content-Type", "text/javascript; charset=utf-8"); self.send_security_headers(); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body); return
        if path.startswith("/sites/"):
            return self.serve_site()
        if path == "/api/config":
            if not self.current_session():
                return self.error_json(401, "sessão obrigatória")
            cfg = read_config()
            hosting = {k: v for k, v in cfg.get("hostgator", {}).items() if k in HOSTING_FIELDS}
            return self.json_response(200, {"contratante": cfg.get("contratante", {}), "hostgator": hosting})
        if path == "/api/leads":
            if not self.current_session():
                return self.error_json(401, "sessão obrigatória")
            conn = connection(); conn.row_factory = sqlite3.Row
            rows = [public_lead(row) for row in conn.execute("SELECT * FROM leads").fetchall()]
            conn.close()
            return self.json_response(200, rows)
        return self.error_json(404, "rota inexistente")

    def do_POST(self) -> None:
        if not self.require_mutation_auth(): return
        if self.path.split("?", 1)[0] != "/api/leads": return self.error_json(404, "rota inexistente")
        try: lead = validate_lead(self.read_json())
        except OverflowError as exc: return self.error_json(413, str(exc))
        except (ValueError, json.JSONDecodeError) as exc: return self.error_json(400, str(exc))
        cols = sorted(lead)
        conn = connection()
        before = conn.execute("SELECT * FROM leads WHERE slug=?", (lead["slug"],)).fetchone()
        duplicate = duplicate_slug(conn, lead)
        if duplicate: conn.close(); return self.error_json(409, f"possível duplicata de {duplicate}")
        conn.execute(f"INSERT INTO leads ({','.join(cols)}) VALUES ({','.join('?' for _ in cols)}) ON CONFLICT(slug) DO UPDATE SET " + ",".join(f"{c}=excluded.{c}" for c in cols if c != "slug"), [lead[c] for c in cols])
        audit(conn, lead["slug"], "upsert", dict(before) if before else None, lead)
        conn.commit(); conn.close()
        return self.json_response(200, {"ok": True})

    def do_PUT(self) -> None:
        if not self.require_mutation_auth(): return
        path = self.path.split("?", 1)[0]
        try: payload = self.read_json()
        except OverflowError as exc: return self.error_json(413, str(exc))
        except (ValueError, json.JSONDecodeError) as exc: return self.error_json(400, str(exc))
        if path == "/api/config":
            if not isinstance(payload, dict) or set(payload) - {"contratante", "hostgator"}: return self.error_json(400, "bloco de configuração inválido")
            cfg = read_config()
            for section, allowed in (("contratante", CONFIG_FIELDS), ("hostgator", HOSTING_FIELDS)):
                if section in payload:
                    if not isinstance(payload[section], dict) or set(payload[section]) - allowed: return self.error_json(400, f"campos inválidos em {section}")
                    cfg[section] = {**cfg.get(section, {}), **{k: clean_text(v, 512) for k, v in payload[section].items()}}
            write_config(cfg)
            return self.json_response(200, {"ok": True})
        parts = path.split("/")
        if len(parts) == 4 and parts[1:3] == ["api", "leads"]:
            try: slug, changes = safe_slug(parts[3]), validate_lead(payload, partial=True)
            except ValueError as exc: return self.error_json(400, str(exc))
            changes.pop("slug", None)
            if changes:
                cols = sorted(changes); conn = connection(); before = conn.execute("SELECT * FROM leads WHERE slug=?", (slug,)).fetchone()
                conn.execute("UPDATE leads SET " + ",".join(f"{c}=?" for c in cols) + ", atualizado=datetime('now','localtime') WHERE slug=?", [changes[c] for c in cols] + [slug])
                audit(conn, slug, "update", dict(before) if before else None, changes)
                conn.commit(); conn.close()
            return self.json_response(200, {"ok": True})
        return self.error_json(404, "rota inexistente")

    def do_DELETE(self) -> None:
        if not self.require_mutation_auth(): return
        parts = self.path.split("?", 1)[0].split("/")
        if len(parts) != 4 or parts[1:3] != ["api", "leads"]: return self.error_json(404, "rota inexistente")
        try: slug = safe_slug(parts[3])
        except ValueError as exc: return self.error_json(400, str(exc))
        conn = connection(); before = conn.execute("SELECT * FROM leads WHERE slug=?", (slug,)).fetchone()
        conn.execute("CREATE TABLE IF NOT EXISTS leads_deleted AS SELECT *, datetime('now','localtime') AS removido FROM leads WHERE 0")
        conn.execute("INSERT INTO leads_deleted SELECT *, datetime('now','localtime') FROM leads WHERE slug=?", (slug,))
        conn.execute("DELETE FROM leads WHERE slug=?", (slug,)); audit(conn, slug, "delete", dict(before) if before else None, None); conn.commit(); conn.close()
        return self.json_response(200, {"ok": True})

    def log_message(self, *_: Any) -> None:
        pass


if __name__ == "__main__":
    connection().close()
    print(f"Prospector seguro em http://{HOST}:{PORT} (Ctrl+C para parar)")
    try: webbrowser.open(f"http://{HOST}:{PORT}")
    except Exception: pass
    try: ThreadingHTTPServer((HOST, PORT), App).serve_forever()
    except KeyboardInterrupt: print("\nEncerrado.")
