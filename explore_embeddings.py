"""Experiment: do similar meanings really get similar embeddings?"""

import math

import ollama

MODEL = "nomic-embed-text"


def embed(text):
    """Ask Ollama for the embedding (list of numbers) of one piece of text."""
    response = ollama.embed(model=MODEL, input=text)
    return response["embeddings"][0]


def cosine_similarity(a, b):
    """How similar are two embeddings? Near 1 = similar meaning."""
    dot = sum(x * y for x, y in zip(a, b))
    length_a = math.sqrt(sum(x * x for x in a))
    length_b = math.sqrt(sum(y * y for y in b))
    return dot / (length_a * length_b)


if __name__ == "__main__":
    question = "Can new hires finish setting up their payroll account without help?"
    similar = "Check whether employees can complete the onboarding process."
    unrelated = "How satisfied are users with the colors of the mobile app?"

    q_vec = embed(question)
    print(f"Embedding length: {len(q_vec)} numbers")
    print(f"First five numbers: {[round(x, 3) for x in q_vec[:5]]}\n")

    print(f"Question vs similar:   {cosine_similarity(q_vec, embed(similar)):.3f}")
    print(f"Question vs unrelated: {cosine_similarity(q_vec, embed(unrelated)):.3f}")