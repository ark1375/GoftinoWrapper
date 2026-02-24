import sqlite3

conn = sqlite3.connect('./db/messages.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS CustomerServiceChats (
    MessageId TEXT, 
    ChatId TEXT, 
    UserId TEXT, 
    MessageDate TEXT, 
    FetchedDate TEXT, 
    Sender TEXT, 
    Content TEXT,
    PRIMARY KEY (MessageId, ChatId, UserId)
);
''')

conn.commit()
conn.close()