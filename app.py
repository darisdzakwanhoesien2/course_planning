import streamlit as st

st.set_page_config(
    page_title="Course Planner",
    layout="wide"
)

st.title("🎓 Course Planning Dashboard")

st.markdown("""
Welcome to your **course planning system**.

Use the sidebar to:
- Browse minor programs
- Explore courses
- Inspect detailed course descriptions
""")

st.info("Select a page from the sidebar to begin.")
