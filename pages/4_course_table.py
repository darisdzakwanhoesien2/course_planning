import streamlit as st
import pandas as pd
from modules.loaders import list_minors, load_json, load_course

# -----------------------------------------------------
# Helpers
# -----------------------------------------------------
def period_to_semester(period: int) -> str:
    if period in (1, 2):
        return "Autumn"
    if period in (3, 4):
        return "Spring"
    return "Unknown"

def build_course_table():
    rows = []

    for minor_path in list_minors():
        minor = load_json(minor_path)
        minor_title = minor["title"]

        for course_id in minor.get("courses", []):
            course = load_course(course_id)

            periods = course.get("availability", {}).get("periods", [])
            semesters = sorted(
                {period_to_semester(p) for p in periods}
            )

            rows.append({
                "Minor": minor_title,
                "Course ID": course["course_id"],
                "Course Title": course["title"],
                "Periods": ", ".join(map(str, periods)) if periods else "-",
                "Semester(s)": ", ".join(semesters) if semesters else "-",
                "Language": course["administrative"]["language"],
                "Level": course["administrative"]["level"]
            })

    return pd.DataFrame(rows)

# -----------------------------------------------------
# Page setup
# -----------------------------------------------------
st.set_page_config(layout="wide")
st.title("📊 Course Availability Table")

df = build_course_table()

if df.empty:
    st.warning("No course data available.")
    st.stop()

# -----------------------------------------------------
# Filters
# -----------------------------------------------------
st.markdown("### Filters")

selected_semester = st.multiselect(
    "Semester",
    options=["Autumn", "Spring"],
    default=[]
)

if selected_semester:
    df = df[df["Semester(s)"].str.contains("|".join(selected_semester))]

# -----------------------------------------------------
# Table display
# -----------------------------------------------------
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)
