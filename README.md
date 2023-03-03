# Приложение «Продуктовый помощник»
[![status](https://github.com/alexpro2022/foodgram-project-react/actions/workflows/dockerhub_workflow.yml/badge.svg)](https://github.com/alexpro2022/foodgram-project-react/actions)
[![codecov](https://codecov.io/gh/alexpro2022/foodgram-project-react/branch/master/graph/badge.svg?token=4HIR16U0RJ)](https://codecov.io/gh/alexpro2022/foodgram-project-react)

Приложение «Продуктовый помощник» - это сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. 

## Оглавление
- [Технологии](#технологии)
- [Описание работы](#описание-работы)
- [Установка на новый хост](#установка-на-новый-хост)
- [Запуск](#запуск-парсера)
- [Автор](#автор)

## Технологии 
[![Python](https://warehouse-camo.ingress.cmh1.psfhosted.org/7c5873f1e0f4375465dfebd35bf18f678c74d717/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f7072657474797461626c652e7376673f6c6f676f3d707974686f6e266c6f676f436f6c6f723d464645383733)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/-Pytest-464646?logo=pytest)](https://docs.pytest.org/en/latest/)
[![Django](https://www.djangoproject.com/m/img/badges/djangoproject120x25.gif)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?logo=Django)](https://www.django-rest-framework.org/)
[![DJoser](https://img.shields.io/badge/-DJoser-464646?logo=Django)](https://djoser.readthedocs.io/en/latest/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?logo=Yandex)](https://cloud.yandex.ru/)

[⬆️Оглавление](#оглавление)


## Описание работы


[⬆️Оглавление](#оглавление)


## Установка на новый хост

### I. Подготовка сервера
1. Убедитесь, что на виртуальной машине установлен и запущен Docker и плагин Docker Compose:
    ```
    docker --version
    docker-compose --version
    ```

2. Остановите службу nginx:
    ```
    sudo systemctl stop nginx
    ```

### II. Github
1. Сделайте fork репозитория https://github.com/alexpro2022/foodgram-project-react

2. Отредактируйте значение secrets.HOST:
    из вашего репозитория -> Settings -> Secrets -> Actions -> HOST -> Update -> укажите IP вашего сервера

### III. Ваш компьютер   
1. Клонируйте новый репозиторий себе на компьютер.

2. Отредактируйте server_name в infra/nginx.conf (укажите IP своего сервера)

3. Скопируйте файлы docker-compose.yml и nginx.conf из вашего проекта на ваш сервер в домашнюю папку. 
    Из папки infra проекта на локальной машине выполните команды:
    ```
    scp docker-compose.yaml <your_username>@<server_IP>:/home/<your_username>
    scp nginx.conf <your_username>@<server_IP>:/home/<your_username>
    ```

4. Отправьте отредактированный проект на Github, выполнив команды из корневой папки проекта:
    ```
    git add .
    git commit -m 'ваше сообщение'
    git push
    ```

### IV. Сервер
1. Войдите в домашнюю папку home/<username>/ на свой удаленный сервер в облаке.

2. Проект будет развернут в три контейнера (db, web, nginx). Посмотреть информацию о состоянии которых можно с помощью команды:
    ```
    $ sudo docker ps
    ```

3. В контейнере web уже произведены следующие действия:    
  * выполнены миграции
  * заполнена начальными данными БД
  * собрана статика 

4. В контейнере web нужно:
  * создать суперпользователя командой:
    ```
    sudo docker-compose exec web python manage.py createsuperuser
    ```

[⬆️Оглавление](#оглавление)


## Проект развернут на сервере: 
### IP 84.252.138.7
### Доступные ресурсы:
admin/ login:adm@adm.ru, password: 111

Logins of installed test users with common password 111:
```
-bingobongo@yamdb.fake
-capt_obvious@yamdb.fake
-faust@yamdb.fake
-reviewer@yamdb.fake
-angry@yamdb.fake
```

[⬆️Оглавление](#оглавление)


## Автор
[Проскуряков Алексей](https://github.com/alexpro2022)

[⬆️В начало](#Приложение-«Продуктовый-помощник»)