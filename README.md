<h2 align="center">Parser bot(Avito)</h2>


### Описание проекта:
Парсер бот (сайта Avito).
- Парсинг объявлений на покупку и продажу квартир
- Развёртывание телеграм бота
- Хранение объявление и пользователя в базе данных

### Инструменты разработки

**Стек:**
- Python >= 3.11
- Aiogram == 3
- PostgreSQL
- Docker
- Redis

## Разработка

##### 2) Клонировать репозиторий

    git clone ссылка_сгенерированная_в_вашем_репозитории

##### 3) Создать виртуальное окружение

    python -m venv venv

##### 4) Активировать виртуальное окружение


##### 5) Устанавливать зависимости:

    pip install -r req.txt

##### 6) Переименовать файл .env.example на .env и изменить на свои данные

##### 7) Установить docker на свою ОС

##### 8) Запустить контейнеры с базами данными через docker

    make up

##### 9) Выполнить команду для выполнения миграций

    alembic upgrade head

##### 10) Запустить main.py файл c корня проекта

    python main.py


