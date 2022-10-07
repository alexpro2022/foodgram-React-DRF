# FOODGRAM project
![](https://github.com/alexpro2022/foodgram-project-react/actions/workflows/main.yml/badge.svg)

## Стек: 
  * каркас: django, django-restframework, djoser
  * деплой: docker, wsgi (gunicorn), nginx

## Установка на новый хост:

### I. Подготовка сервера:
1. Убедитесь, что на виртуальной машине установлен и запущен Docker и плагин Docker Compose:
    ```
    docker --version
    docker-compose --version
    ```

2. Остановите службу nginx:
    ```
    sudo systemctl stop nginx
    ```

### II. Github:
1. Сделайте fork репозитория https://github.com/alexpro2022/foodgram-project-react

2. Отредактируйте значение secrets.HOST:
    из вашего репозитория -> Settings -> Secrets -> Actions -> HOST -> Update -> укажите IP вашего сервера

### III. Ваш компьютер:   
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

### IV. Сервер:
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

## Проект развернут на сервере: 
### IP 84.252.138.7
### Доступные ресурсы:
admin/ login:adm@adm.ru, password: 111

Logins of installed test users with common password 111:
-bingobongo@yamdb.fake
-capt_obvious@yamdb.fake
-faust@yamdb.fake
-reviewer@yamdb.fake
-angry@yamdb.fake


## Автор:
[Проскуряков Алексей](https://github.com/alexpro2022)