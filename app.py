import streamlit as st
from ingest import from_audio, from_text, from_url, from_whatsapp
from extractor import extract
from graph_store import load, save, add
from query_engine import answer
import tempfile, os

st.set_page_config(page_title="MemoryOS", layout="wide")
st.title("🧠 MemoryOS — Your Personal Knowledge Graph")

G = load()

# Sidebar — ingest
with st.sidebar:
    st.header("Feed Your Brain")
    mode = st.selectbox("Input type", ["Text/Notes","Audio (.mp3)","URL","WhatsApp export"])
    label = st.text_input("Label (e.g. 'gym_june14', 'huberman_podcast')")

    if mode == "Text/Notes":
        raw = st.text_area("Paste your notes here")
        if st.button("Add to graph") and raw and label:
            G = add(G, extract(raw, label)); save(G)
            st.success(f"Added! Graph now has {G.number_of_nodes()} nodes.")

    elif mode == "Audio (.mp3)":
        f = st.file_uploader("Upload voice memo", type=["mp3","wav","m4a"])
        if st.button("Transcribe & Add") and f and label:
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                tmp.write(f.read()); tmp_path = tmp.name
            text = from_audio(tmp_path)
            G = add(G, extract(text, label)); save(G)
            st.success("Transcribed and added!")
            st.caption(f"Transcript: {text[:200]}...")

    elif mode == "URL":
        url = st.text_input("Paste article URL")
        if st.button("Fetch & Add") and url and label:
            text = from_url(url)
            G = add(G, extract(text, label)); save(G)
            st.success("Fetched and added!")

    elif mode == "WhatsApp export":
        f = st.file_uploader("Upload _chat.txt", type=["txt"])
        if st.button("Import") and f and label:
            with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
                tmp.write(f.read()); tmp_path = tmp.name
            text = from_whatsapp(tmp_path)
            G = add(G, extract(text, label)); save(G)
            st.success("WhatsApp chat added!")

# Main — query + graph view
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("Ask Your Brain")
    query = st.text_input("Query (Hindi/English/Hinglish ok)",
                          placeholder="Progressive overload ke baare mein kya pata hai?")
    if st.button("Ask ↗") and query:
        with st.spinner("Searching your graph..."):
            st.markdown(answer(G, query))

    st.metric("Total concepts stored", G.number_of_nodes())
    st.metric("Total connections", G.number_of_edges())

with col2:
    st.subheader("Knowledge Graph")
    if G.number_of_nodes() > 0:
        # show top 50 nodes by count
        top = sorted(G.nodes(data=True),
                     key=lambda x: x[1].get("count",1), reverse=True)[:50]
        sub = G.subgraph([n for n,_ in top])

        import plotly.graph_objects as go
        pos = __import__("networkx").spring_layout(sub, seed=42)

        edge_x, edge_y = [], []
        for u,v in sub.edges():
            x0,y0 = pos[u]; x1,y1 = pos[v]
            edge_x += [x0,x1,None]; edge_y += [y0,y1,None]

        node_x = [pos[n][0] for n in sub.nodes()]
        node_y = [pos[n][1] for n in sub.nodes()]
        node_text = [sub.nodes[n].get("label",n) for n in sub.nodes()]
        node_size = [8 + sub.nodes[n].get("count",1)*3 for n in sub.nodes()]

        fig = go.Figure(
            data=[
                go.Scatter(x=edge_x, y=edge_y, mode="lines",
                           line=dict(width=0.5, color="#aaa"), hoverinfo="none"),
                go.Scatter(x=node_x, y=node_y, mode="markers+text",
                           text=node_text, textposition="top center",
                           marker=dict(size=node_size, color="#7F77DD"),
                           hoverinfo="text")
            ],
            layout=go.Layout(showlegend=False, margin=dict(l=0,r=0,t=0,b=0),
                             height=400, paper_bgcolor="rgba(0,0,0,0)",
                             plot_bgcolor="rgba(0,0,0,0)")
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add notes to see your graph grow here.")