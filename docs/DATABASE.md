# Docker-compose
### Чистим кэш докеров
```shell
sudo docker stop $(sudo docker ps -a -q)
sudo docker rm $(sudo docker ps -a -q)
```
### Поднять docker-compose
```shell
docker compose -f docker-compose.yaml up -d
```

### Положить docker-compose
```shell
docker compose -f docker-compose.yaml down
docker network prune --force
```
