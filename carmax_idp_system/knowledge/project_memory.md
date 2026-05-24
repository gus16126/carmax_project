# CarMax Manager Agent — Project Memory

> Quick-context inject for AI assistants. Read this first before working on the project.
> Last updated: 2026-05-23

---

## Project at a Glance

| Field | Value |
|-------|-------|
| **Root** | `C:\Users\trans\Documents\carmax_project\` |
| **System dir** | `carmax_idp_system/` |
| **CLI entry point** | `carmax_idp_system/tools/carmax_cli.py` |
| **Workdir for CLI** | `C:\Users\trans\Documents\carmax_project\carmax_idp_system\tools\` |
| **Hermes skill** | `carmax-manager` (at `~/.hermes/skills/productivity/carmax-manager/`) |
| **Persona file** | `AGENTS.md` (project root) |

---

## Owner: Gustavo Felipe Guallar

- Associate ID: 280305
- Role: Home Delivery Driver / Fleet Driver — CarMax Logistics (since June 2022)
- Career target: Logistics Coordinator (6-12 mo) → Logistics Manager (2-3 yr) → Senior Manager/Regional Lead (4-5 yr)
- Strength: Results Focus (95% Executed Efficiency, 2.75 cars/week, Perfect Wheels & Bows score)
- Development area: Analysis & Decision Making
- 2025 APR: Business Objectives Exceptional / Competency Successful
- Key artifacts: QuiXspinz 2.0 article, 500-point Pre-Trip Checklist, 101+ recognitions, 4+ peer trainings
- Location: Miami, FL (US/Eastern)

---

## System Capabilities

| Command | What it generates |
|---------|-------------------|
| `python carmax_cli.py recognition --to "Name" --value "..." --reason "..."` | Achievers recognition |
| `python carmax_cli.py training --subject "..." --audience "..."` | Training communication |
| `python carmax_cli.py idp --period "Q2 2026" --target-role "..."` | IDP report |
| `python carmax_cli.py communication --type huddle\|safety_alert\|team_email\|management_update --topic "..."` | Leadership comm |
| `python carmax_cli.py status` | System health check |
| `python carmax_cli.py index` | Rebuild corpus index |

**Values:** Win Together | Put People First | Go For Greatness | Do The Right Thing

---

## Knowledge Base (151 files, 80 readable)

| Category | Contents |
|----------|----------|
| `carmax_reference/` (41) | CarMax policies, DOT CFR parts (49 CFR 376-399), vocabulary, Code of Conduct, Cottrell manual, tow guides, Role Guide |
| `personal_records/` (11) | APR, self-evaluations, manager evaluations, leadership notes, functional observation, BOL paperwork |
| `recognitions/` (6) | Achievers given/received — 101+ recognitions |
| `training/` (7 + subdirs) | Peer logs (Ben, Santiago, Benaiah), checklists, articles, pre-trip media (73 images) |
| `assessments/` (5) | Harver Assessment, MDP Assessment, self-evaluation |
| `generated/` (4) | Prior outputs — auto-fed back into system |

---

## Key Files

| File | Purpose |
|------|---------|
| `AGENTS.md` | AI persona — load this to become the CarMax Manager Agent |
| `carmax_idp_system/docs/identity.md` | Institutional identity (predecessor to AGENTS.md) |
| `carmax_idp_system/docs/Prompt - Expert CarMax Manager & IDP Coach.md` | Full coaching prompt |
| `carmax_idp_system/docs/Personal Sub‑Prompt for Gustavo.md` | Gustavo-specific coaching instructions |
| `carmax_idp_system/docs/MANIFEST.md` | Verified file index & audit log |
| `carmax_idp_system/docs/Control Tower (Instructions Charter).md` | Governance & audit framework |
| `carmax_idp_system/tools/knowledge_loader.py` | Corpus scanner — now reads .md, .txt, .csv, .pdf, .docx |
| `carmax_idp_system/tools/feedback_loop.py` | Generation log — every output becomes future input |

---

## Communication Standards

- **5-Step Structure:** Greeting → Purpose → Key Points → Value Connection → Positive Close
- **SBI-R Feedback:** Situation, Behavior, Impact, Recommendation
- **STAR + Reflection:** Situation, Task, Action, Result, Reflection
- **Tone:** Calm, clear, positive, constructive — formal but approachable
- **Language:** CarMax-native, inclusive (we/our/team), values-aligned

---

## Recent Changes (2026-05-23)

- Added PDF and DOCX text extraction to knowledge_loader (PyMuPDF + python-docx)
- Readable files jumped from 35 → 80
- Added 6 new files to knowledge base (self evaluation, functional observation, BOL, role guide, pretrip log, training images)
- All scattered root files consolidated into knowledge_base

---

## Guardrails

- IDP is development, NOT punitive
- No shortcuts that undermine safety/values/integrity
- Autocratic leadership ONLY for safety crises — default is collaborative
- Always use CarMax vocabulary before generic corporate language
- Anchor on behaviors and evidence, not tenure
