import shutil

# Path to your Chroma persist directory
persist_dir = "./chroma_freshservice"

# Delete the folder completely
shutil.rmtree(persist_dir)
print("✅ Vectorstore cleared from disk.")