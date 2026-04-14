from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable


DEFAULT_RATINGS = ["Ineffective", "Developing", "Effective", "Highly Effective"]


@dataclass
class RubricRow:
    domain: str
    indicator: str
    ratings: list[str]


def split_sentences(text: str) -> list[str]:
    raw = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in raw if s.strip()]


def summarize_lesson(notes: str, max_sentences: int = 3) -> str:
    sentences = split_sentences(notes)
    if not sentences:
        return "No lesson summary available. Add more observation notes."
    return " ".join(sentences[:max_sentences])


def find_evidence(notes: str) -> dict[str, list[str]]:
    text = notes.lower()
    sentences = split_sentences(notes)

    keyword_map = {
        "Planning": ["objective", "standard", "lesson plan", "target"],
        "Instruction": ["question", "model", "explain", "checks for understanding", "guided"],
        "Environment": ["culture", "respect", "behavior", "routine", "engagement"],
        "Assessment": ["exit ticket", "assessment", "quiz", "monitor", "feedback"],
    }

    evidence: dict[str, list[str]] = {k: [] for k in keyword_map}
    for domain, keywords in keyword_map.items():
        for sentence in sentences:
            s = sentence.lower()
            if any(k in s for k in keywords):
                evidence[domain].append(sentence)

    if not any(evidence.values()) and text:
        evidence["Instruction"] = sentences[:2]

    return evidence


def analyze_notes(notes: str) -> dict[str, object]:
    summary = summarize_lesson(notes)
    evidence = find_evidence(notes)

    strengths: list[str] = []
    growth: list[str] = []

    if evidence.get("Instruction"):
        strengths.append("Instruction included observable teaching moves and student-facing explanations.")
    else:
        growth.append("Add clearer evidence of instructional modeling and checks for understanding.")

    if evidence.get("Assessment"):
        strengths.append("Assessment evidence was present during the lesson.")
    else:
        growth.append("Capture more formative assessment evidence (checks for understanding, exit tickets, quick polls).")

    if evidence.get("Environment"):
        strengths.append("Classroom culture and routines showed support for learning.")
    else:
        growth.append("Include evidence of classroom routines, behavior systems, and culture-building moves.")

    if not strengths:
        strengths.append("No clear strengths detected from current notes; add more specific evidence statements.")

    return {
        "summary": summary,
        "strengths": strengths,
        "growth_areas": growth,
        "evidence": evidence,
    }


def parse_rubric_csv(contents: bytes) -> list[RubricRow]:
    text_stream = io.StringIO(contents.decode("utf-8"))
    reader = csv.DictReader(text_stream)
    if reader.fieldnames is None:
        raise ValueError("CSV file is empty.")

    normalized = {name.lower(): name for name in reader.fieldnames}
    required = {"domain", "indicator", "ratings"}
    missing = required - set(normalized)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    rows: list[RubricRow] = []
    for record in reader:
        ratings_raw = str(record[normalized["ratings"]]).strip()
        ratings = [r.strip() for r in ratings_raw.split("|") if r.strip()] or DEFAULT_RATINGS
        rows.append(
            RubricRow(
                domain=str(record[normalized["domain"]]).strip(),
                indicator=str(record[normalized["indicator"]]).strip(),
                ratings=ratings,
            )
        )
    return rows


def export_markdown(
    teacher_name: str,
    evaluator_name: str,
    lesson_date: str,
    analysis: dict[str, object],
    rubric_rows: Iterable[RubricRow],
    selected_ratings: dict[str, str],
    comments: dict[str, str],
) -> str:
    lines = [
        "# Teacher Evaluation Draft",
        f"- Teacher: {teacher_name or 'N/A'}",
        f"- Evaluator: {evaluator_name or 'N/A'}",
        f"- Lesson Date: {lesson_date or 'N/A'}",
        f"- Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Lesson Summary",
        str(analysis["summary"]),
        "",
        "## Strengths",
    ]

    for item in analysis["strengths"]:
        lines.append(f"- {item}")

    lines += ["", "## Growth Areas"]
    for item in analysis["growth_areas"]:
        lines.append(f"- {item}")

    lines += ["", "## Rubric Ratings"]
    for idx, row in enumerate(rubric_rows):
        key = f"row_{idx}"
        lines.append(f"### {row.domain} — {row.indicator}")
        lines.append(f"- Rating: {selected_ratings.get(key, 'Not selected')}")
        lines.append(f"- Comment: {comments.get(key, '').strip() or 'N/A'}")

    return "\n".join(lines)
