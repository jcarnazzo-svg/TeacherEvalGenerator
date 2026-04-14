from __future__ import annotations

import streamlit as st

from core import analyze_notes, export_markdown, parse_rubric_csv


def main() -> None:
    st.set_page_config(page_title="Teacher Evaluation Generator", layout="wide")
    st.title("Teacher Evaluation Generator (MVP)")
    st.caption("Upload a district rubric, paste notes, generate a draft, and fill ratings with dropdowns.")

    with st.sidebar:
        st.header("Session details")
        teacher_name = st.text_input("Teacher name")
        evaluator_name = st.text_input("Evaluator name")
        lesson_date = st.date_input("Lesson date").isoformat()

        rubric_file = st.file_uploader(
            "Upload rubric CSV",
            type=["csv"],
            help="Required columns: domain, indicator, ratings (pipe-separated).",
        )

    notes = st.text_area(
        "Observation notes",
        height=220,
        placeholder="Paste timestamped or narrative observation notes here...",
    )

    if st.button("Generate draft"):
        if not rubric_file:
            st.error("Please upload a rubric CSV first.")
            st.stop()
        if not notes.strip():
            st.error("Please add observation notes.")
            st.stop()

        try:
            rubric_rows = parse_rubric_csv(rubric_file.read())
        except Exception as exc:  # noqa: BLE001
            st.error(f"Could not parse rubric file: {exc}")
            st.stop()

        analysis = analyze_notes(notes)
        st.session_state["analysis"] = analysis
        st.session_state["rubric_rows"] = rubric_rows

    analysis = st.session_state.get("analysis")
    rubric_rows = st.session_state.get("rubric_rows")

    if analysis and rubric_rows:
        st.subheader("Generated lesson summary")
        st.write(analysis["summary"])

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Strengths**")
            for s in analysis["strengths"]:
                st.write(f"- {s}")
        with col2:
            st.markdown("**Growth Areas**")
            for g in analysis["growth_areas"]:
                st.write(f"- {g}")

        st.subheader("Rubric scoring")
        selected_ratings: dict[str, str] = {}
        comments: dict[str, str] = {}

        for idx, row in enumerate(rubric_rows):
            key = f"row_{idx}"
            with st.expander(f"{row.domain}: {row.indicator}", expanded=False):
                default_index = row.ratings.index("Effective") if "Effective" in row.ratings else 0
                selected_ratings[key] = st.selectbox(
                    "Rating",
                    row.ratings,
                    index=default_index,
                    key=f"rating_{key}",
                )
                evidence = analysis["evidence"].get(row.domain, [])[:2]
                if evidence:
                    st.caption("Suggested evidence")
                    for ev in evidence:
                        st.write(f"- {ev}")
                comments[key] = st.text_area("Comment", key=f"comment_{key}", height=80)

        markdown_doc = export_markdown(
            teacher_name=teacher_name,
            evaluator_name=evaluator_name,
            lesson_date=lesson_date,
            analysis=analysis,
            rubric_rows=rubric_rows,
            selected_ratings=selected_ratings,
            comments=comments,
        )

        st.download_button(
            "Download evaluation draft (.md)",
            data=markdown_doc,
            file_name=f"evaluation_{teacher_name or 'teacher'}.md",
            mime="text/markdown",
        )


if __name__ == "__main__":
    main()
