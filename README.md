# Intelligence_Docs

⚙️ 1. Prerequisites

Windows 10/11 with PowerShell

Python 3.10+ installed → check with:

python --version


Docker Desktop installed and running (for Postgres + pgvector).

📥 2. Setup the Project
2.1 Extract the Project

Unzip the project folder somewhere, e.g. D:\My_Projj.

2.2 Create Virtual Environment

In PowerShell:

cd D:\My_Projj
python -m venv .venv
.venv\Scripts\activate

2.3 Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt

2.4 Install spaCy Model
pip install spacy
python -m spacy download en_core_web_sm
pip install fastapi
pip install python-multipart
pip install dotenv
pip install httpx
pip install pypdf
pip install python-docx
pip install openai
pip install streamlit
pip install uvicorn

🔑 3. Configure Environment Variables

Copy .env.example → .env and set your values:
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your-key>
AZURE_OPENAI_API_VERSION=2024-12-01
AZURE_OPENAI_DEPLOYMENT_NAME=<your-deployment-name>
POSTGRES_URL=postgresql+psycopg://langchain:langchain@localhost:6024/langchain
MCP_FILE_SERVER_URL=http://localhost:9000
MCP_SEARCH_SERVER_URL=http://localhost:9001
UPLOAD_DIR=uploaded_docs
VECTOR_COLLECTION=documents

🗄️ 4. Start Postgres with pgvector

Run Postgres + pgvector with Docker:
docker compose up -d
This starts Postgres on localhost:6024 with:
user: langchain
password: langchain
database: langchain

📡 5. Start MCP Servers

In one terminal (inside venv):
python mcp/servers/file_server.py

In another terminal:
python mcp/servers/search_server.py

🖥️ 6. Run Backend (FastAPI)
In a new terminal:
python -m uvicorn backend.main:app --reload --port 8000

Backend will be available at:
👉 http://localhost:8000

🎨 7. Run Frontend (Streamlit UI)
In a new terminal:
python -m streamlit run ui/app.py

Frontend will be available at:
👉 http://localhost:8501

🤖 8. How it Works
Upload documents → stored in uploaded_docs/ and embedded into Postgres (pgvector).
MCP file/search servers handle file access + search operations.
LangChain retrieves documents + embeddings from Postgres.
Azure OpenAI (chat + embeddings) powers the LLM responses.
AutoGen agents (Assistant + User Proxy) orchestrate conversations.
Frontend (Streamlit) provides a user interface.

🧪 9. Testing API (Optional)
Check backend endpoints:
curl http://localhost:8000/health

🛑 10. Stop Everything
docker compose down


Then close the MCP + backend + UI terminals.
