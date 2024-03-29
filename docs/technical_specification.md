# **1. Цель проекта**
**Цель проекта** - разработать telegram bot, который будет парсить объявление на продажу/cдачи квартир. 
# **2. Описание системы**
Система состоит из следующий основных функциональных блоков:
+ Создание telegram bot.
+ Парсинг сайта Avito, в дальнейшем с возможным расширением на другие платформы.
+ Подключение Базы данных с хранением информации о пользователей и их действий.
  
## **2.1 Создание telegram bot**
Данный бот будет создан на основе Telegram API, в нём будет следующие функции:
1. При старте бота будет его описание, а так же при нажатии на `/help` - будет показаны команды, которые он выполняет.
2. Основные кнопки на стартовой страницы:
   + `Парсинг`(при нажатии появиться четыре кнопки)
      > Сдача квартир посуточно

      > Сдача квартир на длительный срок

      > Продажа квартир
     
   + `Написать администратору`(можно задать любой интересующий вопрос)
   + `Дополнительно`(Расширение функционала бота, данный блок возможно будет реализован)
   + `Помощь`(будут храниться все команды, которые доступны пользователю)
        > /start - Старт бота

        >/help - Помощь 

        >/pars - Начало парсинга

        >/write_admin - Написать админу

        > /optional - Раздел дополнительно

        > /panel_admin - Панель администратора
   + `Панель администратора`(при нажатии появиться две кнопки)
     > Добавление города

     > Удаление города
  
3. После выбора любого раздела объявление в кнопке `Парсинг`, пользователь может выбрать город, свой бюджет. Дополнительно для квартир: площадь, этаж.




## **2.2 Парсинг Avito**
Основной сайт объявление будет Avito, одна из самых популярных сайтов. 
Парсинг будет происходить по городам миллионеркам. Города, которые взяты за основу:
+ Сочи, Пермь, Москва, Екатеринбург
+ Уфа, Санкт-Петербург

  
В дальнейшем администратор сможет добавить больше городов, а так же их удалять.
Основная информация, которая будет в объявление...

**Общая для всех:**
+ Заголовок
+ Цена
+ Ссылка
+ Фото 
+ Дата публикации
+ Краткое описание
  
**Дополнительно для квартир:**

+ Этаж
+ Площадь

## **2.3 База данных**
За основу выступит отрытая, современная, многофункциональная база данных PSQL. В ней будет 2 сущности:

1. offers - Предложение сдачи/покупка квартир
2. users - Хранение данных о пользователе

# **3. Предлагаемый стек технологий**
Для реализации системы предлагается следующий стек технологий:
+ Язык Python,а именно основные библиотеки:
  + Aiogram 3
  + Selenium
  + Asyncio
  + Beautiful Soup
  + Request
  + Psycopg2

+ БД PostgreSQL
+ Docker
  