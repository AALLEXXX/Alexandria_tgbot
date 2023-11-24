import sqlite3


class Database:
    def __init__(self, database_file):
        """
        Инициализация объекта Database.
        Args:
            database_file (str): Путь к файлу базы данных SQLite.
        """
        self.conn = sqlite3.connect(database_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def add_queue(self, chat_id, sex):
        """
        Добавляет пользователя в очередь.

        Args:
            chat_id (int): Идентификатор чата пользователя.
            sex (str): Пол пользователя.
        """
        with self.conn:
            result = self.cursor.execute("SELECT * FROM 'users' WHERE chat_id = ?", (chat_id,)).fetchone()
            self.cursor.execute("INSERT INTO 'queue' ('chat_id', 'sex', 'user_gender') VALUES (?,?,?)",
                                (chat_id, sex, result[1],))

    def stop_queue(self, chat_id):
        """
        Останавливает поиск для пользователя и удаляет его из очереди.

        Args:
            chat_id (int): Идентификатор чата пользователя.
        """
        with self.conn:
            self.cursor.execute("DELETE FROM 'queue' WHERE chat_id = ?", (chat_id,))

    # проверка стоит ли кто-то в поиске
    def check_queue(self):
        """
        Проверка, стоит ли кто-то в поиске.

        Returns:
            bool: True, если кто-то в поиске, иначе False.
        """
        with self.conn:
            self.cursor.execute("SELECT COUNT(*) FROM queue")
            count = self.cursor.fetchone()[0]
            if count > 0:
                return True
            else:
                return False

    def check_user_in_queue(self, chat_id):
        """
        Проверка, стоит ли пользователь в очереди.
        Args:
            chat_id (int): Идентификатор чата пользователя.

        Returns:
            bool: True, если пользователь в очереди, иначе False.
        """
        with self.conn:
            result = self.cursor.execute("SELECT * FROM queue WHERE chat_id = ?", (chat_id,)).fetchone()
            if result:
                return True
            else:
                return False

    def create_chat(self, chat_one, chat_two) -> bool:
        """
        Создает чат между двумя пользователями и удаляет их из очереди.

        Args:
            chat_one (int): Идентификатор первого пользователя.
            chat_two (int): Идентификатор второго пользователя.

        Returns:
            bool: True, если чат успешно создан.
        """
        with self.conn:
            self.cursor.execute("DELETE FROM 'queue' WHERE chat_id = ?", (chat_one,))
            self.cursor.execute("DELETE FROM 'queue' WHERE chat_id = ?", (chat_two,))
            self.cursor.execute("INSERT INTO 'chats' ('chat_one', 'chat_two') VALUES (?,?)", (chat_one, chat_two,))
            return True

    def get_active_chat(self, chat_id):
        """
        Получение активного чата пользователя
        """
        with self.conn:
            columns = ['chat_one', 'chat_two']
            for column in columns:
                query = f"SELECT * FROM chats WHERE {column} = ?"
                self.cursor.execute(query, (chat_id,))
                result = self.cursor.fetchone()
                if result:
                    if column == 'chat_two':
                        result = (result[0], result[2], result[1])
                    return result
            else:
                return False

    def stop_chat(self, chat_id):
        """
        Удаление общего чата из базы данных
        :param chat_id: идентификатор пользователя
        """
        with self.conn:
            self.cursor.execute("DELETE FROM 'chats' WHERE chat_one = ? OR chat_two = ?", (chat_id, chat_id,))

    def check_active_chat(self, chat_id) -> bool:
        """
        Проверка есть ли у пользователя активный чат
        :param chat_id: id пользователя
        :return: true - если чат создан
        """
        with self.conn:
            self.cursor.execute("SELECT * FROM 'chats' WHERE chat_one = ? OR chat_two = ?", (chat_id, chat_id,))
            result_chats = self.cursor.fetchone()
            if result_chats:
                if result_chats[1] != result_chats[2]:
                    return True
            else:
                return False

    def add_sex(self, chat_id, sex):
        """
        Добавляет пол пользователя в базу данных при регистрации
        :param chat_id: id пользователя
        :param sex: пол
        """
        with self.conn:
            self.cursor.execute("INSERT INTO 'users' ('chat_id', 'sex') VALUES (?,?)", (chat_id, sex,))

    def get_sex(self, chat_id):
        """
        Получаем пол собеседника, которого ищет пользователь
        :param chat_id:
        :return: если данных нет то вернет False
        """
        with self.conn:
            self.cursor.execute("SELECT * FROM 'users' WHERE chat_id = ?", (chat_id,))
            result = self.cursor.fetchone()
            if result:
                return result[1]
            else:
                return False

    def save_sticker_id(self, sticker_id, chat_id):
        """

        :param sticker_id:
        :param chat_id:
        :return:
        """
        with self.conn:
            self.cursor.execute("UPDATE queue SET sticker_id = ? WHERE chat_id = ?", (sticker_id, chat_id,))

    def get_sticker_id(self, chat_id):
        with self.conn:
            result = self.cursor.execute("SELECT * FROM queue WHERE chat_id = ?", (chat_id,)).fetchone()
            return result[4]


    def check_sex(self, user0_id, sex_user0):
        """
        Проверяет, совпадают ли поиск по полу и стоящих в очереди.

        Args:
            user0_id (int): Идентификатор пользователя, инициировавшего поиск.
            sex_user0 (str): Пол пользователя, инициировавшего поиск.

        Returns:
            bool: True, если есть совпадение по полу в очереди, иначе False.
        """
        with self.conn:
            gender_user0 = (self.cursor.execute("SELECT * FROM 'users' WHERE chat_id = ?", (user0_id,)).fetchone()[1])

            if sex_user0 == 'any':
                result = self.cursor.execute("SELECT * FROM queue WHERE (sex = ? OR sex = ?)",
                                             (gender_user0, 'any',)).fetchone()
                if result:
                    return result[1]
                else:
                    return False
            else:
                result = self.cursor.execute("SELECT * FROM queue WHERE (sex = ? OR sex = ?) AND (user_gender = ?)",
                                             (gender_user0, 'any', sex_user0,)).fetchone()
                if result:
                    return result[1]
                else:
                    return False
