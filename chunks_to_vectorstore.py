from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
from dotenv import load_dotenv

load_dotenv()

# Embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Persistent Chroma store
persist_dir = "./chroma_freshservice"

vectorstore = Chroma(
    # collection_name="freshservice",
    collection_name="github",
    embedding_function=embeddings,
    persist_directory=persist_dir
)

# Text splitter
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

total_chunks = 0

with open("github_docs.jsonl", 'r', encoding='utf8') as f:
    for line in f:
        if not line.strip():
            continue
        doc = json.loads(line.strip())
        chunks = splitter.split_text(doc["text"])

        documents = [
            Document(
                page_content=chunk,
                metadata={
                    "url": doc["url"],
                    "heading": doc["heading"],
                    "chunk_index": i
                }
            )
            for i, chunk in enumerate(chunks)
        ]

        if documents:
            vectorstore.add_documents(documents)
            total_chunks += len(documents)

print(f"Ingested {total_chunks} chunks into Chroma")
print("Number of documents stored:", vectorstore._collection.count())
