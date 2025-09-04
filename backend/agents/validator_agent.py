from backend.agents.base_agent import BaseAgent
from backend.utils.langsmith_stub import log_agent_event

class ValidatorAgent(BaseAgent):
    def run(self, doc_id: str, summary: str, entities: list):
        reasons = []
        valid = True
        if not summary or len(summary) < 80:
            valid = False
            reasons.append('Summary too short')
        if not entities or len(entities) == 0:
            reasons.append('No entities found')
        res = {'doc_id': doc_id, 'valid': valid, 'reasons': reasons}
        log_agent_event('validator', {'doc_id': doc_id}, res)
        return res
