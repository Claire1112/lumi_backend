# from rag.retriever import retrieve_knowledge
from rag.retriever import retrieve_relevant_knowledge
from llm import get_llm

# =====================================================
# 使用 Lumi 原本的 Gemini LLM
# =====================================================
llm = get_llm()

def answer_with_rag(query: str):

    # =====================================================
    # 1. 從 Chroma 找相關知識
    # =====================================================

    # documents = retrieve_knowledge(query)
    documents = retrieve_relevant_knowledge(query)

    if not documents:
        return {
            "answer": None,
            "sources": []
        }


    # =====================================================
    # 2. 把 Retrieved Documents 整理成文字
    # =====================================================

    knowledge_text = "\n\n".join(
        doc.page_content
        for doc in documents
    )


    # =====================================================
    # 3. Prompt
    # =====================================================

    prompt = f"""
你是 Lumi，一個日常身心調養助理。

請根據下面提供的 Lumi Knowledge Base 回答使用者。

規則：
1. 優先使用 Knowledge Base 中提供的資訊。
2. 不要自行加入 Knowledge Base 沒有提供的具體健康建議。
3. 回答自然、簡短、容易理解。
4. 不需要告訴使用者你正在使用 RAG 或知識庫。
5. 如果提供的知識無法回答問題，請直接表示目前沒有足夠資訊。

====================
Knowledge Base
====================

{knowledge_text}

====================
User
====================

{query}

====================
Lumi
====================
"""


    # =====================================================
    # 4. Gemini Generation
    # =====================================================

    response = llm.invoke(prompt)


    # =====================================================
    # 5. Source
    # =====================================================

    sources = list({
        doc.metadata.get("source")
        for doc in documents
        if doc.metadata.get("source")
    })

    # =====================================================
    # 取出 Gemini 真正的文字回答
    # =====================================================

    if isinstance(response.content, list):

        answer = "".join(
            block.get("text", "")
            for block in response.content
            if isinstance(block, dict) and block.get("type") == "text"
        )

    else:
        answer = str(response.content)


    return {
        "answer": answer,
        "sources": sources
    }


# =====================================================
# Test
# =====================================================

if __name__ == "__main__":

    test_questions = [
        "我讀書一直分心，腦袋很多想法，有什麼方法？",
        "高雄明天天氣如何？"
    ]

    for question in test_questions:

        result = answer_with_rag(question)

        print("\n==============================")
        print("RAG Answer")
        print("==============================")

        print("\nQuestion:")
        print(question)

        print("\nAnswer:")
        print(result["answer"])

        print("\nSources:")
        for source in result["sources"]:
            print("-", source)