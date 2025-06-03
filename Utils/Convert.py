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
        
        with open(f'./temp/{file_.name}', "wb") as f:
            f.write(file_.getbuffer())
        # Copy files to temp directory
        shutil.copy('./Utils/IfcConvert.exe', './temp/IfcConvert.exe')
        
        # Change to temp directory
        os.chdir('./temp')

        # Prepare the command for conversion
        command = ['IfcConvert', f'./temp/{file_.name}', f'{output_path}/{output_name}.{format}']
        subprocess.run(command, check=True)
        try:
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except subprocess.CalledProcessError as e:
            return(e.stderr)
    except:
        os.chdir(cwd)  # Adjust path as necessary

    return(f'{output_path}/{output_name}.{format}', format) 
