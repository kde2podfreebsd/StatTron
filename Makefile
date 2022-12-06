#---------------- Requirements ----------------
freeze:
	pip freeze > app/requirements.txt
	pip freeze > client/requirements.txt

deps:
	pip install -r app/requirements.txt
	pip install -r client/requirements.txt

#---------------- App [DEV] ----------------
bot:
	cd app/userBot/ && python UserAgent.py

server:
	cd app/ && gunicorn --bind 0.0.0.0:5000 app:app

db_dev:
	cd app/ && flask commands create_db

#---------------- App [PROD] ----------------
master_db:
	sudo docker exec stattron_master flask commands create_db

slave_db:
	sudo docker exec stattron_slave flask commands create_db

slave_userbot:
	sudo docker exec stattron_slave python userBot/userAgent.py

#---------------- Docker-Compose Slave --------------------------------
docker_master_build:
	sudo docker-compose -f docker-compose.slave.dev.yml build

docker_master_up:
	sudo docker-compose -f docker-compose.slave.dev.yml up

docker_master_upd:
	sudo docker-compose -f docker-compose.slave.dev.yml up -d

#---------------- Docker-Compose Master -------------------------------
docker_master_build:
	sudo docker-compose -f docker-compose.master.dev.yml build

docker_master_up:
	sudo docker-compose -f docker-compose.master.dev.yml up

docker_master_upd:
	sudo docker-compose -f docker-compose.master.dev.yml up -d

#---------------- Docker-Compose: PostgreSQL + PGAdmin4 ----------------
docker_pgdb_build:
	sudo docker-compose -f docker-compose.postgres.dev.yml build

docker_pgdb_up:
	sudo docker-compose -f docker-compose.postgres.dev.yml up

docker_pgdb_upd:
	sudo docker-compose -f docker-compose.postgres.dev.yml up -d

#---------------- Docker---------------------------------------

docker_stop:
	sudo docker stop $(sudo docker ps -a -q)

docker_rm:
	sudo docker rm $(sudo docker ps -a -q)

#---------------- Clean cache ----------------
clean:
	cd app/ && find . -name __pycache__ -type d -print0|xargs -0 rm -r --

#---------------- Git ----------------
gadd:
	git add .

gcom: # git commit -am "{com}" | com=<your comment>
	git commit -am "$(com)"

gpush_dev:
	git push origin dev

gpull:
	git pull




