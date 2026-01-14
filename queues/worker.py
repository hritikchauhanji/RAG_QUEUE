from ollama import Client
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore

client = Client(
    host="http://localhost:11434",
)

embeddings = OllamaEmbeddings(
    model="mxbai-embed-large:latest"
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",                              
    collection_name="learning_rag",
    embedding=embeddings
)

def process_queue(query: str):
    print("Searching Chunks", query)
    search_results = vector_db.similarity_search(query=query)
    context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}"
    for result in search_results])

    SYSTEM_PROMPT = f"""
    You are a helpful assistant AI Assistant who answers user query based on the available context retrieved from a PDF file along with page_contents and page number.

    You should only ans the user based on the following context and navigate the user to open the right page number to know more.

    Context: 
    {context}
    """

    response = client.chat(
        model="gemma:2b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    )
    return response.message.content
    print(f"🤖: {response.message.content}")