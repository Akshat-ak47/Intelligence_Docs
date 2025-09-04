import streamlit as st
import os
import requests

API = os.getenv('API_URL', 'http://localhost:8000')

st.set_page_config(page_title='Doc Intelligence', layout='wide')
st.title('Intelligent Document Summarization & Q&A (Azure single-deploy + pgvector + MCP)')

st.sidebar.header('Upload')
uploaded = st.sidebar.file_uploader('Upload PDF/DOCX/TXT', type=['pdf','docx','txt'])
if uploaded:
    if st.sidebar.button('Upload & Process'):
        files = {'file': (uploaded.name, uploaded.getvalue())}
        with st.spinner('Uploading & running pipeline...'):
            r = requests.post(f"{API}/ingest/upload/", files=files)
        if r.status_code == 200:
            st.success('Processed')
            res = r.json().get('result')
            if res:
                st.header('Summary')
                st.write(res.get('summary', 'No summary available'))
                st.header('Entities (sample)')
                st.write(res.get('entities', [])[:40])
                st.header('Validation')
                st.write(res.get('validation', {}))
            else:
                st.write(r.json())
        else:
            st.error(r.text)

st.sidebar.header('Docs')
if st.sidebar.button('List docs'):
    r = requests.get(f"{API}/docs")
    if r.status_code == 200:
        st.write(r.json())
    else:
        st.error(r.text)

st.header('Q&A')
doc_id = st.text_input('Doc ID (filename without extension)')
query = st.text_input('Question')
if st.button('Ask'):
    if not doc_id or not query:
        st.error('Provide doc id and a question')
    else:
        r = requests.post(f"{API}/qa/", data={'doc_id': doc_id, 'query': query})
        if r.status_code == 200:
            st.write(r.json())
        else:
            st.error(r.text)

st.header('External Search (MCP Search Server)')
q = st.text_input('Query for external search')
if st.button('Search Web'):
    if q:
        r = requests.get(f"{API}/search-external/", params={'q': q})
        if r.status_code == 200:
            st.write(r.json())
        else:
            st.error(r.text)
