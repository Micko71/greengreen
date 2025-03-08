#document loading and splitting
import json
from  langchain.schema import Document
from typing import Iterable
from langchain_text_splitters import RecursiveCharacterTextSplitter

#embedding
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain_community.vectorstores.faiss import FAISS

#chains
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

#from dotenv import load_dotenv

#load_dotenv() 


#function to load documents
def load_docs_from_jsonl(file_path)->Iterable[Document]:
    array = []
    with open(file_path, 'r') as jsonl_file:
        for line in jsonl_file:
            data = json.loads(line)
            obj = Document(**data)
            array.append(obj)
    return array

def get_vector_store(file_path='myoko_tourism_gg_data.json'):
    embeddings = OpenAIEmbeddings()
    docs=load_docs_from_jsonl(file_path)
    
    #chunk documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    
    #embed documents and create vectorstore
    vectorstore = FAISS.from_documents(splits, embeddings)
    
    return vectorstore

#Returns history_aware_retriever
def get_retreiver_chain(vector_store):
  llm = ChatOpenAI(model="gpt-4o-mini")
  retriever = vector_store.as_retriever()
  prompt = ChatPromptTemplate.from_messages([
      MessagesPlaceholder(variable_name="chat_history"),
      ("user","{input}"),
      ("user","Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
  ])
  history_aware_retriver = create_history_aware_retriever(llm,retriever,prompt)
  
  return history_aware_retriver

#Returns conversational rag
def get_conversational_rag(history_aware_retriver):
  llm = ChatOpenAI(model="gpt-4o-mini")
  system_prompt = (
    "You are a host for an airbnb style accommodation called Greengreen Guesthouse."
    "Greengreen Guesthouse is located in Suginosawa. Unless otherwise stated, assume guests are located here"
    "Use the following pieces of retrieved context to answer questions from guests."
    "If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)
  
  answer_prompt=ChatPromptTemplate.from_messages([
      ("system",system_prompt),
      MessagesPlaceholder(variable_name="chat_history"),
      ("user","{input}")
  ])

  document_chain = create_stuff_documents_chain(llm,answer_prompt)

  #create final retrieval chain
  conversational_retrieval_chain = create_retrieval_chain(history_aware_retriver,document_chain)

  return conversational_retrieval_chain

#Returns the final response
def get_response(user_input,chat_history,vector_store):
  #returns context aware retriever chain
  history_retriever_chain = get_retreiver_chain(vector_store)
  
  #returns final conversation chain
  conversation_rag_chain = get_conversational_rag(history_retriever_chain)

  response = conversation_rag_chain.invoke({
        "chat_history":chat_history,
        "input":user_input
    })
  return response["answer"]

  # return conversation_rag_chain.stream({
  #       "chat_history": chat_history,
  #       "input": user_input,
  # })
      
  

 
