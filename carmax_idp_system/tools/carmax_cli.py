#!/usr/bin/env python3
"""
CarMax IDP Manager — Master CLI
Single entry point for all document generation and system management.

Usage:
    python carmax_cli.py recognition --to "Name" --value "Win Together" --reason "helped with route"
    python carmax_cli.py training --subject "Pre-Trip Refresher" --audience "All Drivers"
    python carmax_cli.py idp --period "Q2 2026" --target-role "Logistics Coordinator"
    python carmax_cli.py communication --type huddle --topic "Safety Review"
    python carmax_cli.py status
    python carmax_cli.py index
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def cmd_recognition(args):
    from generate_recognition import generate_recognition
    generate_recognition(args.to, args.value, args.reason, args.from_name, args.style)


def cmd_training(args):
    from generate_training_text import generate_training_text
    generate_training_text(args.subject, args.audience, args.series, args.from_name)


def cmd_idp(args):
    from generate_idp_report import generate_idp_report
    generate_idp_report(args.period, args.target_role, args.focus)


def cmd_communication(args):
    from generate_communication import generate_communication
    generate_communication(args.type, args.topic, args.from_name, args.audience)


def cmd_status(args):
    from feedback_loop import get_generation_stats, list_generated
    from knowledge_loader import build_corpus

    corpus = build_corpus()
    stats = get_generation_stats()

    print("=" * 60)
    print("  CarMax IDP Manager — System Status")
    print("=" * 60)
    print(f"\n📚 Knowledge Base:")
    print(f"   Total files: {len(corpus['knowledge_base'])}")
    print(f"   Readable:    {sum(1 for e in corpus['knowledge_base'] if e['readable'])}")

    cats = {}
    for e in corpus["knowledge_base"]:
        cat = e["category"]
        cats[cat] = cats.get(cat, 0) + 1
    for cat, count in sorted(cats.items()):
        print(f"     → {cat}: {count}")

    print(f"\n📝 Generated Documents:")
    print(f"   Total: {stats['total_generated']}")
    if stats["by_type"]:
        for t, c in sorted(stats["by_type"].items()):
            print(f"     → {t}: {c}")

    print(f"\n🔄 Feedback Loop:")
    gen_files = len(corpus["generated"])
    print(f"   Generated files in corpus: {gen_files}")
    print(f"   All generated content is automatically available as source material.")
    print()


def cmd_index(args):
    from knowledge_loader import build_corpus, save_index
    corpus = build_corpus()
    idx_path = save_index(corpus)
    print(f"Corpus index rebuilt: {idx_path}")
    print(f"Total files indexed: {corpus['total_files']}")


def main():
    parser = argparse.ArgumentParser(
        description="CarMax IDP Manager — Document Generation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python carmax_cli.py recognition --to "Santiago" --value "Win Together" --reason "helped with delivery"
  python carmax_cli.py training --subject "DOT Compliance" --audience "All Drivers"
  python carmax_cli.py idp --period "Q2 2026" --target-role "Logistics Coordinator"
  python carmax_cli.py communication --type huddle --topic "Morning Safety Brief"
  python carmax_cli.py status
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Recognition
    p_rec = subparsers.add_parser("recognition", help="Generate a recognition message")
    p_rec.add_argument("--to", required=True)
    p_rec.add_argument("--value", required=True, choices=["Win Together", "Put People First", "Go For Greatness", "Do The Right Thing"])
    p_rec.add_argument("--reason", required=True)
    p_rec.add_argument("--from-name", default="Gustavo Guallar")
    p_rec.add_argument("--style", default="standard", choices=["standard", "formal", "brief"])
    p_rec.set_defaults(func=cmd_recognition)

    # Training
    p_train = subparsers.add_parser("training", help="Generate a training communication")
    p_train.add_argument("--subject", required=True)
    p_train.add_argument("--audience", default="All Drivers")
    p_train.add_argument("--series", default="Operational Excellence")
    p_train.add_argument("--from-name", default="Gustavo Guallar")
    p_train.set_defaults(func=cmd_training)

    # IDP Report
    p_idp = subparsers.add_parser("idp", help="Generate an IDP report")
    p_idp.add_argument("--period", default="Q2 2026")
    p_idp.add_argument("--target-role", default="Logistics Coordinator")
    p_idp.add_argument("--focus", default="comprehensive", choices=["comprehensive", "competencies", "goals", "evidence"])
    p_idp.set_defaults(func=cmd_idp)

    # Communication
    p_comm = subparsers.add_parser("communication", help="Generate a leadership communication")
    p_comm.add_argument("--type", required=True, choices=["huddle", "safety_alert", "team_email", "management_update"])
    p_comm.add_argument("--topic", required=True)
    p_comm.add_argument("--from-name", default="Gustavo Guallar")
    p_comm.add_argument("--audience", default="CarMax Logistics Team")
    p_comm.set_defaults(func=cmd_communication)

    # Status
    p_status = subparsers.add_parser("status", help="Show system status and statistics")
    p_status.set_defaults(func=cmd_status)

    # Index
    p_index = subparsers.add_parser("index", help="Rebuild the corpus index")
    p_index.set_defaults(func=cmd_index)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
