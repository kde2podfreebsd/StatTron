# Requirements
freeze:
	pip freeze > requirements.txt

deps:
	pip install -r requirements.txt

bot:
	python TGUserAgent/UserBot.py

runapi:
	uvicorn api.api:app --reload

initdb:
	python api/api.py
	mv sql_app.db api/

dropdb:
	rm api/sql_app.db

clean:
	rm -rf __pycache__ && rm -rf api/__pycache__


# GitHub
gadd:
	git add .

gcom: # git commit -am "{com}" | com=<your comment>
	git commit -am "$(com)"

gpush_dev:
	git push origin dev

gpull:
	git pull




