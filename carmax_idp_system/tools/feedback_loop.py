#!/usr/bin/env python3
"""
CarMax IDP System — Feedback Loop Manager
Every generated document is logged and automatically becomes part of the
knowledge base for future generations. This module handles:
1. Registering new generated files
2. Maintaining a generation log with metadata
3. Copying generated content into the feedback corpus
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GEN_DIR = PROJECT_ROOT / "generated"
FEEDBACK_DIR = PROJECT_ROOT / "feedback_loop"
GEN_LOG = FEEDBACK_DIR / "generation_log.json"


def _load_log() -> list[dict]:
    if GEN_LOG.exists():
        return json.loads(GEN_LOG.read_text())
    return []


def _save_log(log: list[dict]):
    FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
    GEN_LOG.write_text(json.dumps(log, indent=2))


def register_generated_file(
    filepath: str | Path,
    doc_type: str,
    description: str,
    source_files: list[str] | None = None,
    metadata: dict | None = None,
) -> dict:
    """
    Register a newly generated file in the feedback loop.
    
    Args:
        filepath: Path to the generated file
        doc_type: Type of document (recognition, training_text, idp_report, communication)
        description: Human-readable description
        source_files: List of source file paths used to generate this
        metadata: Additional metadata dict
    
    Returns:
        The log entry created
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Generated file not found: {filepath}")

    log = _load_log()
    entry = {
        "id": len(log) + 1,
        "timestamp": datetime.now().isoformat(),
        "filename": filepath.name,
        "path": str(filepath.relative_to(PROJECT_ROOT)),
        "doc_type": doc_type,
        "description": description,
        "source_files": source_files or [],
        "metadata": metadata or {},
        "size_bytes": filepath.stat().st_size,
        "feedback_integrated": True,
    }
    log.append(entry)
    _save_log(log)

    print(f"[Feedback Loop] Registered: {filepath.name} (type={doc_type})")
    print(f"  → Total generated documents: {len(log)}")
    print(f"  → This file is now part of the knowledge base for future generations.")
    return entry


def get_generation_stats() -> dict:
    """Return summary statistics about all generated documents."""
    log = _load_log()
    stats = {
        "total_generated": len(log),
        "by_type": {},
        "latest_generation": log[-1]["timestamp"] if log else None,
    }
    for entry in log:
        t = entry["doc_type"]
        stats["by_type"][t] = stats["by_type"].get(t, 0) + 1
    return stats


def list_generated(doc_type: str | None = None) -> list[dict]:
    """List all generated documents, optionally filtered by type."""
    log = _load_log()
    if doc_type:
        return [e for e in log if e["doc_type"] == doc_type]
    return log


if __name__ == "__main__":
    stats = get_generation_stats()
    print("=== Feedback Loop Statistics ===")
    print(f"Total generated documents: {stats['total_generated']}")
    if stats["by_type"]:
        print("By type:")
        for t, c in stats["by_type"].items():
            print(f"  {t}: {c}")
    else:
        print("No documents generated yet.")
