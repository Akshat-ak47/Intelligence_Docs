from backend.agents.base_agent import BaseAgent
from backend.utils.exceptions import ParsingError
from pathlib import Path
from pypdf import PdfReader
import docx

class ParserAgent(BaseAgent):
    def run(self, file_path: str) -> str:
        p = Path(file_path)
        if not p.exists():
            raise ParsingError('file not found: %s' % file_path)
        suffix = p.suffix.lower()
        if suffix == '.pdf':
            reader = PdfReader(str(p))
            texts = [page.extract_text() or '' for page in reader.pages]
            return '\n\n'.join([t for t in texts if t.strip()])
        elif suffix in ('.docx', '.doc'):
            d = docx.Document(str(p))
            paras = [para.text for para in d.paragraphs if para.text.strip()]
            return '\n\n'.join(paras)
        else:
            try:
                return p.read_text(encoding='utf-8')
            except Exception:
                raise ParsingError('unsupported file type')
