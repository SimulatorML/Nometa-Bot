from src.app.constants import PATTERNS_META_QUESTIONS
from src.models.tfidf_text_classifier.model import TfidfTextClassifier


def сheck_question_pattern(message: str) -> bool:
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


def сheck_question_with_tfidf_model(message: str) -> bool:
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
