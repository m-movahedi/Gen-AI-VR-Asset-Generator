import streamlit as st
import os 
import pandas as pd
st.session_state.cwd = os.getcwd()

import json
with open("./temp/session.json", "r") as f:
    session = json.load(f)

st.set_page_config(page_title="API Configuration", page_icon="🖥️", initial_sidebar_state='collapsed')

try:
    api_df = pd.read_csv('./temp/api_keys.csv')
    openai = api_df.loc[api_df['Service'] == 'OpenAI', 'API Key'].values[0]
    gemini = api_df.loc[api_df['Service'] == 'Gemini', 'API Key'].values[0]
    check_apis = True
except FileNotFoundError:
    openai = "Enter your OpenAI API Key here"
    gemini = "Enter your Gemini API Key here"

st.title("API Configuration 🖥️")
openai = st.text_input("OpenAI API Key", type="password", placeholder="Enter your OpenAI API Key here", value=openai if openai != "Enter your OpenAI API Key here" else "")
gemeni = st.text_input("Gemini API Key", type="password", placeholder="Enter your Gemini API Key here", value=gemini if gemini != "Enter your Gemini API Key here" else "")
check_apis = False

st.session_state.openai_api_key = openai
st.session_state.gemini_api_key = gemeni
api_dic = {}
if openai and gemeni:
    # Save the API keys to a file or environment variable
    st.success("API Keys are set successfully!")
    # Set a flag to indicate that the API keys are configured
    check_apis = True
    # Here you can add code to save the keys securely, e.g., in a config file or environment variable
    
    api_df = pd.DataFrame(columns=['Service', 'API Key'])
    api_df.loc[0] = ['OpenAI', openai]
    api_df.loc[1] = ['Gemini', gemeni]
    api_df.to_csv('./temp/api_keys.csv', index=False)
    api_dic ['openai_api_key'] = openai
    api_dic ['gemeni_api_key'] = gemini
    with open("./temp/session.json", "w") as file:
         json.dump(session, file, indent=4) 
    with open("./temp/API.json", "w") as file:
         json.dump(api_dic, file, indent=4) 
else:
    st.warning("Please enter both OpenAI and Gemini API keys to proceed.")

st.markdown('#')
c1, c2= st.columns(2)
with c1:
    if st.button("⬅️ Home", type="secondary"):
        # Switch to the API configuration page
        st.switch_page("Home.py")

with c2:
    if st.button("Select file ➡️", type="primary", disabled = not check_apis):
        # Switch to the Generator page
        st.switch_page("pages/File selection.py")
