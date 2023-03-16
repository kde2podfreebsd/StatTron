# Clean cache
clean:
	find . -name __pycache__ -type d -print0|xargs -0 rm -r --

# Grep IP docker container
grep_ipaddr:
	docker inspect pgdb | grep IPAddress

# freeze requirements.txt
freeze:
	pip freeze > requirements.txt

# install dependencies
deps:
	pip install -r requirements.txt

devdb_dockerup:
	docker-compose -f docker-compose-devdb.yaml up

docker_stop:
	docker stop $(sudo docker ps -a -q)

docker_rm:
	sudo docker rm $(sudo docker ps -a -q)

dbinit:
	cd app/ && flask db init

dbmigrate:
	cd app/ && flask db migrate

dbupgrade:
	cd app/ && flask db upgrade