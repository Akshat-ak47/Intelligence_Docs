from dotenv import load_dotenv
import os
load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT', '')
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY', '')
AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION', '2024-12-01')
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', '')

POSTGRES_URL = os.getenv('POSTGRES_URL', 'postgresql+psycopg://langchain:langchain@localhost:6024/langchain')

MCP_FILE_SERVER_URL = os.getenv('MCP_FILE_SERVER_URL', 'http://localhost:9000')
MCP_SEARCH_SERVER_URL = os.getenv('MCP_SEARCH_SERVER_URL', 'http://localhost:9001')

UPLOAD_DIR = os.getenv('UPLOAD_DIR', 'uploaded_docs')
TMP_UPLOAD_DIR = os.getenv('TMP_UPLOAD_DIR', 'tmp_uploads')
VECTOR_COLLECTION = os.getenv('VECTOR_COLLECTION', 'documents')
