import streamlit as st
import os 
from Utils.utils import display
import json
with open("./temp/session.json", "r") as f:
    session = json.load(f)

st.session_state.cwd = os.getcwd()
# Set the title of the page
st.set_page_config(page_title="Generator", page_icon="⚙️", layout="wide", initial_sidebar_state='collapsed')

st.title("Generator ⚙️")

c2, c1 = st.columns([1.5, 1])

with c1:
    c11, c12 = st.columns([1, 1.5])
    with c11:
        st.write("Select components:")
    with c12:
        import pandas as pd
        components = pd.read_csv(session['Components'])
        component_list = st.multiselect("Select components", options=components['GUID'].tolist(), label_visibility="collapsed", placeholder="Select components")

    c11, c12 = st.columns([1, 1.5])
    with c11:
        st.write("Select a Gen-AI model")
    with c12:
        texture_model = st.selectbox("Select a Gen-AI model", options=['gpt-image-1', 'dall-e-2'], label_visibility="collapsed", placeholder="Select a Gen-AI model")
        session['texture_model'] = texture_model
    c11, c12 = st.columns([1, 1.5])
    with c11:
        st.write("Choose knowledge base file:")
    with c12:
        knowledge_base_file = st.file_uploader("Upload a knowledge base file",
                                               type=["txt"],
                                               key="knowledge_base_file",
                                               label_visibility="collapsed")
        if knowledge_base_file is not None:
            # Save the uploaded file to a temporary location
            knowledge_path = f"./{session['path']}/{session['file_name']}_knowledge.txt"
            with open(knowledge_path, "wb") as f:
                f.write(knowledge_base_file.getbuffer())
            st.success(f"Knowledge base file '{knowledge_base_file.name}' uploaded successfully.", icon="✅")
            session['knowledge_base_file'] = knowledge_path
            session['knowledge_base']= knowledge_base_file.getbuffer()
    st.write("Additional description:")
    additional_info = st.text_input("Enter additional information (optional)", label_visibility="collapsed")
    st.write('Condition rating:')
    condition_rating = st.slider("Select condition rating", min_value=0, max_value=100, value=100, step=10, label_visibility="collapsed")
    generate_flag = st.button("Generate assets",
                              type="primary",
                              #disabled=not component_list or not texture_model or not knowledge_base_file
                              )
    component_indx = []
    for i in component_list:
        component_indx.append(components[components['GUID'] == i].index[0])
    #st.write(component_indx)
        

    if generate_flag:
        from Utils.utils import generate_image, load_image_from_gltf
        system_prompt = f"""You are a Gen-AI model that generates textures for 3D models based on the provided components and additional information.
                            The condition rating is based on the following scale:
                            {knowledge_base_file.getvalue().decode('utf-8') if knowledge_base_file else "0: New, 100: Deteriorated"}"""
        os.makedirs(f"./{session['path']}/Textures",  exist_ok=True)
        os.makedirs(f"./{session['path']}/Modified",  exist_ok=True)
        #st.progress(0, text="Generating assets...")
        temp_model_path = session['file_path']
        for component in component_indx:
            #st.write( components.loc[component]['GUID'])
            os.makedirs(f"{session['path']}/Textures/{components.loc[component]['GUID']}",  exist_ok=True)
            user_prompt = f"""Generate a texture image of the surface of a {components.loc[component]['Material']} material at condition rating index (CI) of {condition_rating} percent.
            Generate a texture that shows the surface condition of the material and can be applies to the 3D object in a glb file"""
            prompt = f"""{system_prompt}
                      {user_prompt}"""
            #os.makedirs(f"./{session['path']}/Textures/{components.loc[component]['GUID'][component]}",  exist_ok=True)
            temp = generate_image(  api_key = session['openai_api_key'],
                                    model  ="gpt-image-1",
                                    prompt = prompt,
                                    image_path= f"./{session['path']}/Textures/{components.loc[component]['GUID']}/{condition_rating}.png")
            
            load_image_from_gltf(   temp_model_path,
                                    png_path = f"./{session['path']}/Textures/{components.loc[component]['GUID']}/{condition_rating}.png",
                                    target_node_ids = components.loc[component]['GUID'],
                                    output_path= f"./{session['path']}/Modified/{session['file_name']}_{condition_rating}.glb",
                                    scale=[2, 3]) 
            temp_model_path = f"{session['path']}/Modified/{session['file_name']}_{condition_rating}.glb"
            #session['Modified_models'][str(condition_rating)] = temp_model_path
            #session['Rendered_models'][str(condition_rating)] = display(temp_model_path, transparency=1.0)
        

            
with c2:
    # Display the GLB file
    try:
        html = display(temp_model_path, transparency=1.0)
        st.components.v1.html(html, height=520)
    except:
        #st.components.v1.html(session['Rendered_models']['Base'], height=520)
        pass

#st.write(file_path)
if st.button("Visualize ➡️", type="primary"):
    # Switch to the Generator page
    st.switch_page("pages/Visualize.py")