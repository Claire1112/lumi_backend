import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS_PATH = BASE_DIR / 'rag' / 'index_settings.json'
EMBEDDING_MODEL = 'models/gemini-embedding-001'
COLLECTION_NAME = 'lumi_knowledge'

def read_index_settings():
    if not SETTINGS_PATH.exists():
        return {'directory': str(BASE_DIR / 'chroma_db'),
                'embedding_model': EMBEDDING_MODEL, 'collection_name': COLLECTION_NAME}
    settings = json.loads(SETTINGS_PATH.read_text(encoding='utf-8'))
    directory = (BASE_DIR / settings['directory']).resolve()
    if not directory.is_relative_to(BASE_DIR.resolve()):
        raise ValueError('Index directory must be inside the project')
    settings['directory'] = str(directory)
    return settings
