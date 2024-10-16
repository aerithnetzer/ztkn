import os
import re
import networkx as nx
from pyvis.network import Network
import webbrowser
from flask import Flask, send_file, request
import threading
import requests

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
    file_paths = {}

    for file_path in md_files:
        with open(file_path, "r") as f:
            for line in f:
                if line.startswith("# "):
                    title = line[2:].strip()
                    if title not in added_nodes:
                        graph.add_node(title)
                        added_nodes.add(title)
                        file_paths[title] = file_path
                    break

        with open(file_path, "r") as f:
            content = f.read()
            links = extract_wikilinks(content)

            for link in links:
                if link not in added_nodes:
                    graph.add_node(link)
                    added_nodes.add(link)
                    file_paths[link] = file_path
                graph.add_edge(title, link)

                # Add context as a tooltip
                context = extract_context(content, link)
                graph.nodes[link]["title"] = context

    return graph, file_paths


def inject_double_click_script(html_file):
    script = """
    <script type="text/javascript">
        network.on("doubleClick", function (params) {
            if (params.nodes.length > 0) {
                var nodeId = params.nodes[0];
                var node = nodes.get(nodeId);
                var filePath = node.file_path;
                fetch("/open_file", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ file_path: filePath })
                });
            }
        });
    </script>
    """

    with open(html_file, "r") as file:
        content = file.read()

    # Insert the script before the closing </body> tag
    content = content.replace("</body>", script + "</body>")

    with open(html_file, "w") as file:
        file.write(content)


def visualize_graph(graph, file_paths):
    net = Network(notebook=False)
    net.from_nx(graph)
    for node in net.nodes:
        node_id = node["id"]
        node["title"] = graph.nodes[node_id].get("title", "")
        node["file_path"] = file_paths.get(node_id, "")
    net.show("graph.html")

    # Inject JavaScript for handling double-click events
    inject_double_click_script("graph.html")


@app.route("/open_file", methods=["POST"])
def open_file():
    data = request.json
    file_path = data.get("file_path")
    if file_path:
        os.system(f"nvim {file_path}")
    return "", 204


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

    graph, file_paths = build_graph(md_files)
    if graph is None:
        print("Graph creation failed.")
        return
    print("Graph created successfully.")

    visualize_graph(graph, file_paths)
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
