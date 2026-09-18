from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from rag.index_config import BASE_DIR, read_index_settings

load_dotenv(BASE_DIR / '.env')
settings = read_index_settings()
CHROMA_DIR = settings['directory']
RELEVANCE_THRESHOLD = 0.52
embeddings = GoogleGenerativeAIEmbeddings(model=settings['embedding_model'])
vectorstore = Chroma(collection_name=settings['collection_name'],
                    embedding_function=embeddings, persist_directory=CHROMA_DIR)
retriever = vectorstore.as_retriever(search_kwargs={'k': 4})

def retrieve_knowledge(query: str):
    return retriever.invoke(query)

def retrieve_knowledge_with_score(query: str, k: int = 4):
    return vectorstore.similarity_search_with_relevance_scores(query, k=k)

def retrieve_relevant_knowledge(query: str, k: int = 4):
    # Threshold preserved from the original project; recalibrate after retrieval evaluation.
    return [doc for doc, score in retrieve_knowledge_with_score(query, k)
            if score >= RELEVANCE_THRESHOLD]
