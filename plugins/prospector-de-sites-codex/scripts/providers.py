"""Contratos mínimos para desacoplar fontes, e-mail e hospedagem."""
from __future__ import annotations
from pathlib import Path
from typing import Protocol, Iterable

class LeadProvider(Protocol):
    def search(self, niche: str, city: str, limit: int) -> Iterable[dict]: ...

class EmailProvider(Protocol):
    def create_draft(self, to: str, subject: str, html: str) -> str: ...
    def replies_since(self, address: str, date: str) -> Iterable[dict]: ...

class HostingProvider(Protocol):
    def publish(self, manifest: Path, confirm: bool = False) -> None: ...
