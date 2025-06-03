def display(address= './temp/temp.glb', transparency=0.5):
    import base64
    from pygltflib import GLTF2, Material, BLEND
    glb = GLTF2().load(address)
    for mat in glb.materials:
        mat.alphaMode = BLEND  # Enable transparency
        # Get current color or default to white
        color = mat.pbrMetallicRoughness.baseColorFactor or [1.0, 1.0, 1.0, 1.0]
        # Update only the alpha (opacity) value
        color[3] = transparency  # 0.0 = fully transparent, 1.0 = fully opaque
        mat.pbrMetallicRoughness.baseColorFactor = color
            
    glb.save(f'./temp/temp_{int(transparency*10)}.glb')

    with open(f'./temp/temp_{int(transparency*10)}.glb', "rb") as f:
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
    return(html)