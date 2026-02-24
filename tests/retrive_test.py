import logging
from goftino.fetcher import fetcher
from goftino.wrapper.client import Goftino
import pandas as pd
from datetime import datetime
import os
import sys
import sqlite3

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.DEBUG) 

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

client = Goftino()

SQL_READ_CHATID = """--sql
    SELECT
        DISTINCT csc."ChatId" AS "ChatId"
    FROM "CustomerServiceChats" csc
    ORDER BY "ChatId" DESC;
"""

def read_chatids_db():

    conn = sqlite3.connect('./db/messages.db')
    chat_ids_raw = pd.read_sql_query(SQL_READ_CHATID, conn)
    conn.close()

    return chat_ids_raw

def insert_data(message_df:pd.DataFrame):

    conn = sqlite3.connect('./db/messages.db')
    message_df.to_sql('CustomerServiceChats', conn, if_exists='replace', index=False)
    conn.close()

def get_chat_list(raw_chat_ids:pd.DataFrame):

    logger.info('Fetching the last message date from the table.')
    chat_list = fetcher.fetch_all_chats_data(client, req_sleep=1, retry_limit=4)

    logger.info('Fetched ~CHAT~ meta-data successfully.')

    chat_list = pd.DataFrame(chat_list)

    chat_list = chat_list[chat_list['chat_status'] == 'closed']
    chat_list = chat_list.drop_duplicates(subset='chat_id', keep=False)

    logger.info('Chats dataframe created. Closing the connection.')

    logger.info('Comparing to previous ChatIds.')
    unfetched_chats = chat_list[~chat_list['chat_id'].isin(raw_chat_ids['ChatId'])]
    unfetched_chats = unfetched_chats.reset_index(drop=True)

    return unfetched_chats[['chat_id', 'user_id']]

def get_messages(chat_list:pd.DataFrame):

    logger.info('Started fetching ~Messages~ from goftino.')
    all_chats = []

    for i, chats in chat_list.iterrows():
        logger.info(f'Requesting to access chat_id {chats["chat_id"][:-6]}.')
        
        try:
            messages = fetcher.fetch_chats(client, [chats["chat_id"]], req_sleep=1)
            if messages:
                messages_df = pd.DataFrame(messages[0]['messages'])
                logger.info(f'Got messages for chat_id {chats["chat_id"][:-6]}.')

                messages_df['chat_id'] = chats['chat_id']
                messages_df['user_id'] = chats['user_id']
                messages_df['fetch_date'] = datetime.now()

                messages_df = messages_df.rename(
                    columns = {
                        'id_': 'MessageId',
                        'chat_id': 'ChatId',
                        'user_id': 'UserId',
                        'date': 'MessageDate',
                        'sender': 'Sender',
                        'content': 'Content',
                        'fetch_date': 'FetchedDate' 
                    }
                )

                all_chats.append(messages_df)

        except Exception as e:
            logger.error(f"Error encountered while fetching chat_id:{chats['chat_id'][:-6]} ==> {str(e)} ")

        logger.debug(f'i is {i}')
        if (i != 0 and i % 50 == 0) or i == len(chat_list) - 1:

            logger.info(f'Inserting untill {i} to db.')
            all_chats_df = pd.concat(all_chats, ignore_index=True)
            insert_data(all_chats_df)
            all_chats.clear()

def main():
    previous_chats = read_chatids_db()
    chat_list = get_chat_list(previous_chats)
    # chat_list = pd.read_pickle('temp.pkl')
    chat_list = chat_list.drop_duplicates(subset='chat_id', keep=False)
    get_messages(chat_list)


if __name__ == '__main__':
    main()