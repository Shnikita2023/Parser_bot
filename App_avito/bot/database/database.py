import sqlite3
from sqlite3 import OperationalError
from bot.config_data import Config, load_config

# Загружаем конфиг в переменную config
config: Config = load_config()


class SqLiteClient:
    """Шаблон работы с БД"""
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.conn = None

    def create_conn(self) -> None:
        """Создание подключение"""
        try:
            self.conn = sqlite3.connect(self.filepath, check_same_thread=False)
        except Exception as Ex:
            print(f"Ошибка подключение к БД {Ex}")

    def close_conn(self):
        """Закрытие подключение"""
        self.conn.close()

    def exucute_command(self, command: str, params: tuple) -> None:
        """Запрос на различные операции в БД"""
        if self.conn is not None:
            self.conn.execute(command, params)
            self.conn.commit()
        else:
            raise ConnectionError("Вы не создали подключение")

    def exucute_select_command(self, command: str):
        """Запрос на выборку данных в БД"""
        if self.conn is not None:
            cur = self.conn.cursor()
            cur.execute(command)
            return cur.fetchall()
        else:
            raise ConnectionError("Вы не создали подключение")


class User:
    """База данных с работой пользователя"""
    CREATE_USER = """
        INSERT INTO users (user_id, username, chat_id) VALUES (?, ?, ?)
    """
    GET_USER = """
        SELECT * FROM users WHERE user_id = %s;
    """

    GET_ID = """
        SELECT id FROM users WHERE user_id = %s;
    """

    def __init__(self, database_client: SqLiteClient):
        self.database_client = database_client


    def setup(self):
        self.database_client.create_conn()

    def shutdown(self):
        self.database_client.close_conn()


    def get_user(self, user_id: int) -> tuple | list:
        user = self.database_client.exucute_select_command(self.GET_USER % user_id)
        return user[0] if user else []


    def create_user(self, user_id: int, username: str, chat_id: int):
        try:
            self.database_client.exucute_command(self.CREATE_USER, (user_id, username, chat_id))
        except OperationalError as Ex:
            print(f'Ошибка создание пользователя {Ex}')


    def get_id(self, user_id: int):
        id_users = self.database_client.exucute_select_command(self.GET_ID % user_id)
        return id_users[0]


class Offer(User):
    GET_OFFER = f"""
          SELECT offers.offer_id FROM offers
          INNER JOIN users
                ON users.id = offers.users_id
          WHERE offers.offer_id = %s AND user_id = %s;
      """
    INSERT_OFFER = """
            INSERT INTO offers (offer_id, title, price, address, url, date, users_id) VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    def check_id_offer(self, offer_id: int, user_id: int):
        try:
            offer = self.database_client.exucute_select_command(self.GET_OFFER % (offer_id, user_id))
            id_users = self.get_id(user_id=user_id)
            return offer if offer else id_users
        except OperationalError as Ex:
            print(f"Ошибка получение offers_id ### {Ex}")


    def insert_offer(self, offer: tuple):
        try:
            self.database_client.exucute_command(self.INSERT_OFFER, offer)
        except OperationalError as Ex:
            print(f'Ошибка добавление данных в таблицу offers {Ex}')

if __name__ == '__main__':
    offer = Offer(database_client=SqLiteClient("Avito.db"))
    offer.setup()
    print(offer.get_user(user_id=1668957907))
    # offer.check_id_offer(offer_id=1514119240, user_id=1668957907)

