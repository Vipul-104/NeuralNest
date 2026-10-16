import networkx as nx

def find_cross_domain_insights(G: nx.Graph, min_domains: int = 2) -> list:
    """
    Find concepts that appear across multiple input domains.
    e.g. 'discipline' appears in gym_notes AND podcast AND study_notes
    Returns list of (concept_label, domains, count) sorted by impact.
    """
    insights = []
    for node, data in G.nodes(data=True):
        sources = data.get("sources", [])
        # extract domain prefix from label e.g. 'gym_june14' -> 'gym'
        domains = set(s.split("_")[0] for s in sources if "_" in s)
        if not domains:
            domains = set(sources)  # fallback: use full source names
        if len(domains) >= min_domains:
            insights.append({
                "concept": data.get("label", node),
                "domains": list(domains),
                "seen_count": data.get("count", 1),
                "sources": sources
            })
    return sorted(insights, key=lambda x: (len(x["domains"]), x["seen_count"]), reverse=True)

def get_knowledge_stats(G: nx.Graph) -> dict:
    """
    Returns summary stats about the user's knowledge graph.
    """
    all_sources = []
    for _, data in G.nodes(data=True):
        all_sources.extend(data.get("sources", []))

    domains = set(s.split("_")[0] for s in all_sources if "_" in s)
    top_nodes = sorted(G.nodes(data=True),
                       key=lambda x: x[1].get("count", 1), reverse=True)[:5]

    return {
        "total_concepts": G.number_of_nodes(),
        "total_connections": G.number_of_edges(),
        "total_inputs": len(set(all_sources)),
        "domains_covered": list(domains),
        "top_concepts": [d.get("label", n) for n, d in top_nodes]
    }