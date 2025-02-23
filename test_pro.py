import numpy as np
import networkx as nx
import random
import math
from typing import Dict, Tuple
from Parties import Prover, Verifier
from Protocol import execute_zkp_protocol as protocol
from main import generate_3_colorable_graph


def make_invalid_coloring(graph: nx.Graph , valid_coloring: Dict[int,int])->Dict[int,int]:
        """ 
        Creates an invalid coloring by forcing a random edge to share the same color
        """
        invalid_coloring= valid_coloring.copy()
        edges=list(graph.edges())

        # Ensure there are edges to modify
        if not edges:
            return invalid_coloring 
        
        e=random.choice(edges)
        u , v =e

        # Force the nodes to share the same color , it makes the graph invalid
        invalid_coloring[v] = invalid_coloring[u]

        return invalid_coloring

# Testing with Valid coloring graph

def test_protocol(trials: int=50, graph_size: int = 20, target: float = 0.9999):
    """
    Tests the ZKP protocol with valid and invalid graph colorings.
    """
    print(f"Running {trials} trials for a 3cg with {graph_size} nodes")

    valid_passes=0
    for _ in range (trials):
        # Generate a 3-colorable graph with valid coloring
        valid_graph,valid_coloring= generate_3_colorable_graph(graph_size)
        edge_count=len(valid_graph)

        # Calculate required verification rounds
        verification_rounds = int(-edge_count * np.log(1 - target))

        # Create prover and verifier 
        prover= Prover(valid_graph,valid_coloring)
        verifier= Verifier(valid_graph,verification_rounds)

        if protocol(prover,verifier):
            valid_passes+=1

    success_rate= valid_passes/trials
    print(f"\n[VALID COLORING]")
    print(f"Protocol accepted {valid_passes} out of {trials} trials")
    print(f"Acceptance rate: {success_rate * 100:.2f}%\n")

# Testing with Invalid coloring graph
    invalid_passes=0
    for _ in range (trials):
        # Generate a 3-colorable graph and make it invalid
        g_invalid,valid_coloring= generate_3_colorable_graph(graph_size)

        invalid_coloring= make_invalid_coloring(g_invalid,valid_coloring)

        edge_count=len(valid_graph)
        verification_rounds = int(-edge_count * np.log(1 - target))

        # Create prover and verifier 
        prover= Prover(g_invalid,invalid_coloring)
        verifier= Verifier(g_invalid,verification_rounds)

        if protocol(prover,verifier):
            invalid_passes+=1

    success_rate= invalid_passes/trials
    print(f"\n[INVALID COLORING]")
    print(f"Protocol accepted {invalid_passes} out of {trials} trials")
    print(f"Acceptance rate: {success_rate * 100:.2f}%\n")

   
if __name__ == '__main__':
    test_protocol(trials=100, graph_size=60, target=0.9  )