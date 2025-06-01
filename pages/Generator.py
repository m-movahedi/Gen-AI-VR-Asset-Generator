import streamlit as st

#st.write(st.session_state.openai_api_key)
#st.write(st.session_state.gemini_api_key)

# Set the title of the page
st.set_page_config(page_title="Generator ⚙️", page_icon="⚙️", layout="wide", initial_sidebar_state='collapsed')

import os
st.write( os.getcwd().replace('\\', '/'))
import base64

# Read .glb file and convert to base64 for embedding
try:
    with open(".temp/temp.glb", "rb") as f:
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
with open(".temp/temp.glb", "rb") as f:
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