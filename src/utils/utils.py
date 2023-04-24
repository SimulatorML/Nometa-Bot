"""Здесь хранятся дополнительные переменные и функции для работы бота."""


patterns_meta_questions = [
    'здесь кто-нибудь работал с',
    'кто-нибудь разбирается в',
    'можно задать вопрос про',
    'кто проходил курс',
    'кто шарит за',
    'кто юзал',
    'можно задать вопрос',
]


def is_meta_question(message: str) -> bool:
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
    for meta_question in patterns_meta_questions:
        if meta_question in message:
            return True
    return False
