import streamlit as st
import os 

st.set_page_config(page_title="Select model", page_icon="🗃️", layout="wide", initial_sidebar_state='collapsed')

st.title("Select model 🗃️")
check_apis = False

file = st.file_uploader("Upload your model file", type=["ifc","dae"], key="model_file")
if file is not None:
    os.chdir(st.session_state.cwd)
    format_ = file.name.split('.')[-1]
    os.makedirs('temp', exist_ok=True)
    with open(f"./temp/temp.{format_}", "wb") as binary_file: 
        binary_file.write(file.getvalue())
    st.success(f"File {file.name} uploaded successfully!", icon="✅")
    if format_ == "ifc":
        from Utils.utils import convert_ifc
        st.session_state.ifc_file = "./temp/temp.ifc"
        try:
            dae_file = convert_ifc("./temp/temp.ifc")
            st.success(f"File converted successfully!", icon="✅")
            check_apis = True
        except:
            st.error("Error converting to DAE. Please check the file and try again.", icon="❌")
    else:
        check_apis = True

    st.session_state.file_path = f"./temp/temp.dae"

os.chdir(st.session_state.cwd)

if st.button("Generate ➡️", type="primary", disabled = not check_apis):
    # Switch to the Generator page
    st.switch_page("pages/Generator.py")