import pytest
import numpy as np


@pytest.fixture
def true_labels():
    return np.array([0, 1, 1, 0, 1, 0])


@pytest.fixture
def pred_labels():
    return np.array([0, 1, 0, 0, 1, 0])


@pytest.fixture
def pred_scores():
    return np.array([0.1, 0.8, 0.6, 0.3, 0.7, 0.2])
