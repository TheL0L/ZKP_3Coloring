import hashlib
import random
import secrets
import networkx as nx
from typing import Dict, Tuple

class Prover:
    def __init__(self, graph: nx.Graph, coloring: Dict[int, int]) -> None:
        """
        Initializes the Prover with a graph and a matching 3-coloring.
        :param graph: NetworkX Graph
        :param coloring: Dictionary mapping nodes to colors {0,1,2}
        """
        self.graph = graph
        self.original_coloring = coloring
        self.shuffled_coloring = {}  
        self.commitments = {}
        self.random_salts = {}

    def commit(self) -> Tuple[str, str]:
        """Generates cryptographic commitments for the colors with random salts."""
        self.commitments = {}
        self.random_salts = {}

        # shuffle colors consistently
        color_permutation = list(range(3))
        random.shuffle(color_permutation)
        self.shuffled_coloring = {node: color_permutation[self.original_coloring[node]] for node in self.graph.nodes}

        # create commitments
        for node, color in self.shuffled_coloring.items():
            salt = secrets.token_hex(16)  
            self.random_salts[node] = salt
            commitment = hashlib.sha256(f"{color}{salt}".encode()).hexdigest()
            self.commitments[node] = commitment
        
        return self.commitments

    def reveal(self, edge: Tuple[int, int]) -> Tuple[int, str, int, str]:
        """Reveals the shuffled colors and salts for a given edge."""
        node1, node2 = edge
        return (
            self.shuffled_coloring[node1], self.random_salts[node1],
            self.shuffled_coloring[node2], self.random_salts[node2]
        )

class Verifier:
    def __init__(self, graph: nx.Graph, verification_cycles: int = 1) -> None:
        """
        Initializes the Verifier with a graph and a number of verification cycles.
        :param graph: NetworkX Graph
        :param verification_cycles: Number of verification rounds
        """
        self.graph = graph
        self.verification_cycles = max(1, verification_cycles)

    def choose_edge(self) -> Tuple[int, int]:
        """Randomly selects an edge to challenge."""
        return random.choice(list(self.graph.edges()))

    def verify(self, edge: Tuple[int, int], commitments: Tuple[str, str], revealed_values: Tuple[int, str, int, str]) -> bool:
        """Verifies that the revealed colors match the commitments and are different."""
        node1, node2 = edge
        color1, salt1, color2, salt2 = revealed_values

        # recompute commitments
        computed_commitment1 = hashlib.sha256(f"{color1}{salt1}".encode()).hexdigest()
        computed_commitment2 = hashlib.sha256(f"{color2}{salt2}".encode()).hexdigest()

        # verify commitments and ensure colors are different
        return (
            computed_commitment1 == commitments[node1] and
            computed_commitment2 == commitments[node2] and
            color1 != color2
        )
