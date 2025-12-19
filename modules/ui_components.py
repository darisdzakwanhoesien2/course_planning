import streamlit as st

def section(title: str):
    st.markdown(f"### {title}")

def bullet_list(items):
    for item in items:
        st.markdown(f"- {item}")

def key_value(label, value):
    st.markdown(f"**{label}:** {value}")
