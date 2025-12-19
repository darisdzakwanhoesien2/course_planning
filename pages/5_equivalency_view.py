import streamlit as st
from pathlib import Path

from modules.loaders import load_json, load_course

# =====================================================
# Page setup
# =====================================================
st.set_page_config(layout="wide")
st.title("🔄 Course Equivalency & External Learning Mapping")

st.markdown("""
This page shows how **Oulu University courses** can be matched with  
**external learning providers** (e.g. Coursera, edX).

• One Oulu course may map to **multiple external programs**  
• Matches can be **partial or full**  
• All mappings are **informational and advisory**
""")

# =====================================================
# Paths
# =====================================================
EQUIV_DIR = Path("data/equivalencies")
PROVIDER_DIR = Path("data/providers")
PROGRAM_DIR = Path("data/external_programs")
EXTERNAL_COURSE_DIR = Path("data/external_courses")

# =====================================================
# Load equivalency files
# =====================================================
equiv_files = sorted(EQUIV_DIR.glob("*_equivalency.json"))

if not equiv_files:
    st.warning("No equivalency mappings found.")
    st.stop()

# Build course map
course_map = {}
for path in equiv_files:
    equiv = load_json(path)
    oulu_id = equiv["oulu_course_id"]
    course_map[oulu_id] = equiv

# =====================================================
# Course selection
# =====================================================
selected_course_id = st.selectbox(
    "Select Oulu University Course",
    sorted(course_map.keys())
)

equiv_data = course_map[selected_course_id]
oulu_course = load_course(selected_course_id)

st.markdown("---")

# =====================================================
# Oulu course overview
# =====================================================
st.markdown("## 🎓 Oulu University Course")

st.markdown(f"**{oulu_course['course_id']} – {oulu_course['title']}**")
st.markdown(f"- Level: {oulu_course['administrative']['level']}")
st.markdown(f"- Subject: {oulu_course['administrative']['subject']}")
st.markdown(f"- ECTS: {oulu_course.get('ects', '-')}")
st.markdown(f"[Official course page]({oulu_course['course_link']})")

# =====================================================
# External equivalencies
# =====================================================
st.markdown("---")
st.markdown("## 🌍 External Learning Equivalencies")

programs = equiv_data.get("accepted_external_programs", [])

if not programs:
    st.info("No external equivalencies defined for this course.")
    st.stop()

for idx, prog in enumerate(programs, start=1):

    program_path = PROGRAM_DIR / f"{prog['program_id']}.json"
    program = load_json(program_path)

    provider_path = PROVIDER_DIR / f"{program['provider']}.json"
    provider = load_json(provider_path)

    with st.expander(
        f"{idx}. {program['title']} ({provider['name']})",
        expanded=False
    ):

        # -------------------------------------------------
        st.markdown("### Program Overview")
        st.markdown(f"- **Provider**: {provider['name']}")
        st.markdown(f"- **Credential Type**: {program['credential_type']}")
        st.markdown(f"- **Level**: {program['level']}")
        st.markdown(f"- **Languages**: {', '.join(program['languages'])}")
        st.markdown(f"[Program page]({program['url']})")

        # -------------------------------------------------
        st.markdown("### Equivalency Details")
        st.markdown(f"- **Coverage**: {prog['coverage'].title()}")
        st.markdown(f"- **Estimated Hour Match**: {prog['estimated_hours_match']} h")
        st.markdown(
            f"- **Estimated ECTS Equivalent**: {prog['ects_equivalent_estimate']}"
        )

        st.markdown("**Rationale**")
        st.markdown(f"> {prog['rationale']}")

        # -------------------------------------------------
        st.markdown("### Required External Units")
        for ext_id in prog.get("required_units", []):
            ext_path = EXTERNAL_COURSE_DIR / f"{ext_id}.json"
            ext = load_json(ext_path)

            st.markdown(
                f"- **{ext['title']}** "
                f"({ext.get('estimated_hours', '-')} h)"
            )

        # -------------------------------------------------
        if equiv_data.get("notes"):
            st.markdown("### Notes")
            for note in equiv_data["notes"]:
                st.markdown(f"- {note}")

# =====================================================
# Footer
# =====================================================
st.markdown("---")
st.markdown("""
⚠️ **Disclaimer**  
External equivalencies are **advisory** and do not automatically grant credit.  
Final approval depends on **faculty and program regulations**.
""")
