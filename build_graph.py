"""Build the knowledge graph from data/graph.json, checked against the ontology."""

import json
from pathlib import Path

import networkx as nx

from ontology import ENTITY_TYPES, RELATIONSHIP_TYPES

GRAPH_FILE = Path(__file__).parent / "data" / "graph.json"


def load_graph_data(path=GRAPH_FILE):
    """Read the graph facts from the JSON file."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_graph(data):
    """Create a directed graph, rejecting anything the ontology doesn't allow."""
    graph = nx.DiGraph()

    # 1. Add nodes, checking each type is a known "box"
    for node in data["nodes"]:
        if node["type"] not in ENTITY_TYPES:
            raise ValueError(f"Unknown type '{node['type']}' on node '{node['id']}'")
        graph.add_node(node["id"], label=node["label"], type=node["type"])

    # 2. Add edges, checking each arrow is allowed by the ontology
    allowed = set(RELATIONSHIP_TYPES)
    for edge in data["edges"]:
        source, relation, target = edge["source"], edge["relation"], edge["target"]

        if source not in graph or target not in graph:
            raise ValueError(f"Edge uses an unknown node: {source} -> {target}")

        rule = (graph.nodes[source]["type"], relation, graph.nodes[target]["type"])
        if rule not in allowed:
            raise ValueError(f"Ontology does not allow {rule} ({source} -> {target})")

        graph.add_edge(source, target, relation=relation)

    return graph


def describe_connections(graph, start):
    """Print every arrow reachable by following edges from the start node."""
    print(f"Starting from: {graph.nodes[start]['label']}")
    for source, target in nx.dfs_edges(graph, start):
        relation = graph.edges[source, target]["relation"]
        print(f"  {graph.nodes[source]['label']} --{relation}--> {graph.nodes[target]['label']}")


if __name__ == "__main__":
    graph = build_graph(load_graph_data())
    print(f"Graph built: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges\n")
    describe_connections(graph, "onboarding")