from aiogram.filters.state import State, StatesGroup


class FSMParserForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    category_pars = State()  # Состояние ожидания выбора категории парсинга
    name_city = State()  # Состояние ожидания выбора города
    price = State()  # Состояние ожидания выбора цены
