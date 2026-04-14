# TeacherEvalGenerator

A starter app for generating teacher evaluation drafts from observation notes and district rubric/forms.

## What this does today
- Upload a district rubric CSV (`domain,indicator,ratings`) to drive scoring dropdowns.
- Paste observation notes.
- Generate a lesson summary, strengths, growth areas, and evidence snippets.
- Fill ratings with dropdowns for each rubric item.
- Export a completed evaluation draft as Markdown.

## Quick start
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Rubric CSV format
Example:
```csv
domain,indicator,ratings
Planning,"Objective is standards-aligned","Ineffective|Developing|Effective|Highly Effective"
Instruction,"Checks for understanding","Ineffective|Developing|Effective|Highly Effective"
Environment,"Classroom culture supports learning","Ineffective|Developing|Effective|Highly Effective"
```

## Notes
- This is an MVP scaffold using deterministic text heuristics (no external LLM key required).
- You can replace `analyze_notes(...)` with an API call to your preferred LLM provider later.
