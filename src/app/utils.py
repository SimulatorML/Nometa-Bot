from typing import Tuple

from src.app.constants import PATTERNS_META_QUESTIONS
from src.models.tfidf_text_classifier.model import TfidfTextClassifier
from src.models.bert_classifier.model import BertClassifier  # Updated import name

def check_question_pattern(message: str) -> bool:
    """
    Check if a message is a meta-question.

    Parameters
    ----------
    message : str
        User's message.

    Returns
    -------
    bool
        True if the message is a meta-question.
        False if the message is a regular question.
    """
    message = message.lower()
    for meta_question in PATTERNS_META_QUESTIONS:
        if meta_question in message:
            return True
    return False

def check_question_with_tfidf_model(message: str) -> bool:
    """
    Check question using the TF-IDF model.

    Parameters
    ----------
    message : str
        User's message.

    Returns
    -------
    bool
        True if the message is classified as a question, otherwise False.
    """
    model = TfidfTextClassifier()
    model.load_model(
        '../src/models/tfidf_text_classifier/artifacts/model.pkl',
        '../src/models/tfidf_text_classifier/artifacts/vectorizer.pkl'
    )
    prediction = model.predict(message)

    return bool(prediction)

def check_question_with_rubert_clf(message: str) -> Tuple[bool, str]:
    """
    Check question using the RuBERT classifier.

    Parameters
    ----------
    message : str
        User's message.

    Returns
    -------
    Tuple[bool, str]
        A tuple containing:
        - A boolean indicating if the message is a question or not.
        - Information about the prediction and details of the classification.
    """
    if "?" in message and len(message) > 10:
        model = BertClassifier(model_path="../src/models/bert_classifier/artifacts")  # Updated path
        prediction = model.predict(message)
        score = model.predict_proba(message)
        info = f"""
Message: {message}\n
Predict: {prediction}\n
Logit: {score}\n
Current threshold: {model.threshold}"""
    else:
        prediction = 0
        info = f"This message: {message} is not a question"
    return bool(prediction), info
