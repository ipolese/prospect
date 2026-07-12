"""Logging estruturado local sem registrar segredos ou conteúdo pessoal."""
from __future__ import annotations
import json, logging, re
from pathlib import Path
_SECRET = re.compile(r'(senha|password|token|secret|authorization)', re.I)
class RedactingFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)
        return '[REDACTED]' if _SECRET.search(message) else message
def logger(name='prospector', path: Path | None = None):
    log = logging.getLogger(name); log.setLevel(logging.INFO)
    if not log.handlers:
        handler = logging.FileHandler(path or 'prospector.log', encoding='utf-8')
        handler.setFormatter(RedactingFormatter('%(asctime)s %(levelname)s %(message)s')); log.addHandler(handler)
    return log
