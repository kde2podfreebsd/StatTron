## Инициализируем главную папку как корень приложения
```shell
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

## Меняем Config.ini
```shell
[POSTGRESQL]
host = <docker inspect testdb | grep IPAddress>
port = 5432
database = postgres
user = postgres
password = postgres

[POSTGRESQL_TEST]
host = <docker inspect testdb | grep IPAddress>
port = 5432
database = postgres_test
user = postgres_test
password = postgres_test

[MainNode]
host = <master node host>
port = <master node port>

[TELEGRAM]
adminbotapitoken = <tg_bot_api_token>
admin_password = admin

[REDIS]
host = <docker inspect redis | grep IPAddress>
port = 6379
```

## Загружаем в SlaveNode/UserBotServer/session/session.session
## Запуск UserBot
```shell
SlaveNode/UserBotServer/UserBotLayer.py
```
