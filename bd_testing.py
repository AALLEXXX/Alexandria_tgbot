import sqlite3

conn = sqlite3.connect('db', check_same_thread=False)
cursor = conn.cursor()

# @dp.message_handler(content_types=types.ContentType.STICKER)
# async def find_sticker_file_id(message: types.Message):
#     # Запрос к API Telegram Bot для получения обновлений
#     response = requests.get(f'https://api.telegram.org/bot{API_TOKEN}/getUpdates')
#     data = response.json()
#
#     # Перебор последних обновлений
#     for update in data['result']:
#         if 'sticker' in update['message']:
#             # Получение информации о стикере
#             sticker = update['message']['sticker']
#             file_id = sticker['file_id']
#             print('Sticker File ID:', file_id)
#             break


# def allex():
#     with conn:
#         cursor.execute("SELECT * FROM chats WHERE chat_one = ? OR chat_two = ?", ('1195685505', '1195685505'))
#         result = cursor.fetchall()
#         for row in result:
#             # Доступ к данным строки
#             print(row)

# def active_chat(chat_id):
#     with conn:
#         columns = ['chat_one', 'chat_two']
#         for column in columns:
#             query = f"SELECT * FROM 'chats' WHERE {column} = ?"
#             cursor.execute(query, (chat_id,))
#             result = cursor.fetchone()
#             if result:
#                 if column == 'chat_two':
#                     result = (result[0], result[2], result[1])
#                 print(result)
#
# def check_chat(self, chat_id):
#     with self.conn:
#         self.cursor.execute("SELECT * FROM 'chats' WHERE chat_one = ? OR chat_two = ?", (chat_id, chat_id,))
#         result_chats = self.cursor.fetchone()
#         self.cursor.execute("SELECT * FROM 'queue' WHERE chat_id = ?", (chat_id,))
#         result_queue = self.cursor.fetchone()
#         if result_chats or result_queue:
#             if result_chats:
#                 if result_chats[1] != result_chats[2]:
#                     return True
#             elif result_queue:
#                 return 'enemy'
#             else:
#                 self.cursor.execute("DELETE FROM 'chats' WHERE chat_one = ? OR chat_two = ?", (chat_id, chat_id,))
#                 return False
#         else:
#             return False
#
#
# def check_chat(self, chat_id):
#     with self.conn:
#         self.cursor.execute("SELECT * FROM 'chats' WHERE chat_one = ? OR chat_two = ?", (chat_id, chat_id,))
#         result_chats = self.cursor.fetchone()
#         self.cursor.execute("SELECT * FROM 'queue' WHERE chat_id = ?", (chat_id,))
#         result_queue = self.cursor.fetchone()
#         if result_queue:
#             return False
#         elif result_chats:
#             if result_chats[1] != result_chats[2]:
#                 return True
#             else:
#                 self.cursor.execute("DELETE FROM 'chats' WHERE chat_one = ? OR chat_two = ?", (chat_id, chat_id,))
#                 return False
#         else:
#             return False
# def get_sex(chat_id, sex):


#     with conn:
#         cursor.execute("INSERT INTO 'users' ('chat_id', 'sex') VALUES (?,?)", (chat_id, sex,))


# def check_sex(user0_id, sex_user0, user1_id):
#     with conn:
#         gender_user0 = cursor.execute("SELECT * FROM 'users' WHERE chat_id = ?", (user0_id,)).fetchone()[1]
#         info_user1 = cursor.execute("SELECT * FROM 'queue' WHERE chat_id = ?", (user1_id,)).fetchone()
#         sex_looking_user1 = info_user1[2]
#         print(gender_user0)
#         print(sex_looking_user1)
#         print(sex_user0)
#         gender_user1 = info_user1[3]
#         print(gender_user1)
#         if sex_looking_user1 == 'any' and sex_user0 == 'any':
#             return True
#         elif (gender_user0 == sex_looking_user1) and (sex_user0 == gender_user1):
#             return True
#         else:
#             return False


# def check_sex(user0_id, sex_user0):
#     with conn:
#         gender_user0 = (cursor.execute("SELECT * FROM 'users' WHERE chat_id = ?", (user0_id,)).fetchone()[1])
#
#         result = cursor.execute("SELECT * FROM queue WHERE (sex = ? OR sex = 'any')",
#                                 (gender_user0,)).fetchone()
#         result1 = cursor.execute("SELECT * FROM queue WHERE(user_gender = ?)",
#                                 (sex_user0,)).fetchone()
#         print(sex_user0)
#
#         print(type(sex_user0))
#         print(gender_user0)
#         print(type(gender_user0))
#         print(result)
#         print(result1)
#
#         if result:
#             return True
#         else:
#             return False
#
#
# check_sex(698451913, 'guy')

# def get_all_ppl_queue():
#     with conn:
#         cursor.execute("SELECT * FROM 'queue'")
#         result = cursor.fetchall()
#         print(result)


def get_active_chat(chat_id):
    with conn:
        columns = ['chat_one', 'chat_two']
        for column in columns:
            query = f"SELECT * FROM chats WHERE {column} = ?"
            cursor.execute(query, (chat_id,))
            result = cursor.fetchone()
            if result:
                if column == 'chat_two':
                    result = (result[0], result[2], result[1])
                return result
        else:
            return False

print(get_active_chat(836697711))
