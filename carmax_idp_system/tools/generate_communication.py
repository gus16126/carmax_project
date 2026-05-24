#!/usr/bin/env python3
"""
CarMax IDP System — Communication Generator
Generates various leadership communications: huddle notes, safety alerts,
team emails, and management updates — all CarMax-aligned.

Usage:
    python generate_communication.py --type huddle --topic "Weekly Safety Review"
    python generate_communication.py --type safety_alert --topic "Tire Pressure Checks"
    python generate_communication.py --type team_email --topic "Q2 Goals Update"
"""

import argparse
import re
from pathlib import Path
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from knowledge_loader import build_corpus, get_vocabulary_guide
from feedback_loop import register_generated_file

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "generated" / "communications"

COMM_TYPES = {
    "huddle": {
        "title": "Team Huddle Notes",
        "structure": ["Opening & Energy Check", "Key Topic", "Action Items", "Value Spotlight", "Close"],
    },
    "safety_alert": {
        "title": "Safety Alert",
        "structure": ["Alert Level", "Issue Description", "Required Actions", "Reference", "Follow-Up"],
    },
    "team_email": {
        "title": "Team Communication",
        "structure": ["Greeting", "Purpose", "Key Points", "Value Connection", "Positive Close"],
    },
    "management_update": {
        "title": "Management Update",
        "structure": ["Summary", "Key Metrics", "Challenges", "Wins", "Next Steps"],
    },
}


def generate_communication(
    comm_type: str,
    topic: str,
    from_name: str = "Gustavo Guallar",
    audience: str = "CarMax Logistics Team",
) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    corpus = build_corpus()
    vocab = get_vocabulary_guide(corpus)

    config = COMM_TYPES.get(comm_type, COMM_TYPES["team_email"])
    date_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H:%M")

    content = f"# {config['title']}\n\n"
    content += f"**Date:** {date_str}  \n"
    content += f"**Time:** {time_str}  \n"
    content += f"**From:** {from_name}, CarMax Logistics Team  \n"
    content += f"**To:** {audience}  \n"
    content += f"**Subject:** {topic}  \n\n---\n\n"

    if comm_type == "huddle":
        content += "## Opening & Energy Check\n"
        content += f"Good morning, team! Let's start today's huddle focused on **{topic}**.\n\n"
        content += "## Key Topic\n"
        content += f"Today we're covering **{topic}**. This is important because it directly impacts our safety, efficiency, and the Iconic Experience we deliver every day.\n\n"
        content += "### Discussion Points\n"
        content += f"- Review current status of {topic.lower()}\n"
        content += "- Share any observations or concerns from the field\n"
        content += "- Identify one thing we can improve this week\n\n"
        content += "## Action Items\n"
        content += f"- [ ] Each driver: Review {topic.lower()} procedures before next shift\n"
        content += "- [ ] Team lead: Follow up on any reported issues within 24 hours\n"
        content += "- [ ] All: Share best practices or tips with the group\n\n"
        content += "## Value Spotlight: Win Together\n"
        content += "Remember — we succeed through collaboration and open communication. "
        content += "If you see something, say something. If you know something, share it. "
        content += "That's how we Win Together.\n\n"
        content += "## Close\n"
        content += "Thanks for your attention and commitment. Let's make today a great one — safely and together.\n"

    elif comm_type == "safety_alert":
        content += "## ⚠️ Alert Level: IMPORTANT\n\n"
        content += f"## Issue: {topic}\n\n"
        content += f"This safety alert addresses **{topic}**. All drivers must review this information "
        content += "and take the required actions before their next shift.\n\n"
        content += "## Required Actions\n"
        content += f"1. Review the standard procedure for {topic.lower()}\n"
        content += "2. Complete a visual inspection related to this item during your next pre-trip\n"
        content += "3. Report any deficiencies immediately to your supervisor\n"
        content += "4. Document compliance in your daily log\n\n"
        content += "## Reference\n"
        content += "Refer to the Pre-Trip Inspection Checklist and DOT compliance guidelines in the knowledge base.\n\n"
        content += "## Value Connection: Do The Right Thing\n"
        content += "Safety isn't optional — it's how we protect ourselves, our team, and the customers who trust us. "
        content += "Doing the Right Thing means following proper procedures every single time, even when no one is watching.\n\n"
        content += "## Follow-Up\n"
        content += "Your supervisor will verify compliance during the next shift review. "
        content += "If you have questions, reach out immediately — we're here to support you.\n"

    elif comm_type == "management_update":
        content += f"## Summary\n"
        content += f"This update covers the current status of **{topic}** and key items requiring attention.\n\n"
        content += "## Key Metrics\n"
        content += "- Executed Efficiency: Tracking to target\n"
        content += "- Safety Incidents: Zero reportable incidents\n"
        content += "- Customer Satisfaction: Maintaining high scores\n\n"
        content += "## Wins\n"
        content += f"- Team continues to demonstrate strong execution on {topic.lower()}\n"
        content += "- Peer training program expanding with positive feedback\n"
        content += "- Cross-departmental relationships strengthening\n\n"
        content += "## Challenges\n"
        content += "- [Document specific challenges related to the topic]\n\n"
        content += "## Next Steps\n"
        content += "- Continue monitoring key metrics\n"
        content += "- Schedule follow-up review in 2 weeks\n"
        content += f"- Update team on any changes to {topic.lower()} procedures\n"

    else:  # team_email
        content += f"Good morning team,\n\n"
        content += f"I'm writing today about **{topic}**. "
        content += "This is part of our ongoing commitment to operational excellence and continuous improvement.\n\n"
        content += "## Key Points\n"
        content += f"- {topic} directly affects our daily operations and customer experience\n"
        content += "- Consistency in following established procedures is critical\n"
        content += "- We all have a role in making this work — let's stay aligned as a team\n\n"
        content += "## Value Connection: Win Together\n"
        content += "We succeed through collaboration and open communication. "
        content += "By staying consistent with the process, we protect each other and deliver the Iconic Experience our customers expect.\n\n"
        content += "Thanks again for your attention and teamwork. Please reach out if you need support.\n"

    content += f"\n---\n\n— {from_name}, CarMax Logistics Team\n"
    content += f"\n*Generated by CarMax IDP Manager System on {date_str}*\n"

    safe_topic = re.sub(r'[^a-zA-Z0-9]', '_', topic.lower())[:50]
    filename = f"{comm_type}_{safe_topic}_{date_str}.md"
    output_path = OUTPUT_DIR / filename
    output_path.write_text(content)

    register_generated_file(
        filepath=output_path,
        doc_type="communication",
        description=f"{config['title']}: {topic}",
        source_files=[],
        metadata={"type": comm_type, "topic": topic, "audience": audience},
    )

    print(f"\n✅ Communication generated: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate CarMax leadership communications")
    parser.add_argument("--type", required=True, choices=list(COMM_TYPES.keys()))
    parser.add_argument("--topic", required=True, help="Communication topic")
    parser.add_argument("--from-name", default="Gustavo Guallar")
    parser.add_argument("--audience", default="CarMax Logistics Team")
    args = parser.parse_args()
    generate_communication(args.type, args.topic, args.from_name, args.audience)


if __name__ == "__main__":
    main()
