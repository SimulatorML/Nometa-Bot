from typing import Tuple

from src.app.constants import PATTERNS_META_QUESTIONS
from src.models.tfidf_text_classifier.model import TfidfTextClassifier
from src.models.bert_classfier.model import BertClassifier


def check_question_pattern(message: str) -> bool:
    """
    Функция проверяет, является ли сообщение мета-вопросом.

    Parameters
    ----------
    message : str
        Сообщенние от пользователя.

    Returns
    -------
    bool
        True, если сообщение - мета вопрос.
        False, если сообщение - обычный вопрос.
    """
    message = message.lower()
    for meta_question in PATTERNS_META_QUESTIONS:
        if meta_question in message:
            return True
    return False


def check_question_with_tfidf_model(message: str) -> bool:
    """
    TODO: add descriptions
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
    TODO: add descriptions
    """
    if "?" in message and len(message) > 20:
        model = BertClassifier(model_path="../src/models/bert_classfier/artifacts")
        prediction = model.predict(message)
        score = model.predict_proba(message)
        info = f"""
Message: {message}\n
Predict: {prediction}\n
Logit: {score}\n
Current threshold: {model.threshold}"""
    else:
        prediction = 0
        info = f"This is message: {message} is not a question"
    return bool(prediction), info
