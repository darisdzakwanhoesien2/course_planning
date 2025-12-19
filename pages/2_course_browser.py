import streamlit as st
from modules.loaders import list_minors, load_json, load_course
from modules.ui_components import section, bullet_list, key_value

# =====================================================
# Page setup
# =====================================================
st.set_page_config(layout="wide")
st.title("🧭 Course Browser")

# =====================================================
# Helpers
# =====================================================
def period_to_semester(period: int) -> str:
    if period in (1, 2):
        return "Autumn"
    if period in (3, 4):
        return "Spring"
    return "Unknown"

# =====================================================
# Load minors
# =====================================================
minor_files = list_minors()

if not minor_files:
    st.warning("No minor programs found.")
    st.stop()

minors = {}
for path in minor_files:
    minor = load_json(path)
    minors[minor["title"]] = minor

# =====================================================
# Minor selection
# =====================================================
selected_minor_title = st.selectbox(
    "Select Minor Program",
    list(minors.keys())
)

minor = minors[selected_minor_title]

st.markdown("---")

section("Minor Overview")
key_value(
    "ECTS Range",
    f'{minor["ects"]["minimum"]} – {minor["ects"]["maximum"]}'
)
key_value("Academic Year", minor.get("academic_year", "-"))
st.markdown(f"[Program page]({minor['program_link']})")

# =====================================================
# Courses
# =====================================================
st.markdown("---")
section("Courses")

if not minor.get("courses"):
    st.info("No courses listed for this minor.")
    st.stop()

for course_id in minor["courses"]:
    course = load_course(course_id)

    with st.expander(f'{course["course_id"]} – {course["title"]}', expanded=False):

        # -------------------------------------------------
        section("Basic Information")
        key_value("Language", course["administrative"]["language"])
        key_value("Level", course["administrative"]["level"])
        key_value("Subject", course["administrative"]["subject"])
        key_value(
            "Person in Charge",
            course["administrative"]["person_in_charge"]
        )
        st.markdown(f"[Official course page]({course['course_link']})")

        # -------------------------------------------------
        section("Availability")

        periods = course.get("availability", {}).get("periods", [])

        if periods:
            semester_map = {}
            for p in periods:
                sem = period_to_semester(p)
                semester_map.setdefault(sem, []).append(p)

            for sem, plist in semester_map.items():
                st.markdown(
                    f"- **{sem} Semester**: Periods {', '.join(map(str, plist))}"
                )
        else:
            st.markdown("- Availability not specified")

        # -------------------------------------------------
        section("Learning Outcomes")
        bullet_list(course.get("learning_outcomes", []))

        # -------------------------------------------------
        section("Content")
        bullet_list(course.get("content", []))

        # -------------------------------------------------
        section("Study Methods")
        bullet_list(course.get("study_methods", []))

        # -------------------------------------------------
        section("Teaching Methods")
        teaching = course.get("teaching_methods", {})
        if teaching:
            for name, info in teaching.items():
                label = name.replace("_", " ").title()
                hours = info.get("hours", "")
                st.markdown(f"- **{label}**: {hours} h")
        else:
            st.markdown("- Not specified")

        # -------------------------------------------------
        section("Assessment")
        assessment = course.get("assessment", {})
        key_value("Type", assessment.get("type", "-"))
        key_value("Scale", assessment.get("scale", "-"))
        key_value(
            "Final Exam",
            "Yes" if assessment.get("final_exam") else "No"
        )


# import streamlit as st
# from modules.loaders import list_minors, load_json, load_course
# from modules.ui_components import section, key_value

# st.set_page_config(layout="wide")
# st.title("🧭 Course Browser")

# minor_files = list_minors()
# minor_titles = {}

# for path in minor_files:
#     m = load_json(path)
#     minor_titles[m["title"]] = m

# minor_title = st.selectbox("Select Minor", list(minor_titles.keys()))
# minor = minor_titles[minor_title]

# course_ids = minor["courses"]

# section("Courses")

# for cid in course_ids:
#     course = load_course(cid)
#     with st.expander(f'{course["course_id"]} – {course["title"]}'):
#         key_value("Language", course["administrative"]["language"])
#         key_value("Level", course["administrative"]["level"])
#         key_value("Assessment", course["assessment"]["scale"])
#         st.markdown(f"[Course link]({course['course_link']})")
