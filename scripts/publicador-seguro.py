#!/usr/bin/env python3
"""Valida e publica um manifesto via SFTP, sem senha na linha de comando."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path, PurePosixPath

ALLOWED_EXTENSIONS = {".html", ".css", ".js", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".woff", ".woff2"}
MAX_FILE = 20 * 1024 * 1024
SAFE_HOST = re.compile(r"^[A-Za-z0-9.-]+$")
SAFE_USER = re.compile(r"^[A-Za-z0-9._-]+$")
SAFE_REMOTE_PATH = re.compile(r"^[A-Za-z0-9._/-]+$")
SAFE_LOCAL_PART = re.compile(r"^[A-Za-z0-9._ -]+$")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_manifest(path: Path, workspace: Path) -> tuple[dict, list[tuple[Path, str]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or set(data) != {"version", "jobId", "arquivos"} or data["version"] != 1:
        raise ValueError("manifesto inválido")
    if not re.fullmatch(r"[A-Za-z0-9-]{8,80}", str(data["jobId"])):
        raise ValueError("jobId inválido")
    if not isinstance(data["arquivos"], list) or not 1 <= len(data["arquivos"]) <= 200:
        raise ValueError("quantidade de arquivos inválida")
    sites = (workspace / "sites").resolve()
    validated = []
    for item in data["arquivos"]:
        if not isinstance(item, dict) or set(item) != {"origem", "destino", "sha256"}:
            raise ValueError("entrada de arquivo inválida")
        source = (workspace / str(item["origem"])).resolve()
        if sites not in source.parents or source.is_symlink() or not source.is_file():
            raise ValueError("origem deve ser arquivo regular dentro de sites/")
        if any(not SAFE_LOCAL_PART.fullmatch(part) for part in source.relative_to(sites).parts):
            raise ValueError("nome de arquivo local contém caracteres inseguros")
        if source.suffix.lower() not in ALLOWED_EXTENSIONS or source.stat().st_size > MAX_FILE:
            raise ValueError("tipo ou tamanho de arquivo não permitido")
        target = PurePosixPath(str(item["destino"]))
        if target.is_absolute() or ".." in target.parts or target.suffix.lower() not in ALLOWED_EXTENSIONS or not SAFE_REMOTE_PATH.fullmatch(target.as_posix()):
            raise ValueError("destino remoto inválido")
        if not re.fullmatch(r"[0-9a-f]{64}", str(item["sha256"])) or sha256(source) != item["sha256"]:
            raise ValueError("hash não confere")
        validated.append((source, target.as_posix()))
    return data, validated


def publish_sftp(files: list[tuple[Path, str]], host: str, user: str, port: int, key: Path | None) -> None:
    if not SAFE_HOST.fullmatch(host) or not SAFE_USER.fullmatch(user) or not 1 <= port <= 65535:
        raise ValueError("conexão SFTP inválida")
    lines = []
    for source, target in files:
        parent = str(PurePosixPath(target).parent)
        lines.append(f'-mkdir "{parent}"')
        lines.append(f'put "{source}" "{target}"')
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as batch:
        batch.write("\n".join(lines) + "\n")
        batch_path = batch.name
    try:
        command = ["sftp", "-oBatchMode=yes", "-oStrictHostKeyChecking=yes", "-P", str(port), "-b", batch_path]
        if key:
            command.extend(["-i", str(key.resolve())])
        command.append(f"{user}@{host}")
        subprocess.run(command, check=True)
    finally:
        try: os.unlink(batch_path)
        except OSError: pass


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifesto", type=Path)
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument("--host")
    parser.add_argument("--user")
    parser.add_argument("--port", type=int, default=22)
    parser.add_argument("--key", type=Path)
    parser.add_argument("--confirm", action="store_true")
    args = parser.parse_args()
    _, files = validate_manifest(args.manifesto.resolve(), args.workspace.resolve())
    print(f"Manifesto válido: {len(files)} arquivo(s).")
    for source, target in files: print(f"- {source.name} -> {target}")
    if not args.confirm:
        print("Validação concluída; use --confirm para publicar.")
        return
    if not args.host or not args.user: parser.error("--host e --user são obrigatórios com --confirm")
    publish_sftp(files, args.host, args.user, args.port, args.key)


if __name__ == "__main__": main()
