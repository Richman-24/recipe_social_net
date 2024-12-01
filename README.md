[![Main foodgran workflow](https://github.com/Richman-24/foodgram/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/Richman-24/foodgram/actions/workflows/main.yml)

### <br>➜ https://foodgram-rm24.zapto.org/</br>

"Foodgram" - это инновационный веб-сайт для кулинарных энтузиастов, предоставляющий уникальную платформу для обмена и открытия рецептов. Здесь пользователи могут делиться своими кулинарными шедеврами, находить вдохновение в рецептах других участников и создавать собственные кулинарные коллекции.

[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru)

## Цели проекта

Проект "Foodgram" стремится создать сообщество, объединяющее любителей готовить, где каждый сможет найти что-то новое и вдохновляющее для себя. Мы верим, что обмен рецептами помогает развивать личные кулинарные навыки и способствует культурному обмену через еду.

## Функционал

- **Публикация рецептов**: Зарегистрированные пользователи могут добавлять свои рецепты, включая описание, список ингредиентов и пошаговые инструкции.
- **Избранное**: Возможность добавлять понравившиеся рецепты в свой список избранного, чтобы всегда иметь быстрый доступ к любимым блюдам.
- **Подписки**: Подписывайтесь на других авторов, чтобы следить за их новыми публикациями и не пропускать интересные рецепты.
- **Список покупок**: Удобный сервис для зарегистрированных пользователей, который позволяет автоматически составлять список необходимых продуктов для выбранных рецептов. Это облегчит планирование покупок и приготовление пищи.


## Инструкции по запуску проекта:
1. **Клонировать репозиторий**:
   ```bash
   git clone git@github.com:icek888/foodgram.git
   ```

2. **Перейти в директорию проекта**:
   ```bash
   cd foodgram/backend/
   ```

3. **Создать и активировать виртуальное окружение** (для Windows):
   ```bash
   python -m venv venv
   source venv/Scripts/activate
   ```

4. **Установить зависимости**:
   ```bash
   pip install -r requirements.txt
   ```
   
5. **Создать файл `.env`** в корне проекта с настройками (по примеру .env.example)

6. **Запустить проект с помощью Docker**:
   ```bash
   docker compose -f docker-compose.production.yml up -d
   ```

7. **Выполнить миграции и собрать статику**:
   ```bash
   docker compose -f docker-compose.production.yml exec backend python manage.py migrate
   docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic --no-input
   ```

8. **Создать суперпользователя**:
   ```bash
   docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
   ```

8. **Наполнить базу данных предустановленными данными**:
   ```bash
   docker compose -f infra/docker-compose.production.yml exec backend python manage.py loaddata data/fixtures.json
   ```

## Примеры API-запросов

Примеры запросов, доступных через API:

- **Получение списка рецептов**:
  ```http
  GET /api/recipes/
  ```

- **Добавление рецепта в избранное**:
  ```http
  POST /api/recipes/{id}/favorite/
  Headers:
    Authorization: Bearer <токен>
  ```

- **Получение списка ингредиентов**:
  ```http
  GET /api/ingredients/
  ```

## Документация к API по ссылке:
 ```http
  https://foodgram-rm24.zapto.org/api/docs
  ```

## Вклад
Мы будем рады, если вы решите внести свой вклад в развитие Foodgram! Пожалуйста, создавайте pull-запросы и делитесь идеями.

### Автор работы
[Дреев Максим](https://github.com/richman-24) <br>
[telegram: @richman24](https://t.me/richman_24)

