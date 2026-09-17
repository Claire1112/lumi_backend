import os
from pathlib import Path
import shutil

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

from dotenv import load_dotenv

load_dotenv()

# =====================================================
# 路徑設定
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_DIR = BASE_DIR / "knowledge"
CHROMA_DIR = BASE_DIR / "chroma_db"


# =====================================================
# 1. 讀取 knowledge 裡面的 Markdown
# =====================================================

documents = []

for file_path in KNOWLEDGE_DIR.rglob("*.md"):

    print(f"讀取語料：{file_path}")

    text = file_path.read_text(
        encoding="utf-8"
    )

    document = Document(
        page_content=text,
        metadata={
            "source": str(file_path.relative_to(KNOWLEDGE_DIR)),
            "filename": file_path.name
        }
    )

    documents.append(document)


print(f"\n共讀取 {len(documents)} 份文件")


# =====================================================
# 2. Chunk
# =====================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=80
)

chunks = text_splitter.split_documents(documents)

print(f"切成 {len(chunks)} 個 chunks")


# =====================================================
# 3. Gemini Embedding
# =====================================================

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

# =====================================================
# 4. 清除舊的 Chroma DB
# 避免重新 build 時產生重複資料
# =====================================================

if CHROMA_DIR.exists():
    print("\n清除舊的 Chroma DB...")
    shutil.rmtree(CHROMA_DIR)

# =====================================================
# 5. 建立新的 Chroma DB
# =====================================================

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="lumi_knowledge",
    persist_directory=str(CHROMA_DIR)
)


print("\n==============================")
print("Lumi RAG 建立完成")
print("==============================")

for i, chunk in enumerate(chunks):

    print(f"\nChunk {i + 1}")
    print("Source:", chunk.metadata["source"])
    print(chunk.page_content[:200])