# src/loaders/document.py

from dataclasses import dataclass

@dataclass
class Document:
    content: str
    metadata: dict
