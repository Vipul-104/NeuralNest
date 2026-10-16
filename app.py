import streamlit as st
from ingest import from_audio, from_text, from_url, from_whatsapp
from extractor import extract
from graph_store import load, save, add
from query_engine import answer
from cross_domain import find_cross_domain_insights, get_knowledge_stats
import tempfile, os

st.set_page_config(page_title="NeuralNest", layout="wide")
st.title("🧠 NeuralNest — Your Personal Knowledge Graph")

G = load()

# ── Sidebar: ingest ──────────────────────────────────────────
with st.sidebar:
    st.header("📥 Feed Your Brain")
    mode = st.selectbox("Input type",
                        ["Text / Notes", "Audio (.mp3/.wav)", "Article URL", "WhatsApp Export"])
    label = st.text_input("Label (e.g. gym_june14, huberman_ep42, ml_study)",
                          placeholder="domain_description")
    st.caption("Label prefix = domain. Use: gym_, podcast_, study_, work_")

    if mode == "Text / Notes":
        raw = st.text_area("Paste your notes here", height=150)
        if st.button("➕ Add to Graph") and raw and label:
            with st.spinner("Extracting concepts..."):
                G = add(G, extract(raw, label))
                save(G)
            st.success(f"✅ Added! Graph: {G.number_of_nodes()} concepts, {G.number_of_edges()} connections")

    elif mode == "Audio (.mp3/.wav)":
        f = st.file_uploader("Upload voice memo", type=["mp3", "wav", "m4a"])
        if st.button("🎙️ Transcribe & Add") and f and label:
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                tmp.write(f.read())
                tmp_path = tmp.name
            with st.spinner("Transcribing audio..."):
                from ingest import from_audio
                text = from_audio(tmp_path)
                G = add(G, extract(text, label))
                save(G)
            st.success("✅ Transcribed and added!")
            st.caption(f"Transcript preview: {text[:200]}...")

    elif mode == "Article URL":
        url = st.text_input("Paste article URL")
        if st.button("🌐 Fetch & Add") and url and label:
            with st.spinner("Fetching article..."):
                text = from_url(url)
                G = add(G, extract(text, label))
                save(G)
            st.success(f"✅ Article added! {len(text.split())} words processed.")

    elif mode == "WhatsApp Export":
        st.caption("Export: WhatsApp chat → ⋮ → More → Export chat → Without media")
        f = st.file_uploader("Upload _chat.txt", type=["txt"])
        if st.button("💬 Import Chat") and f and label:
            with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
                tmp.write(f.read())
                tmp_path = tmp.name
            with st.spinner("Parsing WhatsApp messages..."):
                text = from_whatsapp(tmp_path)
                msg_count = len(text.split("\n"))
                G = add(G, extract(text, label))
                save(G)
            st.success(f"✅ {msg_count} messages processed!")

    # stats
    st.divider()
    stats = get_knowledge_stats(G)
    st.metric("Concepts stored", stats["total_concepts"])
    st.metric("Connections", stats["total_connections"])
    if stats["domains_covered"]:
        st.caption(f"Domains: {', '.join(stats['domains_covered'])}")

# ── Main: tabs ──────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["💬 Ask Your Brain", "🕸️ Knowledge Graph", "✨ Cross-Domain Insights"])

with tab1:
    st.subheader("Ask anything — Hindi / English / Hinglish")
    query = st.text_input("Your question",
                          placeholder="Progressive overload ke baare mein kya pata hai?")
    if st.button("Ask ↗", type="primary") and query:
        with st.spinner("Searching your knowledge graph..."):
            result = answer(G, query)
        st.markdown(result)

with tab2:
    if G.number_of_nodes() == 0:
        st.info("Add some notes to see your knowledge graph grow here.")
    else:
        import plotly.graph_objects as go
        import networkx as nx_lib

        top = sorted(G.nodes(data=True),
                     key=lambda x: x[1].get("count", 1), reverse=True)[:60]
        sub = G.subgraph([n for n, _ in top])
        pos = nx_lib.spring_layout(sub, seed=42, k=0.8)

        edge_x, edge_y = [], []
        for u, v in sub.edges():
            x0, y0 = pos[u]; x1, y1 = pos[v]
            edge_x += [x0, x1, None]; edge_y += [y0, y1, None]

        node_x = [pos[n][0] for n in sub.nodes()]
        node_y = [pos[n][1] for n in sub.nodes()]
        node_text = [sub.nodes[n].get("label", n) for n in sub.nodes()]
        node_size = [10 + sub.nodes[n].get("count", 1) * 4 for n in sub.nodes()]
        node_hover = [
            f"{sub.nodes[n].get('label', n)}<br>Sources: {sub.nodes[n].get('sources', [])}<br>Seen: {sub.nodes[n].get('count', 1)}x"
            for n in sub.nodes()
        ]

        fig = go.Figure(data=[
            go.Scatter(x=edge_x, y=edge_y, mode="lines",
                       line=dict(width=0.5, color="#555"), hoverinfo="none"),
            go.Scatter(x=node_x, y=node_y, mode="markers+text",
                       text=node_text, textposition="top center",
                       hovertext=node_hover, hoverinfo="text",
                       marker=dict(size=node_size, color="#7F77DD",
                                   line=dict(width=1, color="#fff")))
        ], layout=go.Layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            height=500,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        ))
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"Showing top {len(list(sub.nodes()))} concepts. Node size = how often concept appeared.")

with tab3:
    if G.number_of_nodes() == 0:
        st.info("Add notes from multiple domains (gym_, podcast_, study_) to discover cross-domain insights.")
    else:
        insights = find_cross_domain_insights(G, min_domains=2)
        if not insights:
            st.info("Add inputs with different label prefixes (e.g. gym_x, podcast_y, study_z) to find connections.")
        else:
            st.subheader(f"🔗 {len(insights)} cross-domain connections found")
            st.caption("These concepts appear across multiple areas of your life — connections your brain didn't notice.")
            for i in insights[:15]:
                with st.expander(f"**{i['concept']}** — spans {len(i['domains'])} domains"):
                    st.write(f"**Domains:** {' · '.join(i['domains'])}")
                    st.write(f"**Appeared:** {i['seen_count']} times across {len(i['sources'])} sources")
                    st.write(f"**Sources:** {', '.join(set(i['sources']))}")