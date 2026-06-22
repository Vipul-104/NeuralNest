from ingest import from_text
from extractor import extract
from graph_store import load, save, add

text = "Progressive overload means increasing weight by 5% weekly for strength gains."
G = load()
G = add(G, extract(text, "gym_note_1"))
save(G)
print(f"Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")