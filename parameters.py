from dataclasses import dataclass


@dataclass
class Parameters:
    # Preprocessing parameeters
    seq_len: int = 32
    num_words: int = 2000

    # Model parameters
    embedding_size: int = 64
    out_size: int = 32
    stride: int = 2

    # Training parameters
    epochs: int = 100
    batch_size: int = 12
    learning_rate: float = 0.001
