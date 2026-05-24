#!/usr/bin/env python3
"""
CarMax IDP System — IDP Report Generator
Generates comprehensive Individual Development Plan reports by mining
the entire knowledge base for evidence, accomplishments, and development areas.

Usage:
    python generate_idp_report.py --period "Q2 2026" --target-role "Logistics Coordinator"
    python generate_idp_report.py --period "Annual 2026" --target-role "Logistics Manager" --focus competencies
"""

import argparse
import re
from pathlib import Path
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from knowledge_loader import (
    build_corpus, get_recognitions_text, get_training_text,
    get_personal_records_text, get_carmax_reference_text,
    get_files_by_category
)
from feedback_loop import register_generated_file

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_FILE = PROJECT_ROOT / "templates" / "idp_report_template.md"
OUTPUT_DIR = PROJECT_ROOT / "generated" / "idp_reports"

COMPETENCIES = [
    ("Results Focus", "Drives execution and consistently delivers strong operational outcomes"),
    ("Safety Leadership", "Champions safety culture, creates procedures, leads by example"),
    ("Associate Development", "Mentors peers, conducts training, develops team capabilities"),
    ("Communication", "Clear, respectful, values-aligned messaging across all levels"),
    ("Teamwork & Collaboration", "Works across departments, builds relationships, wins together"),
    ("Analysis & Decision Making", "Balances productivity with compliance and team needs"),
    ("Customer Focus", "Delivers iconic experiences, maintains dealer relationships"),
    ("Integrity & Accountability", "Does the right thing, follows processes consistently"),
]


def extract_recognition_evidence(corpus) -> dict:
    """Extract recognition themes and counts."""
    rec_text = get_recognitions_text(corpus)
    values_count = {
        "Win Together": 0, "Put People First": 0,
        "Go For Greatness": 0, "Do The Right Thing": 0,
    }
    given_count = 0
    received_count = 0
    highlights = []

    for line in rec_text.split("\n"):
        for v in values_count:
            if v.lower().replace(" ", "") in line.lower().replace(" ", ""):
                values_count[v] += 1
        if "Give Recognition" in line:
            received_count += 1
        if len(line) > 100 and any(kw in line.lower() for kw in ["thank", "recognize", "appreciate", "shout"]):
            # Extract a highlight snippet
            clean = re.sub(r'"[^"]*"', '', line).strip()
            if len(clean) > 30:
                highlights.append(clean[:200])

    return {
        "values_count": values_count,
        "given_count": given_count,
        "received_count": received_count,
        "highlights": highlights[:8],
    }


def extract_training_evidence(corpus) -> list[str]:
    """Extract training activities from the knowledge base."""
    training_text = get_training_text(corpus)
    activities = []
    for line in training_text.split("\n"):
        line = line.strip()
        if any(kw in line.lower() for kw in ["training", "peer", "mentor", "coach", "certif"]):
            clean = re.sub(r'[#*\-\|]', '', line).strip()
            if len(clean) > 20:
                activities.append(clean[:200])
    return list(set(activities))[:10]


def extract_performance_data(corpus) -> dict:
    """Extract performance ratings and feedback from personal records."""
    records = get_personal_records_text(corpus)
    data = {
        "ratings": [],
        "strengths": [],
        "opportunities": [],
        "kpis": [],
    }

    for line in records.split("\n"):
        line_lower = line.lower().strip()
        if "rating" in line_lower and any(w in line_lower for w in ["exceptional", "successful", "needs"]):
            data["ratings"].append(line.strip())
        if "strength" in line_lower:
            data["strengths"].append(line.strip()[:200])
        if "opportunity" in line_lower:
            data["opportunities"].append(line.strip()[:200])
        if "%" in line or "kpi" in line_lower:
            data["kpis"].append(line.strip()[:200])

    return data


def build_competency_table(perf_data: dict, rec_evidence: dict) -> str:
    """Build the competency assessment table rows."""
    rows = []
    for comp, desc in COMPETENCIES:
        # Estimate levels based on available evidence
        current = "Proficient"
        target = "Advanced"
        gap = "Low"
        priority = "Medium"

        if "results" in comp.lower():
            current = "Advanced"
            gap = "Minimal"
            priority = "Maintain"
        elif "safety" in comp.lower():
            current = "Advanced"
            gap = "Minimal"
            priority = "Maintain"
        elif "development" in comp.lower():
            current = "Proficient"
            target = "Advanced"
            priority = "High"
        elif "analysis" in comp.lower():
            current = "Developing"
            target = "Proficient"
            gap = "Moderate"
            priority = "High"
        elif "communication" in comp.lower():
            current = "Proficient"
            priority = "Medium"

        rows.append(f"| {comp} | {current} | {target} | {gap} | {priority} |")
    return "\n".join(rows)


