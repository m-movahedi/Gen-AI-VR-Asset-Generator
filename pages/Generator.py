import streamlit as st
import os 
st.session_state.cwd = os.getcwd()
# Set the title of the page
st.set_page_config(page_title="Generator", page_icon="⚙️", layout="wide", initial_sidebar_state='collapsed')

st.title("Generator ⚙️")

file = st.file_uploader("Upload your model file", type=["ifc","dae", 'glb'], key="model_file")
