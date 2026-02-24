import unittest
from goftino.wrapper.client import Goftino
from goftino.wrapper.data_types import *
import json

class ClientTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = Goftino()

        with open('./tests/config.json', 'r') as conf_file:
            json_parsed = json.load(conf_file)

        cls.config = json_parsed


    def test_client(self):

        with self.subTest("create_chat"):

            resp_create_chat = self.client.create_chat(user_message=self.config['test_message'])
            self.assertIsInstance(resp_create_chat, Response, "Parse Error; expected Response but got something else.")
            self.assertIsInstance(resp_create_chat.data, CreateChat, "Parse Error in data; expected CreateChat response but got something else.") 

            user_id = resp_create_chat.data.user_id
            chat_id = resp_create_chat.data.chat_id

        with self.subTest("retrive_chats"):
            resp_retrive_chats = self.client.get_all_chats(limit=10)
            self.assertIsInstance(resp_retrive_chats, Response, "Parse Error; expected Response but got something else.")
            self.assertIsInstance(resp_retrive_chats.data, Chats, "Parse Error in data; expected Chats response but got something else.")

            self.assertEqual(resp_retrive_chats.data.chats[0].chat_id, chat_id, "The created chat has not inserted into chatlist of gofitno. ")
            self.assertEqual(
                resp_retrive_chats.data.chats[0].last_message.content,
                self.config['test_message'],
                "The created chat's message is conflicting with the message retrived"
            )

        with self.subTest("send_message_as_operator"):
            resp_send_message_as_operator = self.client.send_message(chat_id=chat_id, operator_id=self.config['test_operator'], message=self.config['test_response'])
            self.assertIsInstance(resp_send_message_as_operator, Response, "Parse Error; expected Response but got something else.")
            self.assertIsInstance(resp_send_message_as_operator.data, SendMessage, "Parse Error in data; expected Chats response but got something else.")
                        
        with self.subTest("retrive_single_chat"):
            resp_retrive_single_chat = self.client.get_chat(chat_id=chat_id)
            self.assertIsInstance(resp_retrive_single_chat, Response, "Parse Error; expected Response but got something else.")
            self.assertIsInstance(resp_retrive_single_chat.data, Chat, "Parse Error in data; expected Chats response but got something else.")
            self.assertIsInstance(resp_retrive_single_chat.data.messages[0], Message, "Parse Error in data.messages; expected list[Message] response but got something else.")
            self.assertEqual(
                resp_retrive_single_chat.data.messages[0].content,
                self.config['test_response'],
                "The retrived chat's message response is conflicting with the default response message."
            )


if __name__ == '__main__':
    unittest.main()