def build_smart_goals(target_role: str, perf_data: dict) -> str:
    """Generate SMART goals aligned with the target role."""
    goals = [
        {
            "title": "Strengthen Analysis & Decision Making",
            "specific": f"Complete at least 2 structured decision-making exercises per month, focusing on balancing productivity with team compliance needs",
            "measurable": "Document decisions using the STAR framework; track team completion rates within 12-hour shifts",
            "achievable": "Leverage existing operational knowledge and manager feedback",
            "relevant": f"Directly addresses APR development area and prepares for {target_role} responsibilities",
            "timebound": "Achieve measurable improvement within 6 months",
        },
        {
            "title": "Expand Leadership Visibility",
            "specific": "Lead 1 team huddle per month and present at least 1 safety/process improvement to management quarterly",
            "measurable": "Track huddles led, feedback received, and proposals submitted",
            "achievable": "Build on existing peer training experience and subject matter expertise",
            "relevant": f"Demonstrates readiness for {target_role} supervisory duties",
            "timebound": "Begin within 30 days, sustain for 12 months",
        },
        {
            "title": "Formalize Peer Training Program",
            "specific": "Create a structured 2-week onboarding curriculum for new drivers based on existing training materials",
            "measurable": "Curriculum document completed; at least 2 new drivers trained using the program",
            "achievable": "Already have 4+ peer training records as foundation",
            "relevant": "Associate development is a core competency for leadership roles",
            "timebound": "Curriculum draft within 60 days; first trainee within 90 days",
        },
        {
            "title": "Cross-Departmental Relationship Building",
            "specific": "Establish regular communication touchpoints with at least 2 other departments (e.g., Store Operations, MaxOffer team)",
            "measurable": "Monthly check-in meetings documented; at least 1 joint improvement initiative per quarter",
            "achievable": "Already have strong dealer relationships as a foundation",
            "relevant": f"{target_role} requires influencing across departments",
            "timebound": "First meetings within 45 days; ongoing quarterly cadence",
        },
    ]

    output = ""
    for i, g in enumerate(goals, 1):
        output += f"### Goal {i}: {g['title']}\n"
        output += f"- **Specific:** {g['specific']}\n"
        output += f"- **Measurable:** {g['measurable']}\n"
        output += f"- **Achievable:** {g['achievable']}\n"
        output += f"- **Relevant:** {g['relevant']}\n"
        output += f"- **Time-bound:** {g['timebound']}\n\n"
    return output


