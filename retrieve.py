"""Search our UX knowledge base by meaning."""

import sys

from ingest import embed_texts, get_collection


def search(question, top_k=3):
    """Return the top_k documents closest in meaning to the question."""
    collection = get_collection()
    results = collection.query(
        query_embeddings=embed_texts([question]),
        n_results=top_k,
    )

    matches = []
    for doc_id, text, meta, distance in zip(
        results["ids"][0],
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        matches.append({
            "id": doc_id,
            "title": meta["title"],
            "similarity": round(1 - distance, 3),
            "text": text,
        })
    return matches


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "Can new hires finish setting up their payroll account without help?"
    print(f"Question: {question}\n")
    for rank, match in enumerate(search(question), start=1):
        print(f"{rank}. {match['title']} ({match['id']})  similarity={match['similarity']}")