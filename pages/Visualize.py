import streamlit as st
import os 
import json
with open("./temp/session.json", "r") as f:
    session = json.load(f)

st.session_state.cwd = os.getcwd()
st.set_page_config(page_title="Visualize", page_icon="👀", layout="wide", initial_sidebar_state='collapsed')

st.title("Visualize 👀")
st.markdown("This is a visualization of the generated 3D model.")
import base64
# Read .glb file and convert to base64 for embedding
c2, c1 = st.columns([1.5, 1])
with c1:
   modified_models = os.listdir(f"./{session['path']}/Modified")
   chosen_model = st.selectbox("Select a Gen-AI model", options=modified_models)
with c2:
    from Utils.utils import display
    st.components.v1.html(display(f"./{session['path']}/Modified/{chosen_model}", transparency=1.0), height=520)


if st.button("Save 💾 ", type="primary"):
    with open(f"./{session['path']}/{session['file_name']}.json", "w") as file:
         json.dump(session, file, indent=4) 