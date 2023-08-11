import logging

import numpy as np
from numpy import ndarray
from typing import Any, Tuple

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


class Metrics:
    """
    A class to calculate various metrics and generate visualizations for model evaluation.
    """

    def get_metrics(self,
                    true_labels: np.ndarray,
                    pred_labels: np.ndarray,
                    pred_scores: np.ndarray,
                    min_precision: float = 0.95,
                    min_specificity: float = 0.95):
        """
        Calculate and display evaluation metrics based on prediction results.

        Parameters
        ----------
        true_labels : np.ndarray
            True labels.
        pred_labels : np.ndarray
            Predicted labels.
        pred_scores : np.ndarray
            Predicted scores.
        min_precision : float, optional
            Minimum precision value for calculating recall, by default 0.95.
        min_specificity : float, optional
            Minimum specificity value for calculating recall, by default 0.95.
        """
        rec_at_pre = self.recall_at_precision(
            true_labels, pred_scores, min_precision
        )
        rec_at_spec = self.recall_at_specificity(
            true_labels, pred_scores, min_specificity
        )

        logger.info(f"recall@precision {min_precision * 100}% : {rec_at_pre}")
        logger.info(
            f"recall@specificity {min_precision * 100}% : {rec_at_spec}")

        self.construction_confusion_matrix(true_labels, pred_labels)

    @staticmethod
    def recall_at_precision(
            true_labels: np.ndarray,
            pred_scores: np.ndarray,
            min_precision: float
    ) -> float:
        """
        Compute recall at a given precision.

        Parameters
        ----------
        true_labels : np.ndarray
            True labels.
        pred_scores : np.ndarray
            Predicted scores.
        min_precision : float
            Minimum precision value.

        Returns
        -------
        float
            Metric value.
        """

        precision, recall, _ = precision_recall_curve(true_labels, pred_scores)
        metric = recall[np.where(precision >= min_precision)].max()
        return metric

    @staticmethod
    def recall_at_specificity(
            true_labels: np.ndarray,
            pred_scores: np.ndarray,
            min_specificity: float
    ) -> float:
        """
        Compute recall at a given specificity.

        Parameters
        ----------
        true_labels : np.ndarray
            True labels.
        pred_scores : np.ndarray
            Predicted scores.
        min_specificity : float
            Minimum specificity value.

        Returns
        -------
        float
            Metric value.
        """

        fpr, tpr, _ = roc_curve(true_labels, pred_scores)
        specificity = 1 - fpr
        metric = tpr[np.where(specificity >= min_specificity)].max()
        return metric

    @staticmethod
    def curves(true_labels: np.ndarray, pred_scores: np.ndarray) -> Tuple[
        ndarray, ndarray]:
        """
        Return ROC and FPR curves as numpy arrays.

        Parameters
        ----------
        true_labels : np.ndarray
            True labels.
        pred_scores : np.ndarray
            Predicted scores.

        Returns
        -------
        Tuple[np.ndarray]
            ROC and FPR curves as numpy arrays.
        """

        def fig2numpy(fig: Any) -> np.ndarray:
            fig.canvas.draw()
            img = fig.canvas.buffer_rgba()
            img = np.asarray(img)
            return img

        pr_curve = PrecisionRecallDisplay.from_predictions(
            true_labels, pred_scores)
        pr_curve = fig2numpy(pr_curve.figure_)

        current_roc_curve = RocCurveDisplay.from_predictions(
            true_labels, pred_scores
        )
        current_roc_curve = fig2numpy(current_roc_curve.figure_)

        return pr_curve, current_roc_curve

    @staticmethod
    def construction_confusion_matrix(
            true_labels: np.ndarray,
            predictions_labels: np.ndarray):
        """
        Construct and display a confusion matrix.

        Parameters
        ----------
        true_labels : np.ndarray
            True labels.
        predictions_labels : np.ndarray
            Predicted labels.
        """
        conf_matrix = confusion_matrix(true_labels, predictions_labels)
        sns.heatmap(conf_matrix, annot=True, cmap='Blues', fmt='g')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.show()
