# StatTron

## Инициализируем главную папку как корень приложения 
```shell
export PYTHONPATH=$PYTHONPATH:$(pwd)
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
gunicorn main:app --reload --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:9876
```


