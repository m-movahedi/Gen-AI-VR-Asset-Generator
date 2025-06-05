import subprocess
import os
import shutil

def convert(file_, output_path='./temp', output_name = 'temp', format ='glb'):
    """
    Convert a 3D model file to GLB format using IfcConvert.
    
    Parameters:
    - input_file: Path to the input 3D model file (IFC, DAE, or GLB).
    - output_file: Path to save the converted GLB file.
    
    Returns:
    - str: Path to the converted GLB file.
    """
    import subprocess
    import os
    import shutil
    cwd = os.getcwd()
    try:
        # Ensure the temp directory exists
        os.makedirs('temp', exist_ok=True)
        file_name = file_.name.split('.')[0].replace(' ','_')
        os.makedirs(f'Archive/{file_name}', exist_ok=True)
        with open(f'./temp/{file_.name}', "wb") as f:
            f.write(file_.getbuffer())
        with open(f'./Archive/{file_name}/{file_.name}', "wb") as f:
            f.write(file_.getbuffer())
        # Copy files to temp directory
        shutil.copy('./Utils/IfcConvert.exe', './temp/IfcConvert.exe')
        
        # Change to temp directory
        os.chdir('./temp')

        # Prepare the command for conversion
        command = ['IfcConvert', f'{file_.name}', f'temp.{format}','-y', '--use-element-guids']
        try:
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except subprocess.CalledProcessError as e:
            return(e.stderr)
        os.chdir(cwd)
        shutil.copy(f'./temp/temp.{format}', f'{output_path}/{output_name}.{format}')
    except Exception as e:
        print(f"An error occurred during conversion: {e}")
    os.chdir(cwd)  # Adjust path as necessary
    

    return(f'{output_path}/{output_name}.{format}', format, True)  # Return the file path, format, and check status



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