import os
import numpy as np
import networkx as nx
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search(G: nx.Graph, query: str, top_k=10) -> list:
    q_emb = embedder.encode(query)
    scores = []
    for node, data in G.nodes(data=True):
        if "embedding" in data:
            score = cosine(q_emb, data["embedding"])
            scores.append((node, score, data))
    return sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]

def answer(G: nx.Graph, query: str) -> str:
    hits = search(G, query)
    if not hits:
        return "Nothing found in your graph yet. Add more notes!"

    context_parts = []
    for node, score, data in hits:
        neighbours = list(G.neighbors(node))
        context_parts.append(
            f"Concept: {data['label']} | Sources: {data.get('sources',[])} | "
            f"Connected to: {neighbours[:5]} | Seen {data.get('count',1)} times"
        )
    context = "\n".join(context_parts)

    prompt = f"""You are MemoryOS — a personal knowledge assistant.
Answer ONLY from the user's personal knowledge graph below.
Never use outside knowledge. Mention which source the insight came from.

GRAPH CONTEXT:
{context}

USER QUESTION: {query}

Answer in the same language as the question (Hindi/English/Hinglish ok)."""

    resp = model.generate_content(prompt)
    return resp.text