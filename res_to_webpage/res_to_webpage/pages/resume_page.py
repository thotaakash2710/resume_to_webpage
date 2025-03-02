import streamlit as st

st.title("Generated Resume Webpage")

if "generated_resume" in st.session_state:
    st.markdown(st.session_state["generated_resume"], unsafe_allow_html=True)
else:
    st.error("No resume data found. Please go back and generate a resume.")
