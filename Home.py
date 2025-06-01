import streamlit as st
import os

# Set the title of the page
st.set_page_config(page_title="Gen-AI-based VR Asset Generator", page_icon="🥽", layout="wide", initial_sidebar_state='collapsed')
st.title("Gen-AI-based VR Asset Generator 🥽")

st.session_state.cwd = os.getcwd()

st.markdown("## Introduction")
st.markdown('''This work is based on a framework presented in ***"Generative Artificial Intelligence and Virtual Reality: Emerging Future of the Building Component Inspection Training"*** during CIB WBC 2025.''')
st.markdown("### Why this framework is needed?")
st.markdown("""This framework combines generative artificial intelligence (Gen AI) and virtual reality (VR) to create a more immersive training environment and help building maintenance and operations. Traditional training methods rely on limited visuals and text, restricting inspectors’ exposure to varied building conditions and hindering their preparedness. The proposed solution uses Gen AI to generate realistic textures of deteriorating components and integrates them into an interactive VR environment. This allows trainees to practice identifying and assessing conditions in a hands-on, immersive setting. The approach aims to reduce subjectivity in inspections and improve knowledge transfer. A hypothetical case study illustrates the framework’s application, showing its potential not only in building maintenance but also in other fields requiring precise and unbiased evaluations.""")
st.image("./Assets/Framework.png", caption="Framework for Gen-AI-based VR Asset Generator")

st.markdown('#')

if st.button("API Configuration ➡️", type="primary"):
    # Switch to the API configuration page
    st.switch_page("pages/API Configuration.py")

