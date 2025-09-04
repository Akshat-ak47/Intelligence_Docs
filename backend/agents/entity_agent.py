from backend.agents.base_agent import BaseAgent
import spacy
from backend.utils.langsmith_stub import log_agent_event
from backend.utils.exceptions import EntityExtractionError

class EntityAgent(BaseAgent):
    def __init__(self):
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except Exception as e:
            raise EntityExtractionError('Install spaCy model: python -m spacy download en_core_web_sm') from e

    def run(self, doc_id: str, text: str):
        doc = self.nlp(text[:200000])
        ents = [{'text': ent.text, 'label': ent.label_, 'start': ent.start_char, 'end': ent.end_char} for ent in doc.ents]
        log_agent_event('entity_agent', {'doc_id': doc_id}, {'entities': len(ents)})
        return ents
