import streamlit as st
import utils2

# app config
st.set_page_config(page_title="greengreenguesthouse", page_icon=":house_with_garden:")

logo = utils2.get_image('logo.jpeg')
st.image(logo)