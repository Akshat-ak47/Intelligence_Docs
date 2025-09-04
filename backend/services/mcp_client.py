from backend.config import MCP_FILE_SERVER_URL, MCP_SEARCH_SERVER_URL
import httpx
from backend.utils.logger import get_logger
logger = get_logger(__name__)

class MCPClient:
    def __init__(self, file_url=MCP_FILE_SERVER_URL, search_url=MCP_SEARCH_SERVER_URL):
        self.file_url = file_url
        self.search_url = search_url
        self.client = httpx.Client(timeout=30.0)

    def upload_file(self, filename: str, data: bytes):
        files = {'file': (filename, data)}
        resp = self.client.post(f"{self.file_url}/files", files=files)
        resp.raise_for_status()
        return resp.json()

    def list_files(self):
        resp = self.client.get(f"{self.file_url}/files")
        resp.raise_for_status()
        return resp.json()

    def read_file(self, filename: str):
        resp = self.client.get(f"{self.file_url}/files/{filename}")
        resp.raise_for_status()
        return resp.content

    def search(self, query: str):
        resp = self.client.get(f"{self.search_url}/search", params={'q': query})
        resp.raise_for_status()
        return resp.json()

mcp_client = MCPClient()
