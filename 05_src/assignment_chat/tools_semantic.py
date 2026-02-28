import chromadb
from chromadb.utils import embedding_functions
from langchain_core.tools import tool
from faq_data import faq_data


client = chromadb.Client(
    chromadb.config.Settings(
        persist_directory="./chroma_db",
        is_persistent=True
    )
)

embedding_function = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="faq_collection",
    embedding_function=embedding_function
)

# Populate only once
if collection.count() == 0:
    for i, item in enumerate(faq_data):
        collection.add(
            documents=[item["question"]],
            metadatas=[{"answer": item["answer"]}],
            ids=[str(i)]
        )


@tool
def semantic_faq_search(query: str) -> str:
    """
    Performs semantic search on campus FAQ dataset.
    """

    results = collection.query(
        query_texts=[query],
        n_results=1
    )

    if not results["documents"]:
        return "I couldn't find anything relevant in the campus database."

    answer = results["metadatas"][0][0]["answer"]

    return f"Here’s what I found in the campus FAQ records:\n\n{answer}"