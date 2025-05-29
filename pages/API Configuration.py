import streamlit as st
st.set_page_config(page_title="API Configuration", page_icon="🖥️", initial_sidebar_state='collapsed')

st.title("API Configuration 🖥️")
openai = st.text_input("OpenAI API Key", type="password", placeholder="Enter your OpenAI API Key here")
gemeni = st.text_input("Gemini API Key", type="password", placeholder="Enter your Gemini API Key here")
check_apis = False

st.session_state.openai_api_key = openai
st.session_state.gemini_api_key = gemeni

if openai and gemeni:
    # Save the API keys to a file or environment variable
    st.success("API Keys are set successfully!")
    # Set a flag to indicate that the API keys are configured
    check_apis = True
    # Here you can add code to save the keys securely, e.g., in a config file or environment variable
else:
    st.warning("Please enter both OpenAI and Gemini API keys to proceed.")

st.markdown('#')
c1, c2= st.columns(2)
with c1:
    if st.button("⬅️ Home", type="secondary"):
        # Switch to the API configuration page
        st.switch_page("Home.py")

with c2:
    if st.button("Generate ➡️", type="primary", disabled = not check_apis):
        # Switch to the Generator page
        st.switch_page("pages/Generator.py")