# Приложение Продуктовый помощник
[![status](https://github.com/alexpro2022/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/alexpro2022/foodgram-project-react/actions)
[![codecov](https://codecov.io/gh/alexpro2022/foodgram-project-react/branch/master/graph/badge.svg?token=4HIR16U0RJ)](https://codecov.io/gh/alexpro2022/foodgram-project-react)

Приложение «Продуктовый помощник» - это сайт, на котором пользователи могут публиковать рецепты, добавлять рецепты в избранное и подписываться на публикации других авторов. 
Сервис «Список покупок» позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. 


## Оглавление
- [Технологии](#технологии)
- [Описание работы](#описание-работы)
- [Установка и запуск](#установка-и-запуск)
- [Удаление](#удаление)
- [Автор](#автор)



## Технологии
<details><summary>Развернуть</summary>

**Языки программирования, библиотеки и модули:**

[![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue?logo=python)](https://www.python.org/)
[![base64](https://img.shields.io/badge/-base64-464646?logo=python)](https://docs.python.org/3/library/base64.html)
[![csv](https://img.shields.io/badge/-csv-464646?logo=python)](https://docs.python.org/3/library/csv.html)
[![os](https://img.shields.io/badge/-os-464646?logo=python)](https://docs.python.org/3/library/os.html)
[![re](https://img.shields.io/badge/-re-464646?logo=python)](https://docs.python.org/3/library/re.html)
[![shutil](https://img.shields.io/badge/-shutil-464646?logo=python)](https://docs.python.org/3/library/shutil.html)
[![sys](https://img.shields.io/badge/-sys-464646?logo=python)](https://docs.python.org/3/library/sys.html)
[![tempfile](https://img.shields.io/badge/-tempfile-464646?logo=python)](https://docs.python.org/3/library/tempfile.html)


**Фреймворк, расширения и библиотеки:**

[![Django](https://img.shields.io/badge/-Django-464646?logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?logo=drf)](https://www.django-rest-framework.org/)
[![DJoser](https://img.shields.io/badge/-DJoser-464646?logo=DJoser)](https://djoser.readthedocs.io/en/latest/)
[![django-filter](https://img.shields.io/badge/-django--filter-464646?logo=)](https://pypi.org/project/django-filter/)


**База данных:**

[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)


**Тестирование:**

[![Pytest](https://img.shields.io/badge/-Pytest-464646?logo=Pytest)](https://docs.pytest.org/en/latest/)
[![Pytest-cov](https://img.shields.io/badge/-Pytest--cov-464646?logo=Pytest)](https://pytest-cov.readthedocs.io/en/latest/)
[![Coverage](https://img.shields.io/badge/-Coverage-464646?logo=Python)](https://coverage.readthedocs.io/en/latest/)


**CI/CD:**

[![GitHub_Actions](https://img.shields.io/badge/-GitHub_Actions-464646?logo=GitHub)](https://docs.github.com/en/actions)
[![docker_hub](https://img.shields.io/badge/-Docker_Hub-464646?logo=docker)](https://hub.docker.com/)
[![docker_compose](https://img.shields.io/badge/-Docker%20Compose-464646?logo=docker)](https://docs.docker.com/compose/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?logo=gunicorn)](https://gunicorn.org/)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?logo=Yandex)](https://cloud.yandex.ru/)
[![Telegram](https://img.shields.io/badge/-Telegram-464646?logo=Telegram)](https://core.telegram.org/api)

[⬆️Оглавление](#оглавление)
</details>


## Описание работы
Сайт Foodgram, «Продуктовый помощник» - это онлайн-сервис и API для него. На этом сервисе пользователи ммогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

[⬆️Оглавление](#оглавление)



## Установка и запуск:
Удобно использовать принцип copy-paste - копировать команды из GitHub Readme и вставлять в командную строку Git Bash или IDE (например VSCode).
### Предварительные условия:
<details><summary>Развернуть</summary>

Предполагается, что пользователь:
 - создал аккаунт [DockerHub](https://hub.docker.com/), если запуск будет производиться на удаленном сервере.
 - установил [Docker](https://docs.docker.com/engine/install/) и [Docker Compose](https://docs.docker.com/compose/install/) на локальной машине или на удаленном сервере, где проект будет запускаться в контейнерах. Проверить наличие можно выполнив команды:
    ```bash
    docker --version && docker-compose --version
    ```
</details>
<hr>
<details>
<summary>Локальный запуск</summary> 

**!!! Для пользователей Windows обязательно выполнить команду:** иначе файл start.sh при клонировании будет бракован:
```bash
git config --global core.autocrlf false
```

1. Клонируйте репозиторий с GitHub и введите данные для переменных окружения (значения даны для примера, но их можно оставить):
```bash
git clone https://github.com/alexpro2022/foodgram-React-DRF.git && \
cd foodgram-React-DRF && \
cp env_example .env && \
nano .env
```

2. Из корневой директории проекта выполните команду:
```bash
docker compose -f infra/local/docker-compose.yml up -d --build
```
Проект будет развернут в трех docker-контейнерах (db, web, nginx) по адресу http://localhost.

3. Остановить docker и удалить контейнеры можно командой из корневой директории проекта:
```bash
docker compose -f infra/local/docker-compose.yml down
```
Если также необходимо удалить тома базы данных, статики и медиа:
```bash
docker compose -f infra/local/docker-compose.yml down -v
```
<hr></details>

<details>
<summary>Запуск на удаленном сервере</summary>

1. Сделайте [форк](https://docs.github.com/en/get-started/quickstart/fork-a-repo) в свой репозиторий.

2. Создайте Actions.Secrets согласно списку ниже (значения указаны для примера) + переменные окружения из env_example файла:
```py
PROJECT_NAME 
SECRET_KEY

CODECOV_TOKEN

DOCKERHUB_USERNAME
DOCKERHUB_PASSWORD

# Данные удаленного сервера и ssh-подключения:
HOST
USERNAME 
SSH_KEY 
PASSPHRASE

# Учетные данные Телеграм-бота для получения сообщения о успешном завершении workflow
TELEGRAM_USER_ID= 
TELEGRAM_BOT_TOKEN= 
```

3. Запустите вручную workflow, чтобы автоматически развернуть проект в трех docker-контейнерах (db, web, nginx) на удаленном сервере.
</details>
<hr>

При первом запуске будут автоматически произведены следующие действия:    
  * выполнены миграции БД
  * БД заполнена начальными данными
  * создан суперюзер (пользователь с правами админа) с учетными данными из переменных окружения `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`
  * собрана статика 

Вход в админ-зону осуществляется по адресу: `http://hostname/admin/` .
Увидеть спецификацию API можно по адресу `http://hostname/api/docs/` , где `hostname`: 
  * `localhost`
  * IP-адрес удаленного сервера  

Учетные данные тестовых аккаунтов для входа в приложение:
  * пароль - 111 (можно поменять для каждого пользователя, включая тестовых)
  * поле email:
      ```py
      bingobongo@yamdb.fake
      capt_obvious@yamdb.fake
      faust@yamdb.fake
      reviewer@yamdb.fake
      angry@yamdb.fake
      ```

[⬆️Оглавление](#оглавление)


## Удаление:
Для удаления проекта выполните команду:
```bash
cd .. && rm -fr foodgram-React-DRF
```

[⬆️Оглавление](#оглавление)


## Автор
[Проскуряков Алексей](https://github.com/alexpro2022)

[⬆️В начало](#Приложение-Продуктовый-помощник)
