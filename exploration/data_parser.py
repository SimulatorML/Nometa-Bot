import json
import csv
import pandas as pd
from typing import List
from telethon import TelegramClient

api_id = ''  # YOUR API ID
api_hash = ''  # YOUR API HASH


def find_nometa_replies(data: dict):
    """Finds all nometa_replies in json-like data"""
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


def exctract_nometa(data: dict, id_messages_with_nometa: List[int], path: str = 'result.csv'):
    """Exctract all questions and converts it to .cvs"""
    messages_with_nometa = pd.DataFrame(columns=['text'])
    for info_message in data['messages']:
        if info_message['id'] in id_messages_with_nometa:
            message = str(info_message['text'])
            new_message = pd.DataFrame({'text': message}, index=[0])
            messages_with_nometa = (
                pd.concat([messages_with_nometa, new_message],
                          ignore_index=True)
            )
    return messages_with_nometa.to_csv(path)


def parse_data(mode: str = 'json', source: List[str] = None, path: str = 'path_to_save.csv'):
    """Parse data from telegram chats using api/json"""

    modes = ['json', 'api']

    if mode not in modes:
        raise ValueError(f'Unknown mode {mode}'
                         f'Only available {modes} parse modes')

    if mode == 'json':
        for file in source:
            with open(file) as f:
                data = json.load(f)

        ids = find_nometa_replies(data)
        exctract_nometa(data, ids)

    if mode == 'api':
        meta_messages_ids = []
        meta_messages = []
        with TelegramClient('my', api_id, api_hash) as client:
            i = 1
            for chat in source:
                all_message = client.get_messages(
                    chat, search='nometa', limit=1000000)
                for message in all_message:
                    if 'nometa' in message.message:
                        try:
                            meta_messages_ids.append(
                                message.reply_to.reply_to_msg_id)
                        except:
                            continue
                for message in meta_messages_ids:
                    meta_message = client.get_messages(chat, ids=message)
                    try:
                        meta_messages.append((i, meta_message))
                        i += 1
                    except:
                        continue
        with open(path, "w") as f:
            writer = csv.writer(f)
            writer.writerows(meta_messages)
