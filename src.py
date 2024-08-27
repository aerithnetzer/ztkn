import os
import re
import networkx as nx
from pyvis.network import Network
import webbrowser
from flask import Flask, send_file
import threading

app = Flask(__name__)


def get_markdown_files(directory):
    md_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    return md_files


def extract_wikilinks(md_content):
    return re.findall(r"\[\[(.*?)\]\]", md_content)


def extract_context(md_content, link):
    idx = md_content.find(link)
    if idx == -1:
        return ""
    start = max(idx - 10, 0)
    end = min(idx + len(link) + 10, len(md_content))
    return md_content[start:end]


def build_graph(md_files):
    graph = nx.Graph()
    added_nodes = set()

    for file_path in md_files:
        title = os.path.basename(file_path)
        if title not in added_nodes:
            graph.add_node(title)
            added_nodes.add(title)

        with open(file_path, "r") as f:
            content = f.read()
            links = extract_wikilinks(content)

            for link in links:
                if link not in added_nodes:
                    graph.add_node(link)
                    added_nodes.add(link)
                graph.add_edge(title, link)

                # Add context as a tooltip
                context = extract_context(content, link)
                graph.nodes[link]["title"] = context

    return graph


def visualize_graph(graph):
    net = Network(notebook=False)
    net.from_nx(graph)
    for node in net.nodes:
        node["title"] = graph.nodes[node["id"]].get("title", "")
    net.show("graph.html")


@app.route("/")
def serve_graph():
    return send_file("graph.html")


def open_browser():
    webbrowser.open("http://127.0.0.1:5000/")


def main(directory):
    md_files = get_markdown_files(directory)
    if not md_files:
        print("No markdown files found.")
        return
    print(f"Markdown files: {md_files}")

    graph = build_graph(md_files)
    if graph is None:
        print("Graph creation failed.")
        return
    print("Graph created successfully.")

    visualize_graph(graph)
    print("Graph visualization created.")

    # Start Flask app in a separate thread
    threading.Timer(1, open_browser).start()
    app.run()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python app.py <directory>")
    else:
        main(sys.argv[1])
