import spacy
from sentence_transformers import SentenceTransformer

nlp = spacy.load("en_core_web_sm")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def extract(text: str, source_label: str) -> dict:
    doc = nlp(text)
    nodes, edges = [], []

    # entities as nodes
    for ent in doc.ents:
        nodes.append({
            "id": ent.text.lower(),
            "label": ent.text,
            "type": ent.label_,
            "source": source_label,
            "embedding": embedder.encode(ent.text).tolist()
        })

    # noun chunks as concept nodes
    for chunk in doc.noun_chunks:
        nodes.append({
            "id": chunk.root.lemma_.lower(),
            "label": chunk.text,
            "type": "concept",
            "source": source_label,
            "embedding": embedder.encode(chunk.text).tolist()
        })

    # subject-verb-object as edges
    for token in doc:
        if token.dep_ == "ROOT":
            subj = [w for w in token.lefts if w.dep_ in ("nsubj","nsubjpass")]
            obj  = [w for w in token.rights if w.dep_ in ("dobj","attr","prep")]
            if subj and obj:
                edges.append({
                    "src": subj[0].lemma_.lower(),
                    "dst": obj[0].lemma_.lower(),
                    "rel": token.lemma_
                })

    return {"nodes": nodes, "edges": edges}