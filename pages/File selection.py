import streamlit as st
import os 
import shutil
import json
with open("./temp/session.json", "r") as f:
    session = json.load(f)

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
    try:
        file_ = st.file_uploader("Upload your model file", type=["ifc","dae", 'glb'], key="model_file", label_visibility="collapsed")
        
        if file_ is not None:
            file_name = file_.name.split('.')[0].replace(' ','_')  if file_ is not None else None
            format_ = file_.name.split('.')[-1] if file_ is not None else None
            
            if format_ not in ["ifc", "dae", "glb"]:
                st.error("Please upload a valid file format: IFC, DAE, or GLB.", icon="❌")
            if format_ != 'glb':
                temp_format_ = format_
                file_path, format_, check_ = convert(file_, output_path = f'./Archive/{file_name}', output_name = f'{file_name}_base', format='glb')
                st.write(file_path)
                st.write(format_)
                st.success(f"""GLB file is created.""", icon="✅")
                if temp_format_ == 'ifc':   
                    #import pandas as pd
                    from Utils.utils import data_extraction
                    component = data_extraction(f'./Archive/{file_name}/{file_.name.split('.')[0]}.ifc')
                    os.chdir(st.session_state.cwd)
                    component.to_csv(f'./Archive/{file_name}/{file_name}_components.csv')
                    st.success(f"""Data file is uploaded.""", icon="✅")
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
                st.success(f"""GLB file is loaded.""", icon="✅")
                try:
                    import pandas as pd
                    component = pd.read_csv(f'./Archive/{folder_name}/{folder_name}_components.csv') 
                    st.success(f"""Data file is uploaded.""", icon="✅")
                except:
                    uploaded_file = st.file_uploader("Upload your data file", type=["csv"], key="model_file", label_visibility="collapsed")
                    if uploaded_file is not None:
                        df = pd.read_csv(uploaded_file)
                        df.to_csv(f'./Archive/{folder_name}/{folder_name}_components.csv', index=False)
                        st.success(f"""Data file is uploaded.""", icon="✅")

            else:
                st.error("Please upload a valid file format: IFC, DAE, or GLB.", icon="❌")

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
if check_:
    session['path'] = f'./Archive/{folder_name}'
    session['file_name'] = file_name[:-5] if file_name.split('_')[-1] == 'base' else file_name
    session['file_path'] = file_path
    session['format'] = format_
    session['Components'] = f'./Archive/{folder_name}/{session['file_name']}_components.csv'
    session['Models_Name'].append('Base')
    session['Models_Path'].append(file_path)
    #session['Rendered_models']['Base'] = display(file_path, transparency=1.0)
    #session['Modified_models']['Base'] = file_path
    with open("./temp/session.json", "w") as file:
         json.dump(session, file, indent=4) 

#st.write(file_path)
if st.button("Generate ➡️", type="primary", disabled = not check_):
    # Switch to the Generator page
    st.switch_page("pages/Generator.py")
    