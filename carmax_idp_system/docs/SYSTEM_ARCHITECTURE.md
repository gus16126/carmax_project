# CarMax IDP Manager — System Architecture

**Owner:** Gustavo Felipe Guallar (Associate ID: 280305)  
**Version:** 2.0  
**Last Updated:** 2026-05-22

---

## 1. System Overview

The CarMax IDP Manager is an automated document generation and knowledge management system designed to support Gustavo Guallar's Individual Development Plan (IDP) progression within CarMax Logistics. It organizes all existing materials, generates new documents aligned with CarMax vocabulary and values, and implements a feedback loop where every generated document becomes source material for future generations.

```
┌─────────────────────────────────────────────────────────────┐
│                   CarMax IDP Manager System                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ Knowledge    │───▶│  Generators  │───▶│  Generated   │  │
│  │ Base (35+    │    │  (4 types)   │    │  Output      │  │
│  │ source files)│    │              │    │              │  │
│  └──────────────┘    └──────────────┘    └──────┬───────┘  │
│         ▲                                        │          │
│         │            ┌──────────────┐            │          │
│         └────────────│ Feedback     │◀───────────┘          │
│                      │ Loop         │                       │
│                      └──────────────┘                       │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ Templates    │    │  Master CLI  │    │  Corpus      │  │
│  │ (3 formats)  │    │  (entry pt.) │    │  Index       │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Directory Structure

```
carmax_idp_system/
│
├── knowledge_base/                  # All source materials (READ-ONLY originals)
│   ├── carmax_reference/            # CarMax corporate docs, policies, vocabulary
│   │   ├── CarMax Vocabulary & Philosophy.md    ← CORE: tone/language guide
│   │   ├── CarMax Master Leadership Binder.md   ← Leadership frameworks
│   │   ├── CarMax-What is the CarMax IDP.md     ← IDP program details
│   │   ├── CarMax Business Overview.md
│   │   ├── CarMax Code Of Business Conduct.md
│   │   ├── CarMax Benefits of creating an IDP.md
│   │   ├── CarMax Distinguishing Teams from Work Groups.md
│   │   ├── CarMax Human Capital Resources.md
│   │   ├── CarMax Laws and Regulations For Dealer.md
│   │   ├── CarMax-Pre-Trip Inspection Two Car Haulers.md
│   │   ├── The Three Pillars of a CarMax Huddle.md
│   │   ├── carmax_vocabulary_guide.txt
│   │   ├── carmax_code_of_business_conduct_2014.txt
│   │   ├── carmax code of conduct.pdf
│   │   ├── 2024-01-25_fl_weigh-stations-best-practices.pdf
│   │   ├── cotrell_two_car_carrier_manual.pdf
│   │   └── safety_updates.txt
│   │
│   ├── personal_records/            # Gustavo's performance data
│   │   ├── Gustavo Guallar 2025 Overall Performance Rating & APR Summary.md
│   │   ├── Self-Evaluation Summary.md
│   │   ├── peer_training_and_self_evaluation_2022-2025_gustavo_guallar.txt
│   │   ├── Management Email Communications.md
│   │   └── leadership_notes.txt
│   │
│   ├── recognitions/                # Achievers recognition records
│   │   ├── Gustavo Guallar Recognition Given.md
│   │   ├── Gustavo Guallar Recognitions Received.md
│   │   ├── Gustavo Guallar Recognitions Reply.md
│   │   ├── recognitions_given_2025-11-04.txt
│   │   ├── recognitions_received_2025-11-04.txt
│   │   └── recognition_reply.txt
│   │
│   ├── training/                    # Peer training logs and materials
│   │   ├── Benaiah Gordon Training.txt
│   │   ├── Integration_Plan_Template.txt
│   │   ├── Pre-Trip Inspection Checklist – Two Car Haulers  (1).docx
│   │   ├── pre-trip_inspection_checklist_two car haulers_drive .docx
│   │   └── pre-trip_inspection_checklist_two car haulers_drive .pdf
│   │
│   └── assessments/                 # Harver and MDP assessments
│       ├── Gustavo Guallar CarMax Manager Development – Harver Assessment Summary.md
│       └── Gustavo Guallar Harver Assessment Summary.md
│
├── templates/                       # Document templates
│   ├── recognition_template.md
│   ├── training_text_template.md
│   └── idp_report_template.md
│
├── tools/                           # Automation scripts
│   ├── carmax_cli.py               ← MASTER ENTRY POINT
│   ├── knowledge_loader.py          # Corpus scanner and loader
│   ├── feedback_loop.py             # Generation tracking and feedback
│   ├── generate_recognition.py      # Recognition message generator
│   ├── generate_training_text.py    # Training communication generator
│   ├── generate_idp_report.py       # IDP report generator
│   └── generate_communication.py    # General communication generator
│
├── generated/                       # All generated output (auto-feeds back)
│   ├── recognitions/
│   ├── training_texts/
│   ├── idp_reports/
│   └── communications/
│
├── feedback_loop/                   # System metadata
│   ├── generation_log.json          # Log of every generated document
│   └── corpus_index.json            # Full corpus index for auditing
│
├── docs/                            # System documentation and identity
│   ├── SYSTEM_ARCHITECTURE.md       ← THIS FILE
│   ├── identity.md                  # AI agent identity anchor
│   ├── Personal Sub‑Prompt for Gustavo.md
│   ├── Prompt - Expert CarMax Manager & IDP Coach.md
│   ├── MANIFEST.md                  # Original project manifest
│   └── Control Tower (Instructions Charter).md
│
└── README.md                        ← MASTER GUIDE
```

---

## 3. Core Components

### 3.1 Knowledge Base (`knowledge_base/`)
The source-of-truth corpus. Contains 35+ files across 5 categories. All files are originals — never modified by the system. The knowledge loader scans this directory recursively to build the corpus used by all generators.

### 3.2 Generators (`tools/`)
Four specialized generators, each consuming the full corpus:

| Generator | Command | Output Dir | What It Produces |
|-----------|---------|------------|------------------|
| Recognition | `recognition` | `generated/recognitions/` | Achievers-style recognition messages |
| Training Text | `training` | `generated/training_texts/` | Training communications with 5-step structure |
| IDP Report | `idp` | `generated/idp_reports/` | Full IDP reports with SMART goals, evidence |
| Communication | `communication` | `generated/communications/` | Huddles, safety alerts, team emails, mgmt updates |

### 3.3 Feedback Loop (`feedback_loop.py`)
Every generated document is:
1. Saved to `generated/` (organized by type)
2. Logged in `feedback_loop/generation_log.json` with full metadata
3. Automatically included in the next corpus build

This means the system grows smarter with each generation — patterns, vocabulary, and examples from previous outputs inform future ones.

### 3.4 Knowledge Loader (`knowledge_loader.py`)
Scans both `knowledge_base/` AND `generated/` to build a unified corpus. Provides category-filtered access (recognitions, training, personal records, etc.) to all generators.

### 3.5 Templates (`templates/`)
Markdown templates following CarMax's 5-Step Communication Structure:
1. Greeting
2. Purpose Statement
3. Key Points
4. Value Connection
5. Positive Close

---

## 4. Data Flow

```
1. User requests document via CLI or AI assistant
       │
