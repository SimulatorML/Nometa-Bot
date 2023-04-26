from typing import Any
from typing import Tuple

import numpy as np
import logging

from sklearn.metrics import (
    precision_recall_curve,
    roc_curve,
    PrecisionRecallDisplay,
    RocCurveDisplay,
    confusion_matrix,
)
import seaborn as sns
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('MetricsCalculator')


class MetricsCalculator:

    def get_metrics(self,
                    true_labels: np.ndarray,
                    pred_scores: np.ndarray,
                    min_precision: float = 0.95):
        rec_at_pre = self.recall_at_precision(
            true_labels, pred_scores, min_precision
        )
        rec_at_spec = self.recall_at_specificity(
            true_labels, pred_scores, min_precision
        )

        logger.info(f"recall@precision {min_precision * 100}% : {rec_at_pre}")
        logger.info(f"recall@specificity {min_precision * 100}% : {rec_at_spec}")

        self.construction_confusion_matrix(true_labels, pred_scores)

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def curves(true_labels: np.ndarray, pred_scores: np.ndarray) -> Tuple[
        np.ndarray]:
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

    @staticmethod
    def construction_confusion_matrix(
            true_labels: np.ndarray,
            predictions_labels: np.ndarray):
        """
        Outputs a confusion matrix
        Args:
            true_labels (np.ndarray): True labels
            predictions_labels (np.ndarray): Target scores
        """
        cm = confusion_matrix(true_labels, predictions_labels)
        sns.heatmap(cm, annot=True, cmap='Blues', fmt='g')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.show()
