import streamlit as st
from modules.loaders import list_minors, load_json, load_course
from modules.ui_components import section, key_value

st.set_page_config(layout="wide")
st.title("🧭 Course Browser")

minor_files = list_minors()
minor_titles = {}

for path in minor_files:
    m = load_json(path)
    minor_titles[m["title"]] = m

minor_title = st.selectbox("Select Minor", list(minor_titles.keys()))
minor = minor_titles[minor_title]

course_ids = minor["courses"]

section("Courses")

for cid in course_ids:
    course = load_course(cid)
    with st.expander(f'{course["course_id"]} – {course["title"]}'):
        key_value("Language", course["administrative"]["language"])
        key_value("Level", course["administrative"]["level"])
        key_value("Assessment", course["assessment"]["scale"])
        st.markdown(f"[Course link]({course['course_link']})")
