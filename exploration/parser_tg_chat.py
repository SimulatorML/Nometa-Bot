import json
import pandas as pd
from typing import List


def definition_question_idx(data: json):
    id_messages_with_nometa = []
    for info_message in data['messages']:
        message = str(info_message['text'])
        if 'nometa' in message:
            try:
                id_message_nometa = info_message['reply_to_message_id']
                id_messages_with_nometa.append(id_message_nometa)
            except:
                # сообщения без реплая
                pass
    return id_messages_with_nometa


def definition_message_text(data: json, id_messages_with_nometa: List):
    messages_with_nometa = pd.DataFrame(columns=['text'])
    for info_message in data['messages']:
        if info_message['id'] in id_messages_with_nometa:
            message = str(info_message['text'])
            new_message = pd.DataFrame({'text': message}, index=[0])
            messages_with_nometa = (
                pd.concat([messages_with_nometa, new_message],
                          ignore_index=True)
            )
    return messages_with_nometa


def parse_nometa_questions(path_to_file: str):
    with open(path_to_file) as f:
        data = json.load(f)

    id_messages_with_nometa = definition_question_idx(data)
    messages_with_nometa = definition_message_text(data,
                                                   id_messages_with_nometa)

    return messages_with_nometa


if __name__ == '__main__':
    # Путь до экспортированного чата (json)
    path_to_export_chat = '/home/user/Загрузки/Telegram Desktop/ChatExport_2023-04-19/result.json'

    messages_with_nometa = parse_nometa_questions(path_to_export_chat)
    messages_with_nometa.to_csv('messages_with_nometa.csv')
