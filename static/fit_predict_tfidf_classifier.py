from src.models.tfidf_text_classifier.model import TfidfTextClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from src.metrics import recall_at_precision, recall_at_specificity
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('tfidf_text_classifier')


def train_model(feature: pd.Series, target: pd.Series):
    """

    :param feature: pd.Series with str texts
    :param target:
    :return:
    """
    model = TfidfTextClassifier()
    model.fit(feature, target)
    model.save_model()


def validate_model(feature: pd.Series,
                   target: pd.Series,
                   test_size: float = 0.2,
                   random_state: int = 42
                   ):
    X_train, X_test, y_train, y_test = train_test_split(
        feature, target, test_size=test_size, random_state=random_state
    )

    model = TfidfTextClassifier()
    model.fit(X_train, y_train)

    predictions = []
    for idx in range(len(X_test)):
        message = X_test.iloc[idx]
        result = model.predict(message)
        predictions.append(result)

    rec_at_pre = recall_at_precision(y_test, predictions)
    rec_at_spec = recall_at_specificity(y_test, predictions)

    logger.info(f"recall_at_precision : {rec_at_pre}")
    logger.info(f"recall_at_specificity : {rec_at_spec}")

    cm = confusion_matrix(y_test, predictions)
    sns.heatmap(cm, annot=True, cmap='Blues', fmt='g')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()


def predict_with_trained_model(message: str,
                               path_to_model: str,
                               path_to_vectorizer: str):
    model = TfidfTextClassifier()
    model.load_model(
        path_to_model=path_to_model,
        path_to_vectorizer=path_to_vectorizer
    )
    prediction = model.predict(message)
    logger.info(f'Class message: {prediction}')


if __name__ == '__main__':
    # Load dataset
    df = pd.read_csv('/home/user/Education/Nometa-Bot/docs/questions.csv')
    # Definition feature and target
    feature = df['text']
    target = df['label']

    # Validation of the model with the calculation of metrics
    # and the formation of confusions matrix
    validate_model(feature, target, test_size=0.2)

    # Model training on all data
    train_model(feature, target)

    # Getting a Prediction from the Model
    message = 'Кто может помочь с pandas?'
    path_to_model = '../src/models/tfidf_text_classifier/artifacts/model.pkl'
    path_to_vectorizer = '../src/models/tfidf_text_classifier/artifacts/vectorizer.pkl'

    predict_with_trained_model(message, path_to_model, path_to_vectorizer)

    logger.info('Done!')
