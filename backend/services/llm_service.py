import openai
from backend.config import AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_DEPLOYMENT_NAME
from backend.utils.logger import get_logger
logger = get_logger(__name__)

if AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT:
    openai.api_type = 'azure'
    openai.api_key = AZURE_OPENAI_API_KEY
    openai.api_base = AZURE_OPENAI_ENDPOINT
    openai.api_version = AZURE_OPENAI_API_VERSION


def chat(system: str, prompt: str, max_tokens=512, temperature=0.0):
    model = AZURE_OPENAI_DEPLOYMENT_NAME
    if not model:
        raise RuntimeError('AZURE_OPENAI_DEPLOYMENT_NAME not configured')
    messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
    resp = openai.ChatCompletion.create(model=model, messages=messages, max_tokens=max_tokens, temperature=temperature)
    return resp['choices'][0]['message']['content'].strip()

def embed_text(text: str):
    model = AZURE_OPENAI_DEPLOYMENT_NAME
    if not model:
        raise RuntimeError('AZURE_OPENAI_DEPLOYMENT_NAME not configured')
    resp = openai.Embedding.create(engine=model, input=text)
    return resp['data'][0]['embedding']
