#!/usr/bin/env python3
"""
CarMax IDP System — Training Text Generator
Generates CarMax-aligned training communications based on the knowledge base.

Usage:
    python generate_training_text.py --subject "Pre-Trip Inspection Refresher" --audience "All Drivers"
    python generate_training_text.py --subject "DOT Compliance Update" --audience "Fleet Team" --series "Safety First"
"""

import argparse
import re
import random
from pathlib import Path
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from knowledge_loader import (
    build_corpus, get_training_text, get_carmax_reference_text,
    get_vocabulary_guide, get_files_by_category
)
from feedback_loop import register_generated_file

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_FILE = PROJECT_ROOT / "templates" / "training_text_template.md"
OUTPUT_DIR = PROJECT_ROOT / "generated" / "training_texts"

TOPIC_KEYWORDS = {
    "pre-trip": ["inspection", "checklist", "safety", "DOT", "ELD", "air brake", "tire", "lights"],
    "dot": ["compliance", "regulations", "weigh station", "CDL", "hours of service", "logbook"],
    "delivery": ["MaxOffer", "customer", "dealership", "pickup", "BOL", "workflow"],
    "safety": ["tie-down", "securement", "QuiXspinz", "rollback", "winch", "deck loading"],
    "leadership": ["teamwork", "mentorship", "coaching", "feedback", "development"],
    "app": ["UKG", "My20", "CarMax Driver App", "ELD", "timekeeping"],
}

VALUE_CONNECTIONS = {
    "safety": "**Do The Right Thing** — Safety isn't optional. Following proper procedures protects our team, our equipment, and the customers who trust us.",
    "compliance": "**Do The Right Thing** — Maintaining DOT compliance is how we demonstrate accountability and protect CarMax's reputation.",
    "teamwork": "**Win Together** — When we share knowledge and support each other, the whole team rises.",
    "training": "**Put People First** — Investing in our people through training creates growth opportunities and strengthens our team.",
    "excellence": "**Go For Greatness** — We don't settle. Every delivery, every inspection, every interaction is a chance to be the best.",
    "default": "**Win Together** — We succeed through collaboration, open communication, and shared purpose.",
}


def find_relevant_content(corpus, subject: str) -> list[str]:
    """Search the knowledge base for content relevant to the subject."""
    subject_lower = subject.lower()
    relevant = []

    all_entries = corpus["knowledge_base"] + corpus["generated"]
    for entry in all_entries:
        if not entry.get("content"):
            continue
        content = entry["content"]
        # Score relevance
        score = 0
        for topic, keywords in TOPIC_KEYWORDS.items():
            if topic in subject_lower:
                for kw in keywords:
                    if kw.lower() in content.lower():
                        score += 1
        # Also check direct subject word matches
        for word in subject_lower.split():
            if len(word) > 3 and word in content.lower():
                score += 1
        if score >= 2:
            # Extract relevant paragraphs
            for para in content.split("\n\n"):
                para = para.strip()
                if len(para) > 50:
                    for word in subject_lower.split():
                        if len(word) > 3 and word in para.lower():
                            relevant.append(para[:500])
                            break
    return relevant[:10]


def determine_value_connection(subject: str) -> str:
    """Pick the best CarMax value connection for the topic."""
    subject_lower = subject.lower()
    if any(w in subject_lower for w in ["safety", "inspection", "pre-trip", "tie-down"]):
        return VALUE_CONNECTIONS["safety"]
    elif any(w in subject_lower for w in ["dot", "compliance", "regulation", "cdl"]):
        return VALUE_CONNECTIONS["compliance"]
    elif any(w in subject_lower for w in ["team", "huddle", "collaboration"]):
        return VALUE_CONNECTIONS["teamwork"]
    elif any(w in subject_lower for w in ["training", "mentor", "coaching", "development"]):
        return VALUE_CONNECTIONS["training"]
    elif any(w in subject_lower for w in ["excellence", "greatness", "best", "improve"]):
        return VALUE_CONNECTIONS["excellence"]
    return VALUE_CONNECTIONS["default"]


def generate_key_points(subject: str, relevant_content: list[str]) -> str:
    """Generate 3-5 key points from relevant content and subject."""
    points = []

    # Extract bullet-worthy statements from relevant content
    for content in relevant_content[:5]:
        sentences = [s.strip() for s in content.split(".") if len(s.strip()) > 20]
        for s in sentences[:1]:
            clean = re.sub(r'[#*\-\|]', '', s).strip()
            if clean and len(clean) > 15:
                points.append(clean)

    # Ensure minimum points
    generic_points = [
        f"Review and follow the standard procedure for {subject.lower()}",
        "Document any questions or concerns and share with your supervisor",
        "Practice consistency — follow the same process every time",
        "Support your teammates by sharing what you learn",
        "Report any safety concerns or process issues immediately",
    ]
    while len(points) < 3:
        points.append(generic_points.pop(0))

    formatted = "\n".join(f"- {p}" for p in points[:5])
    return formatted


def generate_training_text(
    subject: str,
    audience: str = "All Drivers",
    series: str = "Operational Excellence",
    from_name: str = "Gustavo Guallar",
) -> Path:
    """Generate a complete training communication and register it."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    corpus = build_corpus()
    relevant = find_relevant_content(corpus, subject)

    purpose = (
        f"This communication is part of our **{series}** series. "
        f"Today we're focusing on **{subject}** — a critical part of our daily operations "
        f"that directly impacts safety, compliance, and customer experience."
    )

    key_points = generate_key_points(subject, relevant)
    value_conn = determine_value_connection(subject)

    closing = (
        f"Thank you for your attention and commitment to excellence. "
        f"If you have questions about {subject.lower()}, please don't hesitate to reach out. "
        f"Together, we're building something great."
    )

    template = TEMPLATE_FILE.read_text()
    date_str = datetime.now().strftime("%Y-%m-%d")
    content = template.format(
        date=date_str,
        subject=subject,
        from_name=from_name,
        audience=audience,
        series=series,
        purpose_statement=purpose,
        key_points=key_points,
        value_connection=value_conn,
        closing=closing,
    )

    safe_subject = re.sub(r'[^a-zA-Z0-9]', '_', subject.lower())[:50]
    filename = f"training_{safe_subject}_{date_str}.md"
    output_path = OUTPUT_DIR / filename
    output_path.write_text(content)

    source_files = [e["path"] for e in corpus["knowledge_base"] if e.get("readable")][:5]
    register_generated_file(
        filepath=output_path,
        doc_type="training_text",
        description=f"Training text: {subject} for {audience}",
        source_files=source_files,
        metadata={"subject": subject, "audience": audience, "series": series},
    )

    print(f"\n✅ Training text generated: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate CarMax training communications")
    parser.add_argument("--subject", required=True, help="Training subject/topic")
    parser.add_argument("--audience", default="All Drivers", help="Target audience")
    parser.add_argument("--series", default="Operational Excellence", help="Training series name")
    parser.add_argument("--from-name", default="Gustavo Guallar", help="Sender name")
    args = parser.parse_args()
    generate_training_text(args.subject, args.audience, args.series, args.from_name)


if __name__ == "__main__":
    main()
