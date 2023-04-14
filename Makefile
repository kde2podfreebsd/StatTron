up:
	docker compose -f docker-compose-local.yaml up -d

down:
	docker compose -f docker-compose-local.yaml down && docker network prune --force

clean:
	find . -name __pycache__ -type d -print0|xargs -0 rm -r -- && rm -rf .idea/

test:
	pytest app/TaLib/Test/MomentumIndicatorsTest.py

alembic_init:
	alembic init migrations

alembic_rev:
	alembic revision --autogenerate -m 'init'

alembic_upgrade:
	alembic upgrade heads

master_up:
	uvicorn MasterNode.main:app --workers 4 --host 0.0.0.0 --port 9876

pre_commit:
	pre-commit run --all-files
