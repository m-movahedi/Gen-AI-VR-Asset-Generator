import streamlit as st
import os 
st.session_state.cwd = os.getcwd()
# Set the title of the page
st.set_page_config(page_title="Generator", page_icon="⚙️", layout="wide", initial_sidebar_state='collapsed')

st.title("Generator ⚙️")

file = st.file_uploader("Upload your model file", type=["ifc","dae", 'glb'], key="model_file")
format_ = file.name.split('.')[-1] if file else None
if format_ != 'dae':
    from Utils.utils import convert
    output_path, format_, status_flag = convert(file,'/temp','temp','dae')
    #file = trimesh.load(output_path)
else:
    output_path = f'./temp/{file.name}'
    format_ = 'dae'
    status_flag = True

#if status_flag:
    