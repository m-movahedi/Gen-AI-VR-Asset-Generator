import subprocess
import os
import shutil

def convert_ifc(ifc_file, format='glb'):
    cwd = os.getcwd()
    try:
        #make 
        ifc_file = ifc_file.replace('\\', '/')
        #temporary directory for conversion

        #os.makedirs('temp', exist_ok=True)
        try:
            shutil.copy('./Utils/IfcConvert.exe', f'./temp/IfcConvert.exe')
        except FileNotFoundError as e:
            return (e.stderr)
        
        # covnert ifc to dae using IfcConvert
        os.chdir('./temp')
        temp_file = f'./temp/{ifc_file.split("/")[-1]}'
        command = ['IfcConvert', 'temp.ifc', f'temp.{format}']
        try:
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except subprocess.CalledProcessError as e:
            return(e.stderr)
        
    except FileNotFoundError as e:
        os.chdir(cwd)
        return ('overall', e)
    
    #change back to the original directory
    os.chdir(cwd)
