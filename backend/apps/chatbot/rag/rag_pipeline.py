from .retriever import retrieve_chunks
from .response_generator import generate_answer
from .prompt_template import build_prompt

def run_pipeline(query):
    chunks = retrieve_chunks(query)
    prompt = build_prompt(query, chunks)
    return generate_answer(prompt)
