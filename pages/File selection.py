import streamlit as st
import os 
import shutil
from Utils.utils import convert, display
st.set_page_config(page_title="Select model", page_icon="🗃️", layout="wide", initial_sidebar_state='collapsed')
st.title("Select model 🗃️")

# Constants and binary checks
st.session_state.cwd = os.getcwd()
os.chdir(st.session_state.cwd)
check_ = False
format_ = None
vis_ = False
st.session_state.path = None
#os.remove('./temp')

# split the screen
c1, c2 = st.columns([1, 1])
with c2:
    #load the file
    try:
        file_ = st.file_uploader("Upload your model file", type=["ifc","dae", 'glb'], key="model_file", label_visibility="collapsed")
        if file_ is not None:
            format_ = file_.name.split('.')[-1] if file_ is not None else None
            if format_ not in ["ifc", "dae", "glb"]:
                st.error("Please upload a valid file format: IFC, DAE, or GLB.", icon="❌")
            if format_ != 'glb':
                file_path, format_, check_ = convert(file_, output_path='./temp', output_name='temp', format='glb')
                st.success(f"""GLB file is created.""", icon="✅")
            else:
                with open(f'./temp/temp.glb', "wb") as f:
                    f.write(file_.getbuffer())
                file_path = f'./temp/temp.glb'
                format_ = 'glb'
                check_ = True
                st.success(f"""GLB file is uploaded.""", icon="✅")
    except:
        os.chdir(st.session_state.cwd)
        
with c2:
    c121, c122 = st.columns([3, 1])
    with c121:
        transparency = st.slider("Transparency", min_value=0.0, max_value=1.0, value=0.5, step=0.1, key="transparency")
    with c122:
        vis_ = st.button("Visualize", type="primary", disabled = not check_, key="use_file")
    
with c1:
    try:
        if vis_ == True:
            # Check if the file is a valid 3D model format
            html = display(file_path, transparency=transparency)
            st.components.v1.html(html, height=520)
    except:
        os.chdir(st.session_state.cwd)
        pass

os.chdir(st.session_state.cwd)

if st.button("Generate ➡️", type="primary", disabled = not check_):
    # Switch to the Generator page
    st.switch_page("pages/Generator.py")