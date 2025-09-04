from backend.utils.logger import get_logger
logger = get_logger(__name__)

try:
    import autogen_agentchat as autogen
    AUTOGEN_AVAILABLE = True
except Exception:
    AUTOGEN_AVAILABLE = False

from backend.agents.parser_agent import ParserAgent
from backend.agents.summarizer_agent import SummarizerAgent
from backend.agents.entity_agent import EntityAgent
from backend.agents.qa_agent import QnAAgent
from backend.agents.validator_agent import ValidatorAgent
from backend.services.embeddings_service import embeddings_service

class Orchestrator:
    def __init__(self):
        self.parser = ParserAgent()
        self.summarizer = SummarizerAgent()
        self.entity = EntityAgent()
        self.qa = QnAAgent()
        self.validator = ValidatorAgent()

    def run_pipeline(self, file_path: str):
        logger.info('Starting pipeline for %s', file_path)
        text = self.parser.run(file_path)
        doc_id = file_path.split('/')[-1]
        summary = self.summarizer.run(doc_id, text)
        entities = self.entity.run(doc_id, text)
        try:
            embeddings_service.add_documents([{'doc_id': doc_id, 'text': text}])
        except Exception as e:
            logger.warning('embeddings add failed: %s', e)
        validation = self.validator.run(doc_id, summary, entities)
        return {'doc_id': doc_id, 'text': text, 'summary': summary, 'entities': entities, 'validation': validation}

    def run_qa(self, doc_id: str, query: str):
        return self.qa.run(doc_id, query)

orchestrator = Orchestrator()
