#!/bin/bash

docker compose up -d pgvector
sleep 4
uvicorn mcp.servers.file_server:app --reload --port 9000 &
uvicorn mcp.servers.search_server:app --reload --port 9001 &
uvicorn backend.main:app --reload --port 8000 &
streamlit run ui/app.py --server.port 8501
