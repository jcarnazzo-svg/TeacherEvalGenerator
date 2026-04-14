from core import analyze_notes, parse_rubric_csv, summarize_lesson


def test_summarize_lesson_returns_first_sentences() -> None:
    notes = "First sentence. Second sentence. Third sentence. Fourth sentence."
    summary = summarize_lesson(notes, max_sentences=2)
    assert summary == "First sentence. Second sentence."


def test_parse_rubric_csv() -> None:
    csv_data = b"domain,indicator,ratings\nInstruction,Checks for understanding,Ineffective|Effective\n"
    rows = parse_rubric_csv(csv_data)
    assert len(rows) == 1
    assert rows[0].domain == "Instruction"
    assert rows[0].ratings == ["Ineffective", "Effective"]


def test_analyze_notes_has_summary_and_strengths() -> None:
    notes = "Teacher explained objective. Students completed exit ticket."
    output = analyze_notes(notes)
    assert output["summary"]
    assert isinstance(output["strengths"], list)
