#!/usr/bin/env python3
"""
CarMax IDP System — Recognition Generator
Generates CarMax-aligned recognition messages based on the knowledge base.

Usage:
    python generate_recognition.py --to "Name" --value "Win Together" --reason "helped with route"
    python generate_recognition.py --to "Name" --value "Put People First" --reason "trained new driver" --style formal
"""

import argparse
import json
import re
import random
from pathlib import Path
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from knowledge_loader import build_corpus, get_recognitions_text, get_vocabulary_guide
from feedback_loop import register_generated_file

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_FILE = PROJECT_ROOT / "templates" / "recognition_template.md"
OUTPUT_DIR = PROJECT_ROOT / "generated" / "recognitions"

CARMAX_VALUES = ["Win Together", "Put People First", "Go For Greatness", "Do The Right Thing"]

VALUE_LANGUAGE = {
    "Win Together": [
        "Success through collaboration and open communication",
        "Strengthening the team by embracing our differences",
        "Building trust through transparency",
        "We Win Together when everyone stays consistent with the process",
    ],
    "Put People First": [
        "Investing in associates and providing growth opportunities",
        "Having our customers' backs",
        "Supporting Diversity & Inclusion to create a sense of belonging",
        "Putting People First means making each delivery smooth and stress-free",
    ],
    "Go For Greatness": [
        "Executing for excellence and relentlessly innovating",
        "Driving what's possible as industry disruptors",
        "Let's Go For Greatness by learning something new this week",
        "Going above and beyond to deliver an Iconic Experience",
    ],
    "Do The Right Thing": [
        "Operating with honesty, ethics, and accountability",
        "Doing what's right, even when it's not easy",
        "Doing the Right Thing means following through, even when no one's watching",
        "Maintaining integrity and accuracy in everything we do",
    ],
}

OPENERS = [
    "I want to recognize {name} for",
    "Shout out to {name} for",
    "I'd like to acknowledge {name} for",
    "A well-deserved recognition for {name} for",
    "Thank you, {name}, for",
    "Appreciation for {name}!",
]

CLOSERS = [
    "Thanks for all you do.",
    "Your efforts are truly appreciated and make a real difference.",
    "We are grateful for this display of CarMax teamwork.",
    "Keep up the excellent work — it doesn't go unnoticed.",
    "Your contributions set a high standard for our entire team.",
    "Thank you for representing our team with professionalism and care.",
]


def extract_recognition_patterns(corpus) -> list[str]:
    """Mine real recognition patterns from existing data."""
    text = get_recognitions_text(corpus)
    # Extract the actual recognition body texts
    patterns = []
    for line in text.split("\n"):
        line = line.strip()
        if len(line) > 50 and not line.startswith('"20') and not line.startswith("---"):
            # Grab phrases that look like recognition language
            if any(kw in line.lower() for kw in ["thank", "appreciate", "recognize", "shout", "great job", "stepping"]):
                patterns.append(line)
    return patterns


def generate_recognition_body(
    to_name: str,
    value: str,
    reason: str,
    style: str = "standard",
    corpus=None,
) -> str:
    """Generate the body text for a recognition message."""
    opener = random.choice(OPENERS).format(name=to_name)
    value_phrase = random.choice(VALUE_LANGUAGE.get(value, VALUE_LANGUAGE["Win Together"]))
    closer = random.choice(CLOSERS)

    if style == "formal":
        body = (
            f"{opener} {reason}. "
            f"This reflects our core value of **{value}** — {value_phrase.lower()}. "
            f"{to_name}'s actions demonstrate the kind of leadership and commitment "
            f"that makes our CarMax Logistics team exceptional. {closer}"
        )
    elif style == "brief":
        body = f"{opener} {reason}. {closer}"
    else:
        body = (
            f"{opener} {reason}. "
            f"This is a great example of **{value}** in action. "
            f"{value_phrase}. {closer}"
        )

    return body


def generate_recognition(
    to_name: str,
    value: str,
    reason: str,
    from_name: str = "Gustavo Guallar",
    style: str = "standard",
) -> Path:
    """Generate a complete recognition document and register it in the feedback loop."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    corpus = build_corpus()
    body = generate_recognition_body(to_name, value, reason, style, corpus)

    template = TEMPLATE_FILE.read_text()
    date_str = datetime.now().strftime("%Y-%m-%d")
    content = template.format(
        date=date_str,
        from_name=from_name,
        to_name=to_name,
        value=value,
        body=body,
    )

    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', to_name.lower())
    filename = f"recognition_{safe_name}_{date_str}.md"
    output_path = OUTPUT_DIR / filename
    output_path.write_text(content)

    register_generated_file(
        filepath=output_path,
        doc_type="recognition",
        description=f"Recognition for {to_name} — {value}: {reason}",
        source_files=["templates/recognition_template.md"],
        metadata={"to": to_name, "from": from_name, "value": value, "style": style},
    )

    print(f"\n✅ Recognition generated: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate CarMax recognition messages")
    parser.add_argument("--to", required=True, help="Recipient name")
    parser.add_argument("--value", required=True, choices=CARMAX_VALUES, help="CarMax value")
    parser.add_argument("--reason", required=True, help="Reason for recognition")
    parser.add_argument("--from-name", default="Gustavo Guallar", help="Sender name")
    parser.add_argument("--style", default="standard", choices=["standard", "formal", "brief"])
    args = parser.parse_args()
    generate_recognition(args.to, args.value, args.reason, args.from_name, args.style)


if __name__ == "__main__":
    main()
