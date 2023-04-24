from typing import Any
from typing import Tuple

import numpy as np


from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_curve
from sklearn.metrics import PrecisionRecallDisplay
from sklearn.metrics import RocCurveDisplay


def recall_at_precision(
    true_labels: np.ndarray,
    pred_scores: np.ndarray,
    min_precision: float = 0.95,
) -> float:
    """Compute recall at precision

    Args:
        true_labels (np.ndarray): True labels
        pred_scores (np.ndarray): Target scores
        min_precision (float, optional): Min precision for recall. Defaults to 0.95.

    Returns:
        float: Metric value
    """

    precision, recall, _ = precision_recall_curve(true_labels, pred_scores)
    metric = recall[np.where(precision >= min_precision)].max()
    return metric


def recall_at_specificity(
    true_labels: np.ndarray,
    pred_scores: np.ndarray,
    min_specificity: float = 0.95,
) -> float:
    """Compute recall at specificity

    Args:
        true_labels (np.ndarray): True labels
        pred_scores (np.ndarray): Target scores
        min_specificity (float, optional): Min specificity for recall. Defaults to 0.95.

    Returns:
        float: Metric value
    """

    fpr, tpr, _ = roc_curve(true_labels, pred_scores)
    specificity = 1 - fpr
    metric = tpr[np.where(specificity >= min_specificity)].max()
    return metric


def curves(true_labels: np.ndarray, pred_scores: np.ndarray) -> Tuple[np.ndarray]:
    """Return ROC and FPR curves

    Args:
        true_labels (np.ndarray): True labels
        pred_scores (np.ndarray): Target scores

    Returns:
        Tuple[np.ndarray]: ROC and FPR curves
    """

    def fig2numpy(fig: Any) -> np.ndarray:
        fig.canvas.draw()
        img = fig.canvas.buffer_rgba()
        img = np.asarray(img)
        return img

    pr_curve = PrecisionRecallDisplay.from_predictions(
        true_labels, pred_scores)
    pr_curve = fig2numpy(pr_curve.figure_)

    roc_curve = RocCurveDisplay.from_predictions(true_labels, pred_scores)
    roc_curve = fig2numpy(roc_curve.figure_)

    return pr_curve, roc_curve
