from pathlib import Path
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma


load_dotenv()


# =====================================================
# 路徑設定
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "chroma_db"

# =====================================================
# RAG 設定
# =====================================================

RELEVANCE_THRESHOLD = 0.52

# =====================================================
# Embedding Model
# 必須跟 build_index.py 使用相同的 embedding model
# =====================================================

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)


# =====================================================
# 載入 Chroma DB
# =====================================================

vectorstore = Chroma(
    collection_name="lumi_knowledge",
    embedding_function=embeddings,
    persist_directory=str(CHROMA_DIR)
)


# =====================================================
# 建立 Retriever
# =====================================================

retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 1
    }
)


# =====================================================
# 一般 Retrieval
# 給 rag_service.py 使用
# =====================================================

def retrieve_knowledge(query: str):
    """
    根據使用者的問題，
    從 Lumi Knowledge Base 找相關資料。
    """

    documents = retriever.invoke(query)

    return documents


# =====================================================
# 帶 Relevance Score 的 Retrieval
# 目前用來測試 Threshold
# =====================================================

def retrieve_knowledge_with_score(query: str, k: int = 3):
    """
    搜尋相關知識，
    同時取得每個結果的 relevance score。
    """

    results = vectorstore.similarity_search_with_relevance_scores(
        query,
        k=k
    )

    return results

def retrieve_relevant_knowledge(query: str, k: int = 1):
    """
    搜尋 Lumi Knowledge Base。

    只有 relevance score >= threshold 的資料
    才會被視為相關知識。
    """

    results = vectorstore.similarity_search_with_relevance_scores(
        query,
        k=k
    )

    relevant_documents = []

    for doc, score in results:

        if score >= RELEVANCE_THRESHOLD:
            relevant_documents.append(doc)

    return relevant_documents


# =====================================================
# 測試
# =====================================================

if __name__ == "__main__":

    test_questions = [
        # 應該相關
        "我讀書一直分心，腦袋很多想法",
        "我躺在床上但整個人靜不下來",
        "我想跟著固定的吸氣吐氣節奏練習",

        # 應該不相關
        "高雄明天天氣如何？",
        "Python 怎麼寫 for loop？",
        "今天晚餐吃什麼？"
    ]

    for question in test_questions:

        print("\n==============================")
        print("Query:")
        print(question)
        print("==============================")

        results = retrieve_knowledge_with_score(
            question,
            k=3
        )

        for i, (doc, score) in enumerate(results):

            print(f"\n----- Result {i + 1} -----")
            print("Score:", round(score, 4))
            print("Source:", doc.metadata.get("source"))