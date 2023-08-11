import re
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

class TfidfTextClassifier:
    """
    The TfidfTextClassifier class is designed for text classification using TfidfVectorizer
    and LogisticRegression algorithms. This class has methods for model training, saving
    and loading the model, and making predictions.
    """

    def __init__(self, estimator=LogisticRegression()):
        """
        Initializes the TfidfTextClassifier.

        Parameters
        ----------
        estimator : estimator, optional
            Estimator to use for classification, by default LogisticRegression().
        """
        self.clf = estimator
        self.vectorizer = TfidfVectorizer(ngram_range=(2, 3))
        self.pipeline = Pipeline(
            [('tfidf', self.vectorizer), ('clf', self.clf)])

    def fit(self, feature: pd.Series, target: pd.Series):
        """
        Trains the model using the LogisticRegression algorithm.

        Parameters
        ----------
        feature : pd.Series
            Input feature data.
        target : pd.Series
            Target labels for the classification.
        """
        feature = feature.astype('U').apply(self._preprocess_text)
        target = target.astype('int')

        self.pipeline.fit(feature, target)

    def predict(self, text: str) -> int:
        """
        Makes a prediction for the input text.

        Parameters
        ----------
        text : str
            Input text for prediction.

        Returns
        -------
        int
            Predicted label as an integer.
        """
        text = self._preprocess_text(text)
        text = self.vectorizer.transform([text])
        label = self.clf.predict(text)
        predict = int(label[0])
        return predict

    def predict_proba(self, text: str) -> int:
        """
        Computes the probability estimates for the input text.

        Parameters
        ----------
        text : str
            Input text for prediction.

        Returns
        -------
        float
            Probability estimate for the positive class.
        """
        text = self._preprocess_text(text)
        text = self.vectorizer.transform([text])
        probability = self.clf.predict_proba(text)
        probability = probability[0][1]
        return probability

    @staticmethod
    def _preprocess_text(text: str) -> str:
        """
        Preprocesses the input text.

        Parameters
        ----------
        text : str
            Input text to preprocess.

        Returns
        -------
        str
            Preprocessed version of the input text.
        """
        text = re.sub(r'[^А-Яа-яёЁ]', ' ', text.lower())
        return text

    def save_model(self,
                   path_to_model: str = 'model.pkl',
                   path_to_vectorizer: str = 'vectorizer.pkl'):
        """
        Saves the trained model and vectorizer to specified file paths.

        Parameters
        ----------
        path_to_model : str, optional
            Path to save the model, by default 'model.pkl'.
        path_to_vectorizer : str, optional
            Path to save the vectorizer, by default 'vectorizer.pkl'.
        """
        joblib.dump(self.clf, path_to_model)
        joblib.dump(self.vectorizer, path_to_vectorizer)

    def load_model(self,
                   path_to_model: str = 'model.pkl',
                   path_to_vectorizer: str = 'vectorizer.pkl'):
        """
        Loads the trained model and vectorizer from specified file paths.

        Parameters
        ----------
        path_to_model : str, optional
            Path to load the model, by default 'model.pkl'.
        path_to_vectorizer : str, optional
            Path to load the vectorizer, by default 'vectorizer.pkl'.
        """
        self.clf = joblib.load(path_to_model)
        self.vectorizer = joblib.load(path_to_vectorizer)
        self.pipeline = Pipeline(
            [('tfidf', self.vectorizer), ('clf', self.clf)])
