from typing import Iterable, Sequence
import numpy as np


def apk(actual: int, predicted: Sequence[int], k: int = 5) -> float:
    """
    Average Precision at K for a single sample.

    Since each sample has only one true hotel_cluster,
    the score is 1/rank if the actual class is found in top-k, else 0.
    """
    predicted = list(predicted[:k])

    for i, pred in enumerate(predicted):
        if pred == actual:
            return 1.0 / (i + 1.0)

    return 0.0


def mapk(y_true: Iterable[int], y_pred: Iterable[Sequence[int]], k: int = 5) -> float:
    """
    Mean Average Precision at K.
    """
    scores = [apk(actual, predicted, k=k) for actual, predicted in zip(y_true, y_pred)]
    return float(np.mean(scores))