2. Knowledge Loader scans knowledge_base/ + generated/
       │
3. Generator selects relevant content by category
       │
4. Content is assembled using templates + CarMax vocabulary
       │
5. Output saved to generated/{type}/
       │
6. Feedback Loop registers the file in generation_log.json
       │
7. Next generation automatically includes this output as source
```

---

## 5. CarMax Values Integration

Every generated document is filtered through the four CarMax values:

| Value | How It's Applied |
|-------|-----------------|
| **Win Together** | Inclusive language (we/our/team), collaboration emphasis |
| **Put People First** | Recognition, appreciation, growth-focused language |
| **Go For Greatness** | Excellence standards, improvement encouragement |
| **Do The Right Thing** | Integrity, accountability, procedure compliance |

The vocabulary standards from `CarMax Vocabulary & Philosophy.md` are the authoritative source for tone and language.

---

## 6. AI Assistant Navigation Guide

When navigating this system as an AI assistant:

1. **Start with** `docs/identity.md` and `docs/Personal Sub‑Prompt for Gustavo.md` to understand the user context
2. **Use** `knowledge_base/carmax_reference/CarMax Vocabulary & Philosophy.md` for tone/language guidance
3. **Check** `feedback_loop/generation_log.json` to see what's been previously generated
4. **Run** `python tools/carmax_cli.py status` to get a quick system overview
5. **Generate documents** via `python tools/carmax_cli.py [command]` with appropriate arguments
6. **All generated content** automatically feeds back — no manual steps needed

### Key Files for Understanding Gustavo's Profile:
- `knowledge_base/personal_records/Self-Evaluation Summary.md` — comprehensive career history
- `knowledge_base/personal_records/Gustavo Guallar 2025 Overall Performance Rating & APR Summary.md` — current ratings
- `knowledge_base/assessments/` — Harver and MDP assessment data
- `knowledge_base/recognitions/` — full recognition history (given and received)
- `docs/Personal Sub‑Prompt for Gustavo.md` — career goals and coaching preferences
