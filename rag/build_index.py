"""Run from the project directory: python -m rag.build_index [--dry-run]."""
import argparse
from datetime import datetime, timezone
import json
import uuid
from dotenv import load_dotenv
from rag.corpus_loader import load_corpus, chunk_documents
from rag.index_config import BASE_DIR, SETTINGS_PATH, EMBEDDING_MODEL, COLLECTION_NAME

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='Validate and chunk without an API call')
    args = parser.parse_args()
    documents = load_corpus(BASE_DIR / 'knowledge' / 'lumi_rag' / 'corpus.jsonl')
    chunks = chunk_documents(documents)
    print(f'Loaded {len(documents)} records; prepared {len(chunks)} chunks')
    if args.dry_run:
        print('Validation complete. No embedding API call or database change.')
        return
    load_dotenv(BASE_DIR / '.env')
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    from langchain_chroma import Chroma
    # Build separately. Never delete the active or original database.
    name = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '_' + uuid.uuid4().hex[:8]
    directory = BASE_DIR / 'rag_indexes' / name
    directory.mkdir(parents=True, exist_ok=False)
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
    store = Chroma(collection_name=COLLECTION_NAME, embedding_function=embeddings,
                   persist_directory=str(directory))
    ids = [doc.metadata['chunk_id'] for doc in chunks]
    for start in range(0, len(chunks), 32):
        store.add_documents(chunks[start:start+32], ids=ids[start:start+32])
    stored = store.get(ids=ids, include=['metadatas'])
    if set(stored['ids']) != set(ids):
        raise RuntimeError('Incomplete index; active settings have not changed')
    # Switch only after all records are persisted. Restart backend after success.
    settings = {'directory': directory.relative_to(BASE_DIR).as_posix(),
                'embedding_model': EMBEDDING_MODEL, 'collection_name': COLLECTION_NAME,
                'record_count': len(documents), 'chunk_count': len(chunks)}
    temporary = SETTINGS_PATH.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(SETTINGS_PATH)
    print('New index activated. Restart the backend to load it. Original chroma_db retained.')

if __name__ == '__main__':
    main()
