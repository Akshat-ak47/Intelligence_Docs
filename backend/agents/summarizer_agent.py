from backend.agents.base_agent import BaseAgent
from backend.services.llm_service import chat
from backend.utils.langsmith_stub import log_agent_event

class SummarizerAgent(BaseAgent):
    def run(self, doc_id: str, text: str) -> str:
        prompt = (
            "You are an expert document summarizer. Provide:\n"
            "1) Executive summary (3-5 sentences)\n"
            "2) Key bullet points (6-10)\n"
            "3) Short list of important named entities (names, dates, orgs).\n\n"
            "Document:\n" + text[:30000]
        )
        out = chat('Document summarizer', prompt, max_tokens=800)
        log_agent_event('summarizer', {'doc_id': doc_id}, {'summary_len': len(out)})
        return out
