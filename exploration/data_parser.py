import json
import csv
import asyncio
import os
from typing import List
import pandas as pd
from telethon import TelegramClient

API_ID = os.getenv("API_ID")  # YOUR API_ID FROM https://my.telegram.org/apps
API_HASH = os.getenv("API_HASH")  # YOUR API_HASH FROM https://my.telegram.org/apps


def find_nometa_replies(data: dict) -> List[int]:
    """
    Finds all replies to messages containing 'nometa' in json-like data.

    Parameters
    ----------
    data : dict
        JSON-like data containing chat messages.

    Returns
    -------
    List[int]
        List of message IDs that are replies to 'nometa' messages.
    """
    id_messages_with_nometa = []
    for info_message in data['messages']:
        message = str(info_message['text'])
        if 'nometa' in message:
            try:
                id_message_nometa = info_message['reply_to_message_id']
                id_messages_with_nometa.append(id_message_nometa)
            except:
                # messages without reply
                pass
    return id_messages_with_nometa


def exctract_nometa(data: dict, id_messages_with_nometa: List[int], path: str = 'data.csv'):
    """
    Extracts all questions and converts them to a .csv file.

    Parameters
    ----------
    data : dict
        JSON-like data containing chat messages.
    id_messages_with_nometa : List[int]
        List of message IDs that are replies to 'nometa' messages.
    path : str, optional
        Path for saving the CSV file, by default 'data.csv'.
    """
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


def parse_json(source: List[str] = None, path: str = 'data.csv'):
    """
    Parses data from telegram chats using JSON files and converts to CSV.

    Parameters
    ----------
    source : List[str], optional
        List of paths to JSON files, by default None.
    path : str, optional
        Path for saving the CSV file, by default 'data.csv'.
    """
    for file in source:
        with open(file, encoding="utf-8") as f:
            data = json.load(f)

        ids = find_nometa_replies(data)
        exctract_nometa(data, ids, path=f"{file}_{path}")


async def parse_api(source: List[str],
                    api_id: int,
                    api_hash: str,
                    path: str = "data.csv",
                    word: str = "nometa",
                    limit: int = 10000000):
    """
    Parses data from telegram chats using TG API and converts to CSV.

    Parameters
    ----------
    source : List[str]
        List of chat IDs.
    api_id : int
        Your Telegram API ID.
    api_hash : str
        Your Telegram API hash.
    path : str, optional
        Path for saving the CSV file, by default 'data.csv'.
    word : str, optional
        Keyword to search for in messages, by default 'nometa'.
    limit : int, optional
        Maximum number of messages to retrieve, by default 10000000.
    """
    meta_messages_ids = []
    meta_messages = []
    async with TelegramClient('my', api_id, api_hash) as client:
        i = 0
        for chat in source:
            all_message = await client.get_messages(chat, search=word, limit=limit)
            for message in all_message:
                if 'nometa' in message.message:
                    try:
                        meta_messages_ids.append(
                            message.reply_to.reply_to_msg_id)
                    except:
                        continue
            for message in meta_messages_ids:
                meta_message = await client.get_messages(chat, ids=message)
                try:
                    meta_messages.append((i, meta_message.message))
                    i += 1
                except:
                    continue
            with open(f'{chat.split("/")[3]}_{path}', "w", encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(meta_messages)


if __name__ == "__main__":

    chats = [
        "chats"
    ]
    jsons = ["your_jsons"]
    parse_json(jsons)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parse_api(chats, API_ID, API_HASH))
