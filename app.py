import streamlit as st

# app config
st.set_page_config(page_title="greengreenguesthouse", page_icon=":house_with_garden:")

pages = {
    " ": [
        st.Page("gg2.py", title="Greengreen AI assistant"),
    ],
    "Guest Information": [
        st.Page("about.py", title="About"),
        st.Page("contactInfo.py", title="Contact Info"),
        st.Page("guesthouseInfo.py", title="Guesthouse Info")
    ],
    
     "Resort Information ": [
        st.Page("resortInfo.py", title="Local Resorts"),
        st.Page("resortComparison.py", title="Resort Comparison"),
        #st.Page("guesthouseInfo.py", title="Guesthouse Info")
    ],
     
}

pg = st.navigation(pages)
pg.run()