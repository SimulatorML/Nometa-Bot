import pytest
import numpy as np
from src.metrics import Metrics


@pytest.fixture
def true_labels():
    return np.array([1, 0, 1, 1, 0, 0])


@pytest.fixture
def pred_scores():
    return np.array([0.8, 0.7, 0.6, 0.5, 0.3, 0.15])


def test_recall_at_precision(true_labels, pred_scores):
    metrics = Metrics()
    result = metrics.recall_at_precision(true_labels, pred_scores, 0.8)
    assert isinstance(result, float)
    assert np.isclose(round(result, 2), 0.33)



def test_recall_at_specificity(true_labels, pred_scores):
    metrics = Metrics()
    result = metrics.recall_at_specificity(true_labels, pred_scores, 0.8)
    assert isinstance(result, float)
    assert np.isclose(round(result, 2), 0.33)


def test_curves(true_labels, pred_scores):
    metrics = Metrics()
    pr_curve, roc_curve = metrics.curves(true_labels, pred_scores)
    assert isinstance(pr_curve, np.ndarray)
    assert isinstance(roc_curve, np.ndarray)
