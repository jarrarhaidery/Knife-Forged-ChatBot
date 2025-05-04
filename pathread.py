from langchain_community.document_loaders import TextLoader
from pathlib import Path

file_path = Path("data/products.txt").resolve()
loader = TextLoader(str(file_path), encoding="utf-8")

try:
    documents = loader.load()
except Exception as e:
    print(f"❌ Failed to load file: {e}")
    exit(1)

print("✅ Loaded documents!")