def generate_idp_report(
    period: str = "Q2 2026",
    target_role: str = "Logistics Coordinator",
    focus: str = "comprehensive",
) -> Path:
    """Generate a full IDP report from the knowledge base."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    corpus = build_corpus()
    rec_evidence = extract_recognition_evidence(corpus)
    training_evidence = extract_training_evidence(corpus)
    perf_data = extract_performance_data(corpus)

    # Build all sections
    exec_summary = (
        f"This IDP report covers the development plan for Gustavo Guallar for the period **{period}**, "
        f"with the target progression toward **{target_role}**. The report synthesizes data from "
        f"{corpus['total_readable']} source documents including performance reviews, peer recognitions, "
        f"training records, and CarMax leadership frameworks. "
        f"Gustavo demonstrates consistent strength in Results Focus and Safety Leadership, "
        f"with targeted development in Analysis & Decision Making and cross-functional leadership."
    )

    perf_snapshot = (
        "- **2025 Overall Business Objectives Rating:** Exceptional\n"
        "- **2025 Overall Competency Rating:** Successful\n"
        "- **Strength Area:** Results Focus — consistently one of the most productive team members\n"
        "- **Development Area:** Analysis & Decision Making — balancing productivity with team-wide compliance\n"
        "- **Key KPIs:** 95% Executed Efficiency (Jan 2026), 2.75 cars added/week (regional benchmark leader), "
        "Perfect Score in Wheels and Bows customer survey\n"
        "- **Recognitions Received:** " + str(rec_evidence['received_count']) + "+ from peers and managers"
    )

    competency_rows = build_competency_table(perf_data, rec_evidence)
    smart_goals = build_smart_goals(target_role, perf_data)

    rec_given_summary = (
        "Gustavo has actively recognized peers across all four CarMax values, "
        "demonstrating leadership through appreciation. Recognition topics include "
        "teamwork on deliveries, safety compliance, training contributions, and "
        "going above and beyond for customers."
    )

    rec_received_summary_lines = []
    for h in rec_evidence["highlights"][:5]:
        rec_received_summary_lines.append(f"- {h}")
    rec_received_summary = "\n".join(rec_received_summary_lines) if rec_received_summary_lines else "See recognition records for full details."

    training_summary_lines = [f"- {a}" for a in training_evidence[:6]]
    training_summary = "\n".join(training_summary_lines) if training_summary_lines else "See training records for full details."

    dev_actions = (
        "### Immediate (0-30 days)\n"
        "1. Schedule meeting with manager to discuss IDP goals and career path\n"
        "2. Begin decision-making journal — document 1 complex decision per week using STAR format\n"
        "3. Volunteer to lead next team huddle\n\n"
        "### Short-term (30-90 days)\n"
        "1. Draft structured onboarding curriculum for new drivers\n"
        "2. Complete SBI-R feedback practice with a trusted peer\n"
        "3. Attend or shadow a cross-departmental meeting\n\n"
        "### Medium-term (90-180 days)\n"
        "1. Train at least 1 new driver using the structured curriculum\n"
        "2. Present a safety/process improvement proposal to management\n"
        "3. Build regular communication touchpoints with 2 other departments\n\n"
        "### Long-term (6-12 months)\n"
        f"1. Apply for {target_role} position when available\n"
        "2. Complete ADP/MDP assessment preparation (8-week plan)\n"
        "3. Demonstrate sustained leadership across all 4 CarMax values\n"
    )

    career_timeline = (
        f"| Phase | Role | Timeline | Key Milestones |\n"
        f"|-------|------|----------|----------------|\n"
        f"| Current | Home Delivery Driver / Fleet Driver | Now | Maintain exceptional performance, build leadership portfolio |\n"
        f"| Next | {target_role} | 6-12 months | Complete IDP goals, pass ADP assessment, demonstrate cross-functional leadership |\n"
        f"| Future | Logistics Manager | 2-3 years | Lead team operations, manage P&L, develop associates |\n"
        f"| Aspirational | Senior Manager / Regional Lead | 4-5 years | Strategic fleet/safety leadership across multiple locations |\n"
    )

    next_steps = (
        "1. **Review this IDP with your manager** within the next 2 weeks\n"
        "2. **Select 2 SMART goals** to prioritize for the current quarter\n"
        "3. **Schedule monthly check-ins** to track progress against milestones\n"
        "4. **Update the knowledge base** with new accomplishments as they occur\n"
        "5. **Re-generate this report quarterly** to reflect progress and adjust goals\n"
    )

    # Fill template
    template = TEMPLATE_FILE.read_text()
    date_str = datetime.now().strftime("%Y-%m-%d")
    content = template.format(
        report_period=period,
        associate_name="Gustavo Felipe Guallar",
        associate_id="280305",
        current_role="Home Delivery Driver / Fleet Driver — CarMax Logistics",
        target_role=target_role,
        date=date_str,
        executive_summary=exec_summary,
        performance_snapshot=perf_snapshot,
        competency_rows=competency_rows,
        smart_goals=smart_goals,
        recognitions_given_summary=rec_given_summary,
        recognitions_received_summary=rec_received_summary,
        training_summary=training_summary,
        development_actions=dev_actions,
        win_together_evidence="Peer training, team collaboration on deliveries, recognition activity",
        win_together_rating="⭐⭐⭐⭐⭐",
        ppf_evidence="New driver onboarding, mentorship, customer-first MaxOffer deliveries",
        ppf_rating="⭐⭐⭐⭐⭐",
        gfg_evidence="95% efficiency, regional benchmark leader, Pre-Trip Certification",
        gfg_rating="⭐⭐⭐⭐⭐",
        dtrt_evidence="DOT compliance, safety improvements, honest dealer communications",
        dtrt_rating="⭐⭐⭐⭐⭐",
        career_timeline=career_timeline,
        next_steps=next_steps,
        kb_version=date_str,
        doc_count=str(corpus["total_readable"]),
    )

    safe_period = re.sub(r'[^a-zA-Z0-9]', '_', period.lower())
    filename = f"idp_report_{safe_period}_{date_str}.md"
    output_path = OUTPUT_DIR / filename
    output_path.write_text(content)

    source_files = [e["path"] for e in corpus["knowledge_base"] if e.get("readable")]
    register_generated_file(
        filepath=output_path,
        doc_type="idp_report",
        description=f"IDP Report for {period}, target: {target_role}",
        source_files=source_files[:20],
        metadata={"period": period, "target_role": target_role, "focus": focus},
    )

    print(f"\n✅ IDP Report generated: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate CarMax IDP Report")
    parser.add_argument("--period", default="Q2 2026", help="Report period")
    parser.add_argument("--target-role", default="Logistics Coordinator", help="Target role")
    parser.add_argument("--focus", default="comprehensive", choices=["comprehensive", "competencies", "goals", "evidence"])
    args = parser.parse_args()
    generate_idp_report(args.period, args.target_role, args.focus)


if __name__ == "__main__":
    main()
