import streamlit as st
from modules.loaders import list_minors, load_json, load_course
from modules.ui_components import section, bullet_list, key_value

st.set_page_config(layout="wide")
st.title("🧭 Course Browser")

# =====================================================
# Load minors
# =====================================================
minor_files = list_minors()

if not minor_files:
    st.warning("No minor programs found.")
    st.stop()

minors = {}
for path in minor_files:
    m = load_json(path)
    minors[m["title"]] = m

# =====================================================
# Minor selection
# =====================================================
selected_minor_title = st.selectbox(
    "Select Minor",
    list(minors.keys())
)

minor = minors[selected_minor_title]

st.markdown("---")

section("Minor Overview")
key_value(
    "ECTS Range",
    f'{minor["ects"]["minimum"]} – {minor["ects"]["maximum"]}'
)
key_value("Academic Year", minor["academic_year"])
st.markdown(f"[Program page]({minor['program_link']})")

# =====================================================
# Courses (INLINE DETAILS)
# =====================================================
st.markdown("---")
section("Courses")

for course_id in minor["courses"]:
    course = load_course(course_id)

    with st.expander(f'{course["course_id"]} – {course["title"]}', expanded=False):
        section("Basic Information")
        key_value("Language", course["administrative"]["language"])
        key_value("Level", course["administrative"]["level"])
        key_value("Subject", course["administrative"]["subject"])
        key_value("Person in Charge", course["administrative"]["person_in_charge"])
        st.markdown(f"[Official course page]({course['course_link']})")

        section("Learning Outcomes")
        bullet_list(course["learning_outcomes"])

        section("Content")
        bullet_list(course["content"])

        section("Study Methods")
        bullet_list(course["study_methods"])

        section("Teaching Methods")
        for k, v in course["teaching_methods"].items():
            st.markdown(
                f"- **{k.replace('_', ' ').title()}**: {v.get('hours', '')} h"
            )

        section("Assessment")
        key_value("Type", course["assessment"]["type"])
        key_value("Scale", course["assessment"]["scale"])
        key_value(
            "Final Exam",
            "Yes" if course["assessment"]["final_exam"] else "No"
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
