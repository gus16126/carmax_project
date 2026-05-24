# CarMax IDP Manager System

**Owner:** Gustavo Felipe Guallar (Associate ID: 280305)  
**Role:** Home Delivery Driver / Fleet Driver — CarMax Logistics  
**Goal:** Progression from current role → Logistics Coordinator → Logistics Manager → Senior Manager/Regional Lead

---

## What Is This System?

The CarMax IDP Manager is your personal document generation and career development platform. It organizes all your CarMax materials — recognitions, training records, performance data, assessments — and uses them to generate professional documents aligned with CarMax values and vocabulary.

**Every document you generate automatically becomes source material for future generations**, making the system smarter and more personalized over time.

---

## Quick Start

All commands run from the `tools/` directory:

```bash
cd /home/ubuntu/carmax_idp_system/tools
```

### Check System Status
```bash
python carmax_cli.py status
```

### Generate a Recognition
```bash
python carmax_cli.py recognition \
  --to "Santiago Munarriz" \
  --value "Win Together" \
  --reason "stepping up to help with an auction move without hesitation"
```

**Values:** `Win Together` | `Put People First` | `Go For Greatness` | `Do The Right Thing`  
**Styles:** `standard` (default) | `formal` | `brief`

### Generate a Training Communication
```bash
python carmax_cli.py training \
  --subject "Pre-Trip Inspection Refresher" \
  --audience "All Drivers" \
  --series "Safety First"
```

### Generate an IDP Report
```bash
python carmax_cli.py idp \
  --period "Q2 2026" \
  --target-role "Logistics Coordinator"
```

### Generate a Leadership Communication
```bash
# Team huddle notes
python carmax_cli.py communication --type huddle --topic "Morning Safety Brief"

# Safety alert
python carmax_cli.py communication --type safety_alert --topic "Tire Pressure Checks"

# Team email
python carmax_cli.py communication --type team_email --topic "Q2 Goals Update"

# Management update
python carmax_cli.py communication --type management_update --topic "Monthly Performance Review"
```

---

## Asking the AI Assistant for Documents

When working with an AI assistant, you can simply ask in natural language:

- *"Write a recognition for Carlos Barrios for helping with training — Win Together value"*
- *"Create a training text about DOT compliance for all drivers"*
- *"Generate my Q2 2026 IDP report targeting Logistics Coordinator"*
- *"Draft a safety alert about proper tie-down procedures"*
- *"Give me a team huddle script for tomorrow's morning meeting about inspection checklists"*

The assistant should use the CLI tools to generate the documents, which will automatically:
1. Pull relevant content from the knowledge base
2. Apply CarMax vocabulary and values
3. Save the output to `generated/`
4. Register it in the feedback loop for future use

---

## How the Feedback Loop Works

```
You generate a document
        ↓
It's saved in generated/
        ↓
It's logged in feedback_loop/generation_log.json
        ↓
Next time you generate anything, this document
is included in the knowledge base scan
        ↓
Future documents are informed by past ones
```

This means:
- Recognition patterns you use get refined over time
- Training topics build on previous communications
- IDP reports incorporate all historical evidence, including past reports
- The system vocabulary converges toward your authentic CarMax voice

---

## What's In the Knowledge Base

| Category | Files | What's Inside |
|----------|-------|---------------|
| **CarMax Reference** | 17 | Vocabulary guide, Code of Conduct, Leadership Binder, IDP program details, Pre-Trip checklists, DOT compliance |
| **Personal Records** | 5 | APR summary, Self-Evaluation, performance data, management communications |
| **Recognitions** | 6 | All Achievers recognitions — given and received — with dates and values |
| **Training** | 5 | Peer training logs (Ben Gordon, Santiago, Alex, Benaiah), inspection checklists |
| **Assessments** | 2 | Harver Assessment, MDP Assessment Summary |

---

## Document Types Reference

### Recognition
For the Achievers platform. Generates messages that match the tone and format of real recognitions in your history. Includes proper value alignment and signature.

### Training Text
Team training communications following the CarMax 5-Step Structure (Greeting → Purpose → Key Points → Value Connection → Positive Close). Draws from actual training records and procedures.

### IDP Report
Comprehensive Individual Development Plan report including:
- Executive summary
- Performance snapshot with ratings
- Competency assessment table
- SMART goals tailored to your target role
- Evidence base from recognitions, training, and performance data
- Values alignment matrix
- Career path timeline
- Development action plan (30/60/90/180+ days)

### Communication
Four sub-types:
- **Huddle:** Team huddle notes with discussion points and action items
- **Safety Alert:** Formatted safety communications with required actions
- **Team Email:** General team communications
- **Management Update:** Structured updates with metrics, wins, and challenges

---

## File Locations

| What | Where |
|------|-------|
| Source materials | `knowledge_base/` |
| Generated documents | `generated/` |
| Templates | `templates/` |
| Automation tools | `tools/` |
| Generation log | `feedback_loop/generation_log.json` |
| Full corpus index | `feedback_loop/corpus_index.json` |
| System architecture | `docs/SYSTEM_ARCHITECTURE.md` |
| AI agent identity | `docs/identity.md` |
| Coaching prompt | `docs/Personal Sub‑Prompt for Gustavo.md` |

---

## Adding New Materials

To add new source materials to the knowledge base:

1. Place the file in the appropriate `knowledge_base/` subfolder:
   - CarMax policies/procedures → `carmax_reference/`
   - Your performance data → `personal_records/`
   - New recognitions → `recognitions/`
   - Training records → `training/`
   - Assessment results → `assessments/`

2. Rebuild the index:
   ```bash
   python carmax_cli.py index
   ```

3. The new material will automatically be used in future generations.

---

## System Values

All content generated by this system adheres to CarMax's communication standards:

- **Tone:** Calm • Clear • Positive • Constructive
- **Language:** Inclusive (we/our/team), appreciation-focused, values-aligned
- **Structure:** 5-Step format (Greeting, Purpose, Key Points, Value Connection, Positive Close)
- **Integrity:** All content traceable to authentic source materials

---

*"We succeed when our people succeed. Integrity is our North Star."*

— CarMax IDP Manager System v2.0
