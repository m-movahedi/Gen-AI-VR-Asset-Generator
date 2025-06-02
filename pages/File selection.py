import streamlit as st
import os 
st.session_state.cwd = os.getcwd()
import shutil
import easygui
st.set_page_config(page_title="Select model", page_icon="🗃️", layout="wide", initial_sidebar_state='collapsed')

def visualize (transparency):
    from pygltflib import GLTF2, Material, BLEND
        glb = GLTF2().load("temp/temp.glb")
        for mat in glb.materials:
            mat.alphaMode = BLEND  # Enable transparency
            # Get current color or default to white
            color = mat.pbrMetallicRoughness.baseColorFactor or [1.0, 1.0, 1.0, 1.0]
            # Update only the alpha (opacity) value
            color[3] = transparency  # 0.0 = fully transparent, 1.0 = fully opaque
            mat.pbrMetallicRoughness.baseColorFactor = color
                
        glb.save('temp/modified_glb.glb')

    import base64
    #st.write(f"./temp/{st.session_state.path.split('\\')[-1]}")
    with open("./temp/temp.glb", "rb") as f:
        glb_data = f.read()
        glb_base64 = base64.b64encode(glb_data).decode("utf-8")
        # HTML using model-viewer
        st.session_state.html = f"""
        <html>
        <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
        <model-viewer 
            src="data:model/gltf-binary;base64,{glb_base64}" 
            alt="A 3D model" 
            auto-rotate 
            camera-controls 
            style="width: 100%; height: 500px;">
        </model-viewer>
        </html>
        """
        # Display in Streamlit
        st.components.v1.html( st.session_state.html, height=520)

st.title("Select model 🗃️")
check_ = False
format_ = None
vis_ = False
st.session_state.path = None
file_absolut_path_check = False
c1, c2 = st.columns([1, 1])
with c2:
    c111, c112 = st.columns([3, 1])
    with c112:
        if st.button('Add model', type="primary", key="add_file"):
            st.session_state.path = easygui.fileopenbox(title='Add File', filetypes=["*.glb", "*.dae", "*.ifc"])
    with c111:
        if st.session_state.path is None:
            st.warning(" No file is selected", icon="⚠️")
        else:
            st.success(f"""Selected file:   {st.session_state.path}""", icon="✅")
    if st.session_state.path is not None:
        file_absolut_path_check = True

    c121, c122 = st.columns([3, 1])
    with c121:
        transparency = st.slider("Transparency", min_value=0.0, max_value=1.0, value=0.5, step=0.1, key="transparency", disabled = not file_absolut_path_check)
    with c122:
        vis_ = st.button("Visualize", type="primary", disabled = not file_absolut_path_check, key="use_file")

    # Check if the file is a valid 3D model format
    if st.session_state.path is not None:
        format_ = st.session_state.path.split('.')[-1]
        os.chdir(st.session_state.cwd)
        os.makedirs('temp', exist_ok=True)
        shutil.copy('./Utils/IfcConvert.exe', f'./temp/IfcConvert.exe')
        
        shutil.copy(st.session_state.path, f"./temp/{st.session_state.path.split('\\')[-1]}")
        if format_ != "glb":
            os.makedirs('temp', exist_ok=True)
            os.chdir('./temp')
            from Utils.utils import convert_ifc
            try:
                dae_file = convert_ifc(st.session_state.path.split('\\')[-1], format='glb')
                st.success(f"File converted successfully!", icon="✅")
                check_ = True
                st.session_state.path = "./temp/temp.glb"
                format_ = "glb"
            except:
                st.error("Error converting to DAE. Please check the file and try again.", icon="❌")
            os.chdir(st.session_state.cwd)
        else:
            shutil.copy(f"./temp/{st.session_state.path.split('\\')[-1]}", "./temp/temp.glb")
            st.success("File format is checked.", icon="✅")
            check_ = True
            st.session_state.path = "./temp/temp.glb"
with c1:
    try:
        visualize(transparency)
    except FileNotFoundError:
        st.error("No file found to visualize. Please upload a valid 3D model file.", icon="❌")
        

os.chdir(st.session_state.cwd)

if st.button("Generate ➡️", type="primary", disabled = not check_):
    # Switch to the Generator page
    st.switch_page("pages/Generator.py")