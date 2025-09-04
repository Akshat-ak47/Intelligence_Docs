from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import os

UPLOAD_DIR = os.getenv('UPLOAD_DIR', 'uploaded_docs')
os.makedirs(UPLOAD_DIR, exist_ok=True)
app = FastAPI(title='MCP FileOps')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

@app.post('/files')
async def upload_file(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(path, 'wb') as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {'message': 'uploaded', 'filename': file.filename}

@app.get('/files')
async def list_files():
    return {'files': os.listdir(UPLOAD_DIR)}

@app.get('/files/{filename}')
async def read_file(filename: str):
    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail='not found')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return Response(content=content, media_type='text/plain')
    except Exception:
        with open(path, 'rb') as f:
            data = f.read()
        return Response(content=data, media_type='application/octet-stream')
