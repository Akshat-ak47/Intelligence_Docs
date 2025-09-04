from backend.agents.base_agent import BaseAgent
from backend.services.llm_service import chat
from backend.services.embeddings_service import embeddings_service
from backend.utils.langsmith_stub import log_agent_event

class QnAAgent(BaseAgent):
    def run(self, doc_id: str, query: str, doc_text: str = None):
        contexts = embeddings_service.search(query, k=3)
        if contexts:
            context_text = '\n\n---\n\n'.join([c['content'] for c in contexts])
            prompt = f"Use the following context to answer precisely. If the answer is unknown from the context, say 'I don't know'.\n\nCONTEXT:\n{context_text}\n\nQuestion: {query}\nAnswer:"
            ans = chat('Document Q&A', prompt, max_tokens=400)
            log_agent_event('qa_agent', {'doc_id': doc_id, 'query': query}, {'found_contexts': len(contexts)})
            return {'answer': ans, 'source': 'pgvector' if contexts else 'none'}
        if doc_text and query.lower() in doc_text.lower():
            idx = doc_text.lower().find(query.lower())
            start = max(0, idx-200)
            end = min(len(doc_text), idx+200)
            snippet = doc_text[start:end]
            prompt = f"Use the snippet to answer. Snippet:\n{snippet}\nQuestion: {query}\nAnswer:"
            ans = chat('Document Q&A fallback', prompt, temperature=0.0)
            return {'answer': ans, 'source': 'document_snippet'}
        return {'answer': "I don't know based on the provided documents.", 'source': 'none'}
