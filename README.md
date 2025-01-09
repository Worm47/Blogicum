# Blogicum

## Описание проекта
Социальная сеть для публикации постов. Пользователи имеют возможность зарегистрироваться, войти в аккаунт,
создавать и изменять посты, добавлять фото к постам, а также оставлять комментарии. Также присутствует админ-панель.

## Использованные технологии
- Python 3.9
- Django 3.2.16


## Запуск проекта локально
1. Клонируйте репозиторий
2. Создайте и активируйте виртуальное окружение `python -m venv venv`    
Bash: `source venv/Scripts/activate`, PowerShell: `venv/Scripts/activate`
3. Загрузите библиотеки `pip install -r requirements.txt`
4. Выполните миграции `python blogicum/manage.py migrate`
5. По желанию, загрузите фикстуры с заготовленными постами `python blogicum/manage.py loaddata db.json`
6. По желанию, создайте профиль админа `python blogicum/manage.py createsuperuser`
7. Запустите сервер разработки `python blogicum/manage.py runserver`

- Проект доступен локально по адресу `127.0.0.1:8000`
- Админ-панель доступна по адресу `127.0.0.1:8000/admin`

## Автор: Кобелев Влдаислав
GitHub: [worm47](https://github.com/Worm47)    
Gmail: worm0047@gmail.com
