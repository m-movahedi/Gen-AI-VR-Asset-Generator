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

def data_extraction (file_path):
    import ifcopenshell
    file = ifcopenshell.open(file_path)

    import pandas as pd
    elements_with_ids = [el[0] for el in file.by_type("IfcRoot") if el.GlobalId]
    component = pd.DataFrame()
    component ['GUID'] = elements_with_ids

    def get_material_by_guid(id):
        
        # Check for material associations
        element = file.by_guid(id)
        try:
            type_= element.ObjectType
        except:
            type_ = "No type information available"
        material_desc = []
        try:
            for rel in element.HasAssociations:
                if rel.is_a("IfcRelAssociatesMaterial"):
                    material = rel.RelatingMaterial
                    
                    # Direct material
                    if material.is_a("IfcMaterial"):
                        material_desc.append('The material is ' + material)
                        
                    # Layered material
                    elif material.is_a("IfcMaterialLayerSetUsage"):
                        temp = ''
                        for layer in material.ForLayerSet.MaterialLayers:
                            temp =  f'{layer.Material.Name} with thickness {layer.LayerThickness} \n'
                        material_desc.append(temp)

                    elif material.is_a("IfcMaterialLayerSet"):
                        temp = ''
                        for layer in material.MaterialLayers:
                            temp =  f'{layer.Material.Name} with thickness {layer.LayerThickness} \n'
                        material_desc.append(temp)

                    elif material.is_a("IfcMaterialList"):
                        temp = 'multiple materails including: \n'
                        for mat in material.Materials:
                            temp =  f'{mat.Name} \n'
                        material_desc.append(temp)
                    elif material is None:
                        material_desc.append("No material is associated with this element")
                    else:
                        material_desc.append("No material is associated with this element")
                else:
                    material_desc.append("No material is associated with this element")
        except:
            material_desc.append("No material is associated with this element")
        return (material_desc, type_)


    component ['Material'] = None
    component ['Type'] = None
    i=0
    for id in elements_with_ids:
        material, type_ = get_material_by_guid(id)
        component.at[i,'Material'] = material
        component.at[i,'Type'] = type_
        i+=1
    return (component)

def load_image_from_gltf(glb_path, png_path, target_node_ids, output_path="test.glb", scale=[2, 3]):
    if type(target_node_ids) != list:
        target_node_ids = [target_node_ids]  # Ensure it's a list

    from pygltflib import GLTF2, Texture, Image, Material
    from PIL import Image as PILImage
    import base64
    gltf = GLTF2().load(glb_path)
    import pandas as pd
    glb_data = pd.DataFrame(gltf.nodes)

    # Load and encode the PNG image as base64
    with open(png_path, "rb") as f:
        image_data = f.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')

    # Create GLTF Image
    image = Image(uri="data:image/png;base64," + image_base64)
    image_index = len(gltf.images)
    gltf.images.append(image)

    # Create Texture
    texture = Texture(source=image_index)
    texture_index = len(gltf.textures)
    gltf.textures.append(texture)

    # Create Material
    material = Material(
        name="CustomMaterial",
        pbrMetallicRoughness={
            "baseColorTexture": {"index": texture_index,
                                 "extensions": {"KHR_texture_transform": {"scale": scale } # Tiling: 2x horizontal, 3x vertical
                                 }
        }}
    )
    #material.PBRMetallicRoughness = PBRMetallicRoughness
    material_index = len(gltf.materials)
    gltf.materials.append(material)

    # Example IDs; replace with your actual component IDs
    for node_id in target_node_ids:
        indx = glb_data[glb_data['name']==node_id].index
        node = gltf.nodes[indx[0]]
        if node.mesh is not None:
            mesh = gltf.meshes[node.mesh]
            for primitive in mesh.primitives:
                primitive.material = material_index
    # Save new GLB
    gltf.save(output_path)