from Parties import Prover, Verifier
from tqdm import tqdm

def execute_zkp_protocol(prover: Prover, verifier: Verifier) -> bool:
    """Executes the 3-color Zero-Knowledge Proof protocol."""
    for i in tqdm(range(verifier.verification_cycles), desc='Verification Progress', unit='Round'):
        commitments = prover.commit()

        chosen_edge = verifier.choose_edge()
        
        revealed_values = prover.reveal(chosen_edge)

        if not verifier.verify(chosen_edge, commitments, revealed_values):
            return False

    return True

