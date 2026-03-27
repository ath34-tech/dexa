from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

def get_client():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    # Using llama-3.1-8b-instant as the fixed fast model for reliability
    model = os.getenv("GROQ_MODEL_NAME", "llama-3.1-8b-instant")
    return ChatGroq(model=model, temperature=0)

def chat(prompt: str)->str:
    client = get_client()
    prompt_template=ChatPromptTemplate.from_messages([("user","{prompt}")])
    chain=prompt_template|client|StrOutputParser()
    return chain.invoke({"prompt":prompt})
