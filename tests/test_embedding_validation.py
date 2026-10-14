
import pytest

from app.embedding.models import validate_embeddings


def test_accepts_valid_embeddings():
    embeddings = [[0.1, 0.2], [0.3, 0.4]]

    result = validate_embeddings(embeddings, expected_count=2)

    assert result == embeddings


def test_rejects_wrong_embedding_count():
    with pytest.raises(ValueError, match="Expected 2 embeddings, got 1"):
        validate_embeddings([[0.1, 0.2]], expected_count=2)


def test_rejects_inconsistent_dimensions():
    with pytest.raises(ValueError, match="has 1 dimensions"):
        validate_embeddings(
            [[0.1, 0.2], [0.3]],
            expected_count=2,
        )


def test_rejects_empty_vector():
    with pytest.raises(ValueError, match="must not be empty"):
        validate_embeddings([[]], expected_count=1)


@pytest.mark.parametrize("invalid_value", [float("nan"), float("inf"), float("-inf")])
def test_rejects_non_finite_values(invalid_value):
    with pytest.raises(ValueError, match="non-finite"):
        validate_embeddings([[invalid_value]], expected_count=1)


def test_rejects_non_numeric_values():
    with pytest.raises(ValueError, match="non-numeric"):
        validate_embeddings([[0.1, "invalid"]], expected_count=1)


def test_accepts_empty_batch():
    assert validate_embeddings([], expected_count=0) == []