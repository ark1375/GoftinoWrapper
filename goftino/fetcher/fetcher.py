from ..wrapper.client import Goftino
from ..wrapper.data_types import *

from datetime import datetime
import time
import logging

logger = logging.getLogger("goftino_fetcher")

def fetch_all_chats_data(client: Goftino, req_sleep = 2, retry_limit = 5, last_update_date:str = None):

    i = 1
    retries = 0
    is_date_exceeded = False
    chats_list = []

    while True:
        response = client.get_all_chats(limit=50, page = i)

        if response.data == None :
            print(response)

        if isinstance(response, Error) or isinstance(response, Response) and len(response.data.chats) == 0:
            if retries < retry_limit:
                logger.debug(f"Chat List Fetch Error! Page is {i}. Retrying...")
                retries += 1
                continue

            else:
                logger.warning("Chat List Fetch Error! Page is {i}. Terminated fetching!")
                break
        
        retries = 0

        data_to_insert = []
        for chat in response.data.chats:

            if last_update_date and datetime.strptime(chat.last_message.date , "%Y-%m-%d %H:%M:%S") < datetime.strptime(last_update_date , "%Y-%m-%d %H:%M:%S"):
                is_date_exceeded = True
                break

            data_to_insert.append({
                "chat_id" : chat.chat_id,
                "last_message_date" : chat.last_message.date,
                "user_id" : chat.user_id,
                "chat_status" : chat.chat_status,
                "chat_fetch_date" : datetime.now(),
                "page" : i
            })
        
        chats_list.extend(data_to_insert)
        
        if is_date_exceeded:
            logger.warning("Message date exceeded last update date. Terminating fetching process.")
            break

        i+=1

        time.sleep(req_sleep)
    
    logger.debug('Done fetching.')

    return chats_list
        
def fetch_chats(client: Goftino, chat_ids:list , req_sleep = 2):
    
    all_chat_messages = []

    for chat_id in chat_ids:

        messages = []

        i = 1
        logger.debug(f"Getting chat: {chat_id[:-6]}.")
        
        while True:
            time.sleep(req_sleep)
            response = client.get_chat(chat_id, limit=50, page = i)

            if isinstance(response, Error) or isinstance(response.data, dict) or isinstance(response, Response) and len(response.data.messages) == 0:
                logger.debug(f"Chat: {chat_id[:-6]} ==> Page {i} not exist. Moving on.")
                break

            for message in response.data.messages:
                logger.debug(f'Got message. Message_id: {message.message_id[:-6]}')
                if message.type == 'text':
                    message_id = message.message_id
                    content = message.content
                    sender = message.sender.from_
                    date = message.date
        
                    messages.append( {'id_': message_id, 'content' : content, 'sender': sender, 'date' : date} )
            
            i += 1
        
        all_chat_messages.append(
            { "chat_id" : chat_id, "messages" : messages }
        )
    
    logger.debug("Done retriving chats.")
    return all_chat_messages

def main():

    pass
    # cl = fetch_all_chats_data(req_sleep = 2, last_update_date= "2024-12-20 00:00:00" )
    # print(cl)
    # print(len(cl))

    # chats = fetch_chats(
    #     [chat["chat_id"]  for chat in cl if chat["chat_status"] == 'closed']
    #     )
    # print(chats)
    # print(len(chats))

    # fetch_chats()
    # client = Goftino()
    # response = client.get_all_chats(limit=50, page = 87)
    # if response.status == 'success':
    #     print(f'Page Success!')
    #     print(response.data.chats[0])

if __name__ == '__main__':
    main()