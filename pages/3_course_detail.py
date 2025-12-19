import streamlit as st
from modules.loaders import list_minors, load_json, load_course
from modules.ui_components import section, bullet_list, key_value

st.set_page_config(layout="wide")
st.title("📘 Course Detail")

# Collect all courses from all minors
course_ids = set()
for path in list_minors():
    minor = load_json(path)
    course_ids.update(minor["courses"])

course_id = st.selectbox("Select Course", sorted(course_ids))

course = load_course(course_id)

section("Basic Information")
key_value("Course ID", course["course_id"])
key_value("Title", course["title"])
key_value("Language", course["administrative"]["language"])
key_value("Level", course["administrative"]["level"])
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
    st.markdown(f"- **{k.replace('_', ' ').title()}**: {v.get('hours', '')} h")

section("Assessment")
key_value("Type", course["assessment"]["type"])
key_value("Scale", course["assessment"]["scale"])
key_value("Final Exam", "Yes" if course["assessment"]["final_exam"] else "No")
