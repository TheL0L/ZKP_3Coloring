import numpy as np
import networkx as nx
import random
import math
from typing import Dict, Tuple
from Parties import Prover, Verifier
from Protocol import execute_zkp_protocol as protocol
from main import generate_3_colorable_graph


def make_invalid_coloring(graph: nx.Graph , valid_coloring: Dict[int,int])->Dict[int,int]:
        invalid_coloring= valid_coloring.copy()
        edges=list(graph.edges())

        #checking if there edges at all
        if not edges:
            return invalid_coloring 
        
        e=random.choice(edges)
        u , v =e

        #force the nodes to share the same color , it makes the graph invalid
        invalid_coloring[v] = invalid_coloring[u]
        return invalid_coloring


#Testing with Valid coloring graph

def test_pro(trials: int=50, graph_size: int = 20, target: float = 0.9999):
    print(f"Running {trials} trials for a 3cg with {graph_size} nodes")

    valid_passes=0
    for _ in range (trials):
        #here i generate 3cg with valid coloring
        g_valid,valid_coloring= generate_3_colorable_graph(graph_size)
        edges_num=len(g_valid)

        #i calculate how many rounds we need for the specific size
        verification_rounds = int(-edges_num * np.log(1 - target))

        #create prover and verifier 
        prover= Prover(g_valid,valid_coloring)
        verifier= Verifier(g_valid,verification_rounds)

        if protocol(prover,verifier):
            valid_passes+=1

    success_rate= valid_passes/trials
    print(f"\n[VALID COLORING]")
    print(f"Protocol accepted {valid_passes} out of {trials} trials")
    print(f"Acceptance rate: {success_rate * 100:.2f}%\n")

#Testing with Invalid coloring graph
    invalid_passes=0
    for _ in range (trials):
        #here i generate the same 3cg but swapped the coloring
        g_invalid,valid_coloring= generate_3_colorable_graph(graph_size)

        invalid_coloring= make_invalid_coloring(g_invalid,valid_coloring)

        edges_num=len(g_valid)
        #i calculate how many rounds we need for the specific size
        verification_rounds = int(-edges_num * np.log(1 - target))

        #create prover and verifier 
        prover= Prover(g_invalid,invalid_coloring)
        verifier= Verifier(g_invalid,verification_rounds)

        if protocol(prover,verifier):
            valid_passes+=1

    success_rate= invalid_passes/trials
    print(f"\n[INVALID COLORING]")
    print(f"Protocol accepted {invalid_passes} out of {trials} trials")
    print(f"Acceptance rate: {success_rate * 100:.2f}%\n")

   
if __name__ == '__main__':
    test_pro(
        trials=50, 
        graph_size=30, 
        target=0.9999  
    )