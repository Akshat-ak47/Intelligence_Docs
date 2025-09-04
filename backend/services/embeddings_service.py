"""Embeddings service using Postgres+pgvector when available, otherwise in-memory fallback.
"""
from backend.config import POSTGRES_URL
from backend.services.llm_service import embed_text
from backend.utils.logger import get_logger
logger = get_logger(__name__)

try:
    from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Text, select
    from sqlalchemy.exc import SQLAlchemyError
    from pgvector.sqlalchemy import Vector
    SQLALCHEMY_PG_AVAILABLE = True
except Exception as e:
    logger.warning('SQLAlchemy/pgvector not available: %s', e)
    SQLALCHEMY_PG_AVAILABLE = False

class EmbeddingsService:
    def __init__(self):
        self.memory = []
        self._engine = None
        self._metadata = None
        self._table = None
        if SQLALCHEMY_PG_AVAILABLE:
            try:
                self._engine = create_engine(POSTGRES_URL)
                self._metadata = MetaData()
                # if table exists we'll reflect later when needed
            except Exception as e:
                logger.warning('Failed to create SQLAlchemy engine: %s', e)
                self._engine = None

    def _create_table(self, dim: int):
        if not SQLALCHEMY_PG_AVAILABLE or not self._engine:
            return
        try:
            docs = Table(
                'documents', self._metadata,
                Column('id', Integer, primary_key=True, autoincrement=True),
                Column('doc_id', Text, nullable=False),
                Column('content', Text, nullable=False),
                Column('embedding', Vector(dim)),
            )
            docs.create(self._engine, checkfirst=True)
            self._table = docs
            logger.info('Created documents table with vector dim=%d', dim)
        except Exception as e:
            logger.exception('create_table failed: %s', e)

    def add_documents(self, docs: list[dict]):
        """docs: list of {'doc_id': str, 'text': str}
        """
        if not docs:
            return
        if SQLALCHEMY_PG_AVAILABLE and self._engine:
            try:
                first_emb = embed_text(docs[0]['text'])
                dim = len(first_emb)
                if self._table is None:
                    self._create_table(dim)
                with self._engine.begin() as conn:
                    for d in docs:
                        emb = embed_text(d['text'])
                        ins = self._table.insert().values(doc_id=d['doc_id'], content=d['text'], embedding=emb)
                        conn.execute(ins)
                logger.info('Inserted %d docs to Postgres+pgvector', len(docs))
                return
            except Exception as e:
                logger.warning('Postgres insert failed, falling back to memory: %s', e)
        # fallback: in-memory
        for d in docs:
            emb = embed_text(d['text'])
            self.memory.append({'doc_id': d['doc_id'], 'text': d['text'], 'embedding': emb})
        logger.warning('Stored documents in memory (fallback)')

    def search(self, query: str, k: int = 3):
        q_emb = embed_text(query)
        results = []
        if SQLALCHEMY_PG_AVAILABLE and self._engine and self._table is not None:
            try:
                with self._engine.connect() as conn:
                    sel = select(self._table.c.doc_id, self._table.c.content, self._table.c.embedding)
                    rows = conn.execute(sel).fetchall()
                    for r in rows:
                        emb = r['embedding']
                        try:
                            emb_list = list(emb)
                        except Exception:
                            emb_list = emb
                        from math import sqrt
                        def cosine(a,b):
                            dot = sum(x*y for x,y in zip(a,b))
                            na = sqrt(sum(x*x for x in a))
                            nb = sqrt(sum(x*x for x in b))
                            return dot / (na*nb + 1e-12)
                        score = cosine(q_emb, emb_list)
                        results.append((score, r['doc_id'], r['content']))
                    results.sort(key=lambda x: x[0], reverse=True)
                    return [{'doc_id': doc_id, 'content': content} for _, doc_id, content in results[:k]]
            except Exception as e:
                logger.warning('Postgres search failed, falling back to memory: %s', e)
        # memory fallback
        from math import sqrt
        def cosine(a,b):
            dot = sum(x*y for x,y in zip(a,b))
            na = sqrt(sum(x*x for x in a))
            nb = sqrt(sum(x*x for x in b))
            return dot / (na*nb + 1e-12)
        scored = []
        for item in self.memory:
            score = cosine(q_emb, item['embedding'])
            scored.append((score, item['doc_id'], item['text']))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [{'doc_id': doc_id, 'content': text} for _, doc_id, text in scored[:k]]

embeddings_service = EmbeddingsService()
