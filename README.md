# StatTron

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

## Docker-compose
#### Чистим кэш докеров
```shell
sudo docker stop $(sudo docker ps -a -q)
sudo docker rm $(sudo docker ps -a -q)
```
#### Поднять docker-compose
```shell
docker compose -f docker-compose.yaml up -d
```

#### Положить docker-compose
```shell
docker compose -f docker-compose.yaml down
docker network prune --force
```

## Миграции Alembic
#### Инициализировать миграции
```shell
cd Database
rm alembic.ini
rm -rf migrations/
alembic init migrations
```

#### Изменить sqlalchemy.url в alembic.ini
```shell
docker inspect db | grep IPAddress
----------------------------------
"SecondaryIPAddresses": null,
"IPAddress": "",
        "IPAddress": "192.168.192.2",
```
```shell
----------alembic.ini----------
postgresql://postgres:postgres@192.168.192.2:5432/postgres
```

#### Изменить target_metadata в migrations/env.py
```shell
from Database.Models.ChannelModel import Base
target_metadata = Base.metadata
```

#### Создать миграцию
```shell
alembic revision --autogenerate -m 'init'
```

#### Залить миграции
```shell
alembic upgrade heads
```

## Запуск приложения
```shell
uvicorn MasterNode.main:app --workers 4 --host 0.0.0.0 --port 9876

#or

make master_up
```
