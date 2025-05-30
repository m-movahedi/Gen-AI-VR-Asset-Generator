import ifcopenshell
import ifcopenshell.geom
import trimesh




import subprocess

def convert_ifc_to_dae(ifc_file, dae_file_path):
    dae_file_path = dae_file_path.replace('\\', '/')
    ifc_file = ifc_file.replace('\\', '/')
    dae_file_path = f"{dae_file_path}/{ifc_file.split('.')[0]}.dae"
    command = ['./Utils/IfcConvert.exe', ifc_file, dae_file_path]
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        pass
        
