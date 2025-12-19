import streamlit as st
from pathlib import Path

from modules.loaders import list_minors, load_json, load_course
from modules.ui_components import section, bullet_list, key_value

# =====================================================
# Page setup
# =====================================================
st.set_page_config(layout="wide")
st.title("🆕 Available Courses (Not Yet in Any Minor)")

st.markdown("""
This page shows **all courses that exist in the system**  
but are **not yet assigned to any minor program**.

Use this to:
- discover unused courses
- plan new minors
- expand existing minors
""")

# =====================================================
# Paths
# =====================================================
COURSE_DIR = Path("data/courses")

# =====================================================
# Collect courses used in minors
# =====================================================
used_course_ids = set()

for minor_path in list_minors():
    minor = load_json(minor_path)
    for cid in minor.get("courses", []):
        used_course_ids.add(cid)

# =====================================================
# Collect all courses
# =====================================================
all_course_ids = {
    path.stem for path in COURSE_DIR.glob("*.json")
}

# =====================================================
# Compute available courses
# =====================================================
available_course_ids = sorted(all_course_ids - used_course_ids)

if not available_course_ids:
    st.success("🎉 All courses are already assigned to a minor.")
    st.stop()

st.markdown(f"### Found {len(available_course_ids)} available course(s)")

# =====================================================
# Display available courses
# =====================================================
for course_id in available_course_ids:
    course = load_course(course_id)

    with st.expander(f"{course['course_id']} – {course['title']}", expanded=False):

        section("Basic Information")
        key_value("Level", course["administrative"]["level"])
        key_value("Subject", course["administrative"]["subject"])

        # Handle language vs languages (backward compatible)
        langs = (
            course["administrative"].get("languages")
            or [course["administrative"].get("language")]
        )
        key_value("Language(s)", ", ".join(langs))

        key_value(
            "Person in Charge",
            course["administrative"]["person_in_charge"]
        )

        if course.get("ects"):
            key_value("ECTS", course["ects"])

        if course.get("availability", {}).get("periods"):
            periods = course["availability"]["periods"]
            st.markdown(f"**Available Periods:** {', '.join(map(str, periods))}")

        st.markdown(f"[Official course page]({course.get('course_link', '#')})")

        section("Learning Outcomes")
        bullet_list(course.get("learning_outcomes", []))

        section("Content")
        bullet_list(course.get("content", []))
