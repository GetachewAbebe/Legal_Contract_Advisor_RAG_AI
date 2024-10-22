from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader
from dotenv import load_dotenv
import sys
sys.path.insert(1, '/home/getachew/Documents/10_Academy/Week_11/Legal_Contract_Advisor_RAG_AI')
load_dotenv()
def doc_loader(file_path):
    loader = Docx2txtLoader(file_path)
    docs = loader.load()
    return docs
def text_splitter(docs):    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    return vectorstore