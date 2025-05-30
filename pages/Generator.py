import streamlit as st

#st.write(st.session_state.openai_api_key)
#st.write(st.session_state.gemini_api_key)

# Set the title of the page
st.set_page_config(page_title="Generator ⚙️", page_icon="⚙️", layout="wide", initial_sidebar_state='collapsed')

import os
st.write( os.getcwd().replace('\\', '/'))