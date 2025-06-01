import streamlit as st
st.set_page_config(page_title="Visualize", page_icon="👀", layout="wide", initial_sidebar_state='collapsed')

st.title("Visualize 👀")
st.markdown("This is a visualization of the generated 3D model.")
import base64
# Read .glb file and convert to base64 for embedding
try:
    with open("temp/temp.glb", "rb") as f:
            glb_data = f.read()
            glb_base64 = base64.b64encode(glb_data).decode("utf-8")

    # HTML using model-viewer
    html = f"""
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
    st.components.v1.html(html, height=520)
except FileNotFoundError:
    pass

with st.expander("Guide"):
    st.markdown("""
    1. **Upload your model file**: Use the File Selection page to upload your model file.
    2. **Generate the model**: Switch to the Generator page to generate the 3D model.
    3. **Visualize the model**: After generation, return to this page to view the 3D model.
    
    If you encounter any issues, please check the logs for errors.
    """)