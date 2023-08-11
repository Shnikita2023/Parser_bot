import psycopg2
from psycopg2 import OperationalError

from app.config import Config, load_config

# Загружаем конфиг в переменную config
config: Config = load_config()
HOST = config.bd.host
PORT = config.bd.port
USER = config.bd.user
PASSWORD = config.bd.password
DB_NAME = config.bd.db_name


class Database:
    """Шаблон работы с БД"""
    def __init__(self, filepath: str = None) -> None:
        self.filepath = filepath
        self.conn = None

    def create_conn(self) -> None:
        """Создание подключение"""
        try:
            self.conn = psycopg2.connect(user=USER,
                                         password=PASSWORD,
                                         host=HOST,
                                         port=PORT,
                                         database=DB_NAME)
        except Exception as Ex:
            print(f"Ошибка подключение к БД {Ex}")

    def close_conn(self) -> None:
        """Закрытие подключение"""
        self.conn.close()

    def exucute_command(self, command: str, params: tuple) -> None:
        """Запрос на различные операции в БД"""
        if self.conn is not None:
            cur = self.conn.cursor()
            cur.execute(command, params)
            self.conn.commit()
        else:
            raise ConnectionError("Вы не создали подключение")

    def exucute_select_command(self, command: str) -> list:
        """Запрос на выборку данных в БД"""
        if self.conn is not None:
            with self.conn.cursor() as cur:
                cur.execute(command)
                return cur.fetchall()
        else:
            raise ConnectionError("Вы не создали подключение")


class User:
    """База данных с работой пользователя"""
    CREATE_USER = """
        INSERT INTO users (user_id, username, chat_id) VALUES (%s, %s, %s)
    """
    GET_USER = """
        SELECT * FROM users WHERE user_id = %s;
    """

    GET_ID = """
        SELECT id FROM users WHERE user_id = %s;
    """

    def __init__(self, database_client: Database) -> None:
        self.database_client = database_client

    def setup(self) -> None:
        self.database_client.create_conn()

    def shutdown(self) -> None:
        self.database_client.close_conn()

    def get_user(self, user_id: int) -> tuple | list:
        user = self.database_client.exucute_select_command(self.GET_USER % user_id)
        return user[0] if user else []

    def create_user(self, user_id: int, username: str, chat_id: int) -> None:
        try:
            self.database_client.exucute_command(self.CREATE_USER, (user_id, username, chat_id))

        except OperationalError as Ex:
            print(f'Ошибка создание пользователя {Ex}')

    def get_id(self, user_id: int) -> tuple:
        id_users = self.database_client.exucute_select_command(self.GET_ID % user_id)
        return id_users[0]

#
class Offer(User):
    """База данные с данными об объявлений"""
    GET_OFFER = f"""
          SELECT offers.offer_id FROM offers
          INNER JOIN users
                ON users.id = offers.users_id
          WHERE offers.offer_id = %s AND user_id = %s AND price BETWEEN %s AND %s;
      """
    INSERT_OFFER = """
            INSERT INTO offers (offer_id, title, price, address, url, date, users_id) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    def check_id_offer(self, range_price_list: list[int], offer_id: int, user_id: int) -> tuple | list:
        try:
            price_min, price_max = range_price_list
            offer = self.database_client.exucute_select_command(
                self.GET_OFFER % (offer_id, user_id, price_min, price_max))
            id_users = self.get_id(user_id=user_id)
            return offer if offer else id_users

        except OperationalError as Ex:
            print(f"Ошибка получение offers_id ### {Ex}")

    def insert_offer(self, offer: tuple) -> None:
        try:

            self.database_client.exucute_command(self.INSERT_OFFER, offer)

        except OperationalError as Ex:
            print(f'Ошибка добавление данных в таблицу offers {Ex}')


if __name__ == '__main__':
    user = User(database_client=Database())
    user.setup()
    user.create_user(user_id=123131, username="Nikita", chat_id=1315646)
    user.shutdown()






