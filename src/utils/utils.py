from typing import List
from util_variables import patterns_meta_questions



def is_meta_question(message: str, templates: List[str]) -> bool:
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
    for meta_question in templates:
        if meta_question in message:
            return True
    return False
