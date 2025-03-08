import streamlit as st
import pandas as pd

contact_info = {"Hosts":"Maki and Michael", "Email":"greengreenguesthouse@gmail.com",
               "Mobile":"81 90 7210 2046", "WhatsApp":"81 80 2569 3415",
               "Instagram":"@greengreenguesthouse","Address":"1836-1 Suginosawa, Myoko, Niigata, 949-2113"
               }

emergency_numbers = {"Fire/Ambulance":"119","Police":"110"}


contact_df = pd.DataFrame.from_dict(contact_info, orient='index',columns=["Contact"])

emergency_df = pd.DataFrame.from_dict(emergency_numbers, orient='index',columns=["Emergency Number"])

st.subheader("Contact Information",anchor=False)
st.table(contact_df)

st.subheader("Emergency Numbers",anchor=False)
st.table(emergency_df)
