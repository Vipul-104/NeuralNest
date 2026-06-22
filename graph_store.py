import networkx as nx
import pickle, os

GRAPH_PATH = "data/graph.pkl"

def load() -> nx.Graph:
    if os.path.exists(GRAPH_PATH) and os.path.getsize(GRAPH_PATH) > 0:
        return pickle.load(open(GRAPH_PATH, "rb"))
    return nx.Graph()

def save(G: nx.Graph):
    os.makedirs(os.path.dirname(GRAPH_PATH), exist_ok=True)
    pickle.dump(G, open(GRAPH_PATH, "wb"))

def add(G: nx.Graph, extracted: dict) -> nx.Graph:
    for n in extracted["nodes"]:
        if G.has_node(n["id"]):
            G.nodes[n["id"]]["sources"].append(n["source"])
            G.nodes[n["id"]]["count"] = G.nodes[n["id"]].get("count", 1) + 1
        else:
            G.add_node(n["id"], label=n["label"], type=n["type"],
                       sources=[n["source"]], embedding=n["embedding"], count=1)

    for e in extracted["edges"]:
        if G.has_node(e["src"]) and G.has_node(e["dst"]):
            G.add_edge(e["src"], e["dst"], rel=e["rel"])

    return G