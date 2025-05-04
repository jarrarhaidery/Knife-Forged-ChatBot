# ingest.py
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader  # Correct import
from dotenv import load_dotenv
from pathlib import Path
import os

# Load .env variables
load_dotenv()

# Get API key from environment
api_key = os.getenv("GOOGLE_API_KEY")

# Get absolute path to the products.txt file
file_path = Path("data/products.txt").resolve()
print(f"📄 Loading file from: {file_path}")

# Try loading the file
try:
    loader = TextLoader(str(file_path), encoding="utf-8")  # Explicitly set encoding
    documents = loader.load()
except Exception as e:
    print(f"❌ Failed to load file: {e}")
    exit(1)

# Split text into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs = splitter.split_documents(documents)

# Use Gemini embedding with API key
embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=api_key
)

# Create and save FAISS vector DB
db = FAISS.from_documents(docs, embedding)
db.save_local("faiss_index")

print("✅ Ingested and saved to FAISS")
