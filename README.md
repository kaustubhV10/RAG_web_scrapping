# Freshservice (or any other website) API Question Answering with RAG and LangGraph

This project demonstrates an end-to-end **Retrieval-Augmented Generation (RAG)** system for answering questions about the **Freshservice API documentation** using a **Large Language Model (LLM)** and **vector embeddings**. The system scrapes API docs, processes them into a vectorstore, and uses a LangGraph-based RAG pipeline to answer queries with relevant citations.

**Project Overview:** Scraping fetches publicly accessible API documentation sections, Vectorstore Ingestion splits documentation into chunks, creates embeddings with OpenAI, and stores them in **Chroma**, RAG Pipeline retrieves relevant docs and generates answers with an LLM. Output returns answers, citations, and confidence scores.

**Setup Instructions:** Clone the repository: `git clone https://github.com/yourusername/freshservice-rag.git && cd freshservice-rag`. Create a virtual environment and install dependencies: `python -m venv myenv && source myenv/bin/activate # Linux/Mac or myenv\Scripts\activate.bat # Windows && pip install -r requirements.txt`. Set environment variables: `export OPENAI_API_KEY="your_openai_api_key" # Linux/Mac` or `setx OPENAI_API_KEY "your_openai_api_key" # Windows`.

**Usage:** Scrape API docs: `python scraper/scrape_freshservice.py` → produces `freshservice_docs.jsonl` containing `url`, `heading`, and `text`. Ingest docs into Chroma: `python ingestion/chunks_to_vectorstore.py` → splits docs into chunks (chunk size 500, overlap 50), generates embeddings using OpenAI (`text-embedding-3-small`), stores in Chroma with persistence. Query via RAG pipeline: `python rag_pipeline/RAG_freshservice.py` → output includes **Final Answer** (LLM-generated), **Citations** (retrieved docs), and **Confidence** (0-1).

**Dependencies:** `requests` (HTTP requests), `beautifulsoup4` (HTML parsing), `langchain` (LLM + embeddings), `langchain_chroma` (Chroma vectorstore), `langgraph` (RAG pipeline), `python-dotenv` (environment variable management).

**Notes:** Only public sections of Freshservice API docs are scrappable. Chroma vectorstore persists embeddings for repeated queries. RAG pipeline ensures contextual answers with citations and confidence scoring.
****
