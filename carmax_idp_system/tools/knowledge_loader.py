#!/usr/bin/env python3
"""
CarMax IDP System — Knowledge Base Loader
Scans all knowledge_base/ and generated/ folders, loads text content,
and provides structured access to the entire corpus for generators.
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
KB_DIR = PROJECT_ROOT / "knowledge_base"
GEN_DIR = PROJECT_ROOT / "generated"
FEEDBACK_DIR = PROJECT_ROOT / "feedback_loop"
INDEX_FILE = FEEDBACK_DIR / "corpus_index.json"

READABLE_EXTENSIONS = {".md", ".txt", ".csv", ".pdf", ".docx"}


def compute_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def _extract_pdf(path: Path) -> str | None:
    """Extract text from a PDF using PyMuPDF."""
    try:
        import fitz
        doc = fitz.open(str(path))
        pages = []
        for page in doc:
            text = page.get_text()
            if text.strip():
                pages.append(text)
        doc.close()
        return "\n\n".join(pages) if pages else None
    except Exception:
        return None


def _extract_docx(path: Path) -> str | None:
    """Extract text from a .docx file using python-docx."""
    try:
        from docx import Document
        doc = Document(str(path))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs) if paragraphs else None
    except Exception:
        return None


def load_text_file(path: Path) -> str | None:
    """Load a text file, return None for binary/unreadable."""
    ext = path.suffix.lower()
    if ext not in READABLE_EXTENSIONS:
        return None
    try:
        if ext == ".pdf":
            return _extract_pdf(path)
        if ext == ".docx":
            return _extract_docx(path)
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None


def scan_directory(base: Path) -> list[dict]:
    """Recursively scan a directory and return metadata + content for each readable file."""
    entries = []
    if not base.exists():
        return entries
    for fpath in sorted(base.rglob("*")):
        if fpath.is_dir():
            continue
        content = load_text_file(fpath)
        rel = fpath.relative_to(PROJECT_ROOT)
        entry = {
            "path": str(rel),
            "filename": fpath.name,
            "category": fpath.parent.name,
            "extension": fpath.suffix.lower(),
            "size_bytes": fpath.stat().st_size,
            "modified": datetime.fromtimestamp(fpath.stat().st_mtime).isoformat(),
            "readable": content is not None,
            "content_hash": compute_hash(content) if content else None,
        }
        if content is not None:
            entry["content"] = content
            entry["word_count"] = len(content.split())
        entries.append(entry)
    return entries


def build_corpus() -> dict:
    """Build the full corpus from knowledge_base + generated (feedback loop)."""
    corpus = {
        "built_at": datetime.now().isoformat(),
        "knowledge_base": scan_directory(KB_DIR),
        "generated": scan_directory(GEN_DIR),
    }
    corpus["total_files"] = len(corpus["knowledge_base"]) + len(corpus["generated"])
    corpus["total_readable"] = sum(
        1 for e in corpus["knowledge_base"] + corpus["generated"] if e["readable"]
    )
    return corpus


def save_index(corpus: dict):
    """Persist the corpus index (without full content) for auditing."""
    FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
    index_entries = []
    for e in corpus["knowledge_base"] + corpus["generated"]:
        idx = {k: v for k, v in e.items() if k != "content"}
        index_entries.append(idx)
    index = {
        "built_at": corpus["built_at"],
        "total_files": corpus["total_files"],
        "total_readable": corpus["total_readable"],
        "entries": index_entries,
    }
    INDEX_FILE.write_text(json.dumps(index, indent=2))
    return INDEX_FILE


def get_files_by_category(corpus: dict, category: str) -> list[dict]:
    """Filter corpus entries by category folder name."""
    all_entries = corpus["knowledge_base"] + corpus["generated"]
    return [e for e in all_entries if e["category"] == category and e["readable"]]


def get_recognitions_text(corpus: dict) -> str:
    """Concatenate all recognition content for use by generators."""
    entries = get_files_by_category(corpus, "recognitions")
    return "\n\n---\n\n".join(e["content"] for e in entries if "content" in e)


def get_training_text(corpus: dict) -> str:
    """Concatenate all training content."""
    entries = get_files_by_category(corpus, "training")
    return "\n\n---\n\n".join(e["content"] for e in entries if "content" in e)


def get_carmax_reference_text(corpus: dict) -> str:
    """Concatenate all CarMax reference material."""
    entries = get_files_by_category(corpus, "carmax_reference")
    return "\n\n---\n\n".join(e["content"] for e in entries if "content" in e)


def get_personal_records_text(corpus: dict) -> str:
    """Concatenate personal performance records."""
    entries = get_files_by_category(corpus, "personal_records")
    return "\n\n---\n\n".join(e["content"] for e in entries if "content" in e)


def get_vocabulary_guide(corpus: dict) -> str:
    """Extract the CarMax Vocabulary & Philosophy guide specifically."""
    all_entries = corpus["knowledge_base"] + corpus["generated"]
    for e in all_entries:
        if "vocabulary" in e["filename"].lower() and e.get("content"):
            return e["content"]
    return ""


if __name__ == "__main__":
    print("Building CarMax IDP corpus...")
    corpus = build_corpus()
    idx_path = save_index(corpus)
    print(f"Total files: {corpus['total_files']}")
    print(f"Readable files: {corpus['total_readable']}")
    print(f"Index saved to: {idx_path}")

    # Summary by category
    cats = {}
    for e in corpus["knowledge_base"] + corpus["generated"]:
        cat = e["category"]
        cats[cat] = cats.get(cat, 0) + 1
    print("\nFiles by category:")
    for cat, count in sorted(cats.items()):
        print(f"  {cat}: {count}")
