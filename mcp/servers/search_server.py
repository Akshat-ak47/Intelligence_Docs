from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
app = FastAPI(title='MCP SearchOps')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

SEARCH_URL = 'https://duckduckgo.com/html/'

@app.get('/search')
async def search(q: str = Query(..., min_length=1)):
    try:
        headers = {'User-Agent': 'MCP-Search'}
        resp = requests.get(SEARCH_URL, params={'q': q}, headers=headers, timeout=10)
        resp.raise_for_status()
        return {'query': q, 'snippet': resp.text[:800]}
    except Exception as e:
        return {'error': str(e)}
