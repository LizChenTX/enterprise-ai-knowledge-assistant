
import math
from numbers import Real


def validate_embeddings(
    embeddings: list[list[float]],
    expected_count: int,
) -> list[list[float]]:
    """Validate embedding vectors before they enter the vector store."""
    if expected_count < 0:
        raise ValueError("expected_count must be non-negative")

    if len(embeddings) != expected_count:
        raise ValueError(
            f"Expected {expected_count} embeddings, got {len(embeddings)}"
        )

    if not embeddings:
        return embeddings

    expected_dimensions = len(embeddings[0])

    if expected_dimensions == 0:
        raise ValueError("embedding vectors must not be empty")

    for index, vector in enumerate(embeddings):
        if len(vector) != expected_dimensions:
            raise ValueError(
                f"Embedding at index {index} has {len(vector)} dimensions; "
                f"expected {expected_dimensions}"
            )

        for value in vector:
            if isinstance(value, bool) or not isinstance(value, Real):
                raise ValueError(
                    f"Embedding at index {index} contains a non-numeric value"
                )

            if not math.isfinite(value):
                raise ValueError(
                    f"Embedding at index {index} contains a non-finite value"
                )

    return embeddings