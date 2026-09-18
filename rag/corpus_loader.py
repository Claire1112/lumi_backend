import hashlib
import json
from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_corpus(path):
    documents, ids = [], set()
    for line_number, line in enumerate(Path(path).read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        for key in ('id', 'category', 'topic', 'question', 'content', 'source', 'source_type'):
            if not row.get(key):
                raise ValueError(f'Invalid {key} at line {line_number}')
        if row['id'] in ids:
            raise ValueError(f'Duplicate record ID at line {line_number}')
        ids.add(row['id'])
        if row.get('ingestion_allowed') is not True:
            continue
        # The A–E symptom/point mapping is an unvalidated design, not answerable health knowledge.
        if row.get('evidence_status') == 'unvalidated_project_design':
            continue
        metadata = {k: v for k, v in row.items()
                    if k not in ('content', 'page_content') and isinstance(v, (str, int, float, bool))}
        metadata['source'] = json.dumps(row['source'], ensure_ascii=False)
        metadata['tags'] = json.dumps(row.get('tags', []), ensure_ascii=False)
        documents.append(Document(page_content=row.get('page_content') or row['content'], metadata=metadata))
    if not documents:
        raise ValueError('No permitted corpus records')
    return documents

def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=150,
        separators=['\n\n', '\n', '。', '！', '？', '；', '，', ' ', ''])
    chunks = []
    for doc in documents:
        pieces = splitter.split_documents([doc])
        for index, piece in enumerate(pieces):
            piece.metadata.update(parent_id=doc.metadata['id'], chunk_index=index,
                                  chunk_id=f"{doc.metadata['id']}:{index}")
            if len(pieces) > 1:
                piece.page_content += '\n證據限制：' + doc.metadata.get('evidence_notes', '')
                piece.page_content += '\n來源：' + doc.metadata['source']
        chunks.extend(pieces)
    return chunks
