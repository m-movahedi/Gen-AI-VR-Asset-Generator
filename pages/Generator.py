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
    file = trimesh.load(output_path)
else:
    output_path = f'./temp/{file.name}'
    format_ = 'dae'
    status_flag = True

if status_flag:
    import trimesh
    try:
        mesh = trimesh.load(output_path)
        st.success("3D model loaded successfully!")

        # Export it to glTF for browser visualization
        glb_path = output_path.replace('.dae', '.glb')
        mesh.export(glb_path)

        # Render using HTML component with Three.js viewer
        import base64
        with open(glb_path, "rb") as f:
            glb_bytes = f.read()
            encoded = base64.b64encode(glb_bytes).decode()

        viewer_html = f"""
        <model-viewer 
            src="data:model/gltf-binary;base64,{encoded}"
            alt="3D model"
            auto-rotate 
            camera-controls 
            background-color="#FFFFFF" 
            style="width: 100%; height: 500px;">
        </model-viewer>

        <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
        """
        st.components.v1.html(viewer_html, height=500)

    except Exception as e:
        st.error(f"Failed to load model: {e}")

    # Clean up
    #os.unlink(output_path)
