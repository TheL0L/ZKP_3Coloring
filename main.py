import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from Parties import Prover, Verifier
from Protocol import execute_zkp_protocol as protocol
from typing import Dict, Tuple


def generate_3_colorable_graph(N: int, E: int = None) -> Tuple[nx.Graph, Dict[int, int]]:
    """Generates a random 3-colorable graph with N nodes and returns the graph and its coloring."""
    if N < 3:
        raise ValueError("N must be at least 3 for a 3-colorable graph.")

    # Step 1: pick a random number of edges within the valid range
    min_edges = N - 1  # minimum edges for connectivity
    max_edges = (N * (N - 1)) // 2  # complete graph edges
    E = random.randint(min_edges, max_edges) if E is None else max(min_edges, min(int(E), max_edges))

    # Step 2: split nodes into 3 groups randomly
    nodes = np.arange(N)
    np.random.shuffle(nodes)
    groups = [set(), set(), set()]

    for i, node in enumerate(nodes):
        groups[i % 3].add(node)  # distribute nodes across 3 groups

    # assign colors based on grouping
    colors = {node: i for i, group in enumerate(groups) for node in group}

    # Step 3: generate edges between groups
    edges = set()
    possible_edges = []
    
    # only allow edges between different groups
    for i in range(3):
        for j in range(i + 1, 3):
            group1, group2 = list(groups[i]), list(groups[j])
            possible_edges.extend([(u, v) for u in group1 for v in group2])
    
    # randomly select E edges
    E = min(E, len(possible_edges))  # bound max possible edges
    selected_edges = np.random.choice(len(possible_edges), E, replace=False)
    
    for idx in selected_edges:
        edges.add(possible_edges[idx])
    
    # Step 4: create the graph using NetworkX
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # Step 5: return the graph and its 3-coloring
    return G, colors

def draw_colored_graph(graph: nx.Graph, coloring: Dict[int, int]) -> None:
    """Draws the graph with nodes colored according to the given coloring."""
    color_map = {0: 'red', 1: 'green', 2: 'blue'}
    node_colors = [color_map[coloring[node]] for node in graph.nodes]
    
    plt.figure(figsize=(6, 6))
    pos = nx.spring_layout(graph, seed=42)  
    nx.draw(graph, pos, with_labels=True, node_color=node_colors, edge_color="black", node_size=1000, font_size=15)
    
    plt.title("Graph with 3-Coloring")
    plt.show()

def compute_confidence(successful_rounds: int, total_edges: int) -> float:
    """Computes the confidence level of prover not cheating."""
    if successful_rounds == 0 or total_edges == 0:
        return 0  # no confidence if no successful checks
    return 1 - np.exp(-successful_rounds / total_edges)


if __name__ == '__main__':
    # rounds as a function of edges count and probability:
    #           R = -E * ln( 1 - P )
    
    P = 0.999_998
    G, valid_coloring = generate_3_colorable_graph(100, 4950)
    edges_count = len(G.edges())
    verification_rounds = int(-edges_count * np.log(1 - P))

    # draw_colored_graph(G, valid_coloring)

    prover = Prover(G, valid_coloring)
    verifier = Verifier(G, verification_rounds)

    if protocol(prover, verifier):
        print(f'Proof is accepted with {compute_confidence(verification_rounds, edges_count) * 100:.6f}% confidence.')
    else:
        print('Proof rejected, possible cheating or message corruption.')

