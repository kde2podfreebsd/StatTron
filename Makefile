#---------------- Requirements ----------------
.PHONY freeze:
freeze:
	pip freeze > app/requirements.txt
	pip freeze > client/requirements.txt

.PHONY deps:
deps:
	pip install -r app/requirements.txt
	pip install -r client/requirements.txt

#---------------- App [DEV] ----------------
.PHONY bot_dev:
bot:
	cd app/userBot/ && python UserAgent.py

.PHONY server_dev:
server:
	cd app/ && gunicorn --bind 0.0.0.0:5000 app:app

.PHONY db_dev:
db_dev:
	cd app/ && flask commands create_db

#---------------- App [PROD] ----------------
.PHONY master_db:
master_db:
	sudo docker exec stattron_master flask commands create_db

.PHONY slave_db:
slave_db:
	sudo docker exec stattron_slave flask commands create_db

.PHONY slave_userbot:
slave_userbot:
	sudo docker exec stattron_slave python userBot/userAgent.py

#---------------- Docker-Compose Slave --------------------------------
.PHONY docker_slave_build:
docker_slave_build:
	sudo docker-compose -f docker-compose.slave.dev.yml build

.PHONY docker_slave_up:
docker_slave_up:
	sudo docker-compose -f docker-compose.slave.dev.yml up

.PHONY docker_slave_upd:
docker_slave_upd:
	sudo docker-compose -f docker-compose.slave.dev.yml up -d

#---------------- Docker-Compose Master -------------------------------
.PHONY docker_master_build:
docker_master_build:
	sudo docker-compose -f docker-compose.master.dev.yml build

.PHONY docker_master_up:
docker_master_up:
	sudo docker-compose -f docker-compose.master.dev.yml up

.PHONY docker_master_upd:
docker_master_upd:
	sudo docker-compose -f docker-compose.master.dev.yml up -d

#---------------- Docker-Compose: PostgreSQL + PGAdmin4 ----------------
.PHONY docker_pgdb_build:
docker_pgdb_build:
	sudo docker-compose -f docker-compose.postgres.dev.yml build

.PHONY docker_pgdb_up:
docker_pgdb_up:
	sudo docker-compose -f docker-compose.postgres.dev.yml up

.PHONY grep_ipaddr: # for connect to dev db in docker container
grep_ipaddr:
	docker inspect pgdb | grep IPAddress

.PHONY docker_pgdb_upd:
docker_pgdb_upd:
	sudo docker-compose -f docker-compose.postgres.dev.yml up -d

#---------------- Docker---------------------------------------
#.PHONY docker_stop:
#docker_stop:
#	sudo docker stop $(sudo docker ps -a -q)
#
#.PHONY docker_rm:
#docker_rm:
#	sudo docker rm $(sudo docker ps -a -q)

#---------------- Clean cache ----------------
.PHONY clean:
clean:
	cd app/ && find . -name __pycache__ -type d -print0|xargs -0 rm -r --

#---------------- Git ----------------
.PHONY gadd:
gadd:
	git add .

.PHONY gcom:
gcom: # git commit -am "{com}" | com=<your comment>
	git commit -am "$(com)"

.PHONY gpush_dev:
gpush_dev:
	git push origin dev

.PHONY gpull:
gpull:
	git pull




