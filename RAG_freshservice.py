from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import StateGraph, START, END
from typing import List, TypedDict, Any, Dict
from dotenv import load_dotenv

load_dotenv()


class RAGState(TypedDict):
    query:str
    docs: List[str]
    retrieved : List[Dict]
    answer: str
    citations: List[Dict]
    confidence: float

def retriever(state: RAGState) -> RAGState:
    query = state['query']
    results = vectorstore.similarity_search_with_score(query, k=4)
    state['retrieved'] = [{'doc':d.page_content, 'meta':d.metadata, 'score': s} for d,s in results]

    return state

def LLM(state:RAGState) -> RAGState:
    context = ""
    for i, r in enumerate(state['retrieved']):
        context += f"\n---\nSource {i+1}: {r['meta']['heading']} ({r['meta']['url']})\n{r['doc']}"

    prompt = f"""
You are an assistant for answering question about the Fresherservice API.
Answer ONLY using the provided documentation context. If answer not found, say so.
Context:
{context}

Question: {state['query']}

Anwer format:
1. Final Answer
2. Explanation of relevant parameters
3. Citations (URLs)
4. Confidence (0-1)
"""
    resp = llm.invoke(prompt)

    state['answer'] = resp.content
    state['citations'] = [r['meta'] for r in state['retrieved']]
    state['confidence'] = 1 - (sum([r["score"] for r in state["retrieved"]])/len(state['retrieved']))

    return state


def build_rag_graph(vectorstore, llm):
    graph = StateGraph(RAGState)

    graph.add_node('retriever', retriever)
    graph.add_node('llm', LLM)

    graph.add_edge(START,'retriever')
    graph.add_edge('retriever','llm')
    graph.add_edge('llm', END)

    return graph.compile()


if __name__ == "__main__":

    llm = ChatOpenAI(model = 'gpt-4o-mini')

    embeddings = OpenAIEmbeddings(model='text-embedding-3-small')

    vectorstore = Chroma(
    collection_name="freshservice",
    embedding_function=embeddings,
    persist_directory="./chroma_freshservice"
    )

    rag = build_rag_graph(vectorstore, llm)

    #Example
    query = "Give me the curl command to create a ticket"
    #query = "How do I create a new repository using the GitHub API?" 
    result = rag.invoke({'query': query, 'vectorstore':vectorstore, 'llm':llm})


    print("\n-----Final Answer-------")
    print(result['answer'])
    print("\n-----Citations-----------")
    print(result['citations'])
    print('-\n-------Confidence---------')
    print(result['confidence'])