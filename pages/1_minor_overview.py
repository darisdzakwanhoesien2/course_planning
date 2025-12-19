import streamlit as st
from modules.loaders import list_minors, load_json
from modules.ui_components import section, key_value

st.set_page_config(layout="wide")
st.title("📚 Minor Program Overview")

minor_files = list_minors()

if not minor_files:
    st.warning("No minors found.")
    st.stop()

minor_map = {}
for path in minor_files:
    data = load_json(path)
    minor_map[data["title"]] = data

selected_title = st.selectbox(
    "Select a Minor Program",
    list(minor_map.keys())
)

minor = minor_map[selected_title]

section("Program Information")
key_value("ECTS Range", f'{minor["ects"]["minimum"]} – {minor["ects"]["maximum"]}')
key_value("Academic Year", minor["academic_year"])
key_value("Program Link", minor["program_link"])

section("Courses in this Minor")
for cid in minor["courses"]:
    st.markdown(f"- `{cid}`")
