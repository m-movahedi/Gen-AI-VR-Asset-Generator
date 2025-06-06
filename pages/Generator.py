import streamlit as st
import os 
from Utils.utils import display
import json
with open("./temp/session.json", "r") as f:
    session = json.load(f)
st.session_state.cwd = os.getcwd()
# Set the title of the page
st.set_page_config(page_title="Generator", page_icon="⚙️", layout="wide", initial_sidebar_state='collapsed')

st.title("Generator ⚙️")

c2, c1 = st.columns([2, 1])

with c1:
    c11, c12 = st.columns([1, 1.5])
    with c11:
        st.write("Select components:")
    with c12:
        import pandas as pd
        components = pd.read_csv(session['Components'])
        component_list = st.multiselect("Select components", options=components['GUID'].tolist(), label_visibility="collapsed", placeholder="Select components")

    c11, c12 = st.columns([1, 1.5])
    with c11:
        st.write("Select a Gen-AI model")
    with c12:
        texture_model = st.selectbox("Select a Gen-AI model", options=['gpt-image-1', 'dall-e-2'], label_visibility="collapsed", placeholder="Select a Gen-AI model")
        session['texture_model'] = texture_model
    c11, c12 = st.columns([1, 1.5])
    with c11:
        st.write("Choose knowledge base file:")
    with c12:
        knowledge_base_file = st.file_uploader("Upload a knowledge base file",
                                               type=["txt"],
                                               key="knowledge_base_file",
                                               label_visibility="collapsed")
        if knowledge_base_file is not None:
            # Save the uploaded file to a temporary location
            knowledge_path = f"./{session['path']}/{session['file_name']}_knowledge.txt"
            with open(knowledge_path, "wb") as f:
                f.write(knowledge_base_file.getbuffer())
            st.success(f"Knowledge base file '{knowledge_base_file.name}' uploaded successfully.", icon="✅")
            session['knowledge_base_file'] = knowledge_path
            session['knowledge_base']= knowledge_base_file.getbuffer()
    st.write("Additional description:")
    additional_info = st.text_input("Enter additional information (optional)", label_visibility="collapsed")
    st.write('Condition rating:')
    condition_rating = st.slider("Select condition rating", min_value=0, max_value=100, value=100, step=10, label_visibility="collapsed")
    generate_flag = st.button("Generate assets",
                              type="primary",
                              #disabled=not component_list or not texture_model or not knowledge_base_file
                              )
    if generate_flag:
        st.progress(0, text="Generating assets...")
        
    st.write(type(component_list)==list)

with c2:
    # Display the GLB file
    try:
        st.components.v1.html(session['Last rendered'], height=520)
    except:
        st.error("No file to display. Please upload go back to the File Selecetion Tab", icon="❌")

    