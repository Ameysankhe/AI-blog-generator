import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv(dotenv_path="./config/.env")

llm = ChatGroq(model="llama-3.1-8b-instant")
