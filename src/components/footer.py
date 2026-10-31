import streamlit as st


def footer_home():


    st.markdown(f""" 

        <div style ="margin-top:2rem; display:flex; gap:6px; justify-content:center; align-item:center;" >
            <p style="font-weight:bold; color:white;">Created with ❤️ by vaishnavi</p>
    
        </div>
  
            """

    , unsafe_allow_html = True)

def footer_dashboard():

    # logo_url = "https://i.ibb.co/4r5X1FY/apnacollege.png"

    st.markdown(f""" 

        <div style ="margin-top:2rem; display:flex; gap:6px; justify-content:center; align-item:center;" >
            <p style="font-weight:bold; color:black;">Created with ❤️ by vaishnavi </p>

        </div>
  
            """

    , unsafe_allow_html = True)