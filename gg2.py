import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
#from langchain_openai import ChatOpenAI
from PIL import Image
#from dotenv import load_dotenv
import utils2

#load_dotenv()

logo = Image.open('logo.jpeg')
st.image(logo)

#session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hey! I'm your helpful greengreen chatbot, how may I be of assistance?"),
    ]
    
if "vector_store" not in st.session_state:
    st.session_state.vector_store = utils2.get_vector_store()


# conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# user input
user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    response = utils2.get_response(user_query, st.session_state.chat_history,st.session_state.vector_store)
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    #st.session_state.chat_history.append(AIMessage(content=response))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
         #st.write_stream(response)
         st.write(response)
    st.session_state.chat_history.append(AIMessage(content=response))
