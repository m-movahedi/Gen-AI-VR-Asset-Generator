import streamlit as st
import os 
import shutil
from Utils.utils import convert, display
st.set_page_config(page_title="Select model", page_icon="🗃️", layout="wide", initial_sidebar_state='collapsed')
st.title("Select model 🗃️")

# Constants and binary checks
st.session_state.cwd = os.getcwd()
os.chdir(st.session_state.cwd)
os.makedirs('Archive', exist_ok=True)
check_ = False
format_ = None
vis_ = False
st.session_state.path = None
#os.remove('./temp')

# split the screen
c1, c2 = st.columns([1, 1])
with c2:
    #load the file
    #try:
        file_ = st.file_uploader("Upload your model file", type=["ifc","dae", 'glb'], key="model_file", label_visibility="collapsed")
        
        if file_ is not None:
            file_name = file_.name.split('.')[0].replace(' ','_')  if file_ is not None else None
            format_ = file_.name.split('.')[-1] if file_ is not None else None
            
            if format_ not in ["ifc", "dae", "glb"]:
                st.error("Please upload a valid file format: IFC, DAE, or GLB.", icon="❌")
            if format_ != 'glb':
                file_path, format_, check_ = convert(file_, output_path = f'./Archive/{file_name}', output_name = f'{file_name}_base', format='glb')
                st.success(f"""GLB file is created.""", icon="✅")
            elif format_ == 'glb':
                os.chdir(st.session_state.cwd)
                
                if file_name.split('_')[-1] == 'base':
                    folder_name = file_name[:-5]
                    os.makedirs(f'Archive/{folder_name}', exist_ok=True)
                    
                else:
                    folder_name = file_name
                    os.makedirs(f'Archive/{folder_name}', exist_ok=True)
                
                with open(f'./Archive/{folder_name}/{folder_name}_base.glb', "wb") as f:
                    f.write(file_.getbuffer())
                file_path = f'./Archive/{folder_name}/{folder_name}_base.glb'
                format_ = 'glb'
                check_ = True
                
                st.success(f"""GLB file is uploaded.""", icon="✅")
            else:
                st.error("Please upload a valid file format: IFC, DAE, or GLB.", icon="❌")

    #except:
    #    os.chdir(st.session_state.cwd)
        
with c2:
    c121, c122 = st.columns([3, 1])
    with c121:
        transparency = st.slider("Transparency", min_value=0.0, max_value=1.0, value=0.5, step=0.1, key="transparency")
    with c122:
        vis_ = st.button("Visualize", type="primary", disabled = not check_, key="use_file")
    
with c1:
    try:
        st.write(vis_)
        st.write(check_)
        if vis_ == True:
            # Check if the file is a valid 3D model format
            html = display(file_path, transparency=transparency)
            st.components.v1.html(html, height=520)
    except:
        os.chdir(st.session_state.cwd)
        pass

os.chdir(st.session_state.cwd)

#st.write(file_path)
if st.button("Generate ➡️", type="primary", disabled = not check_):
    # Switch to the Generator page
    st.switch_page("pages/Generator.py")