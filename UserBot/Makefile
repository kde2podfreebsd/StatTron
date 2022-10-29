#---------------- Requirements ----------------
freeze:
	pip freeze > requirements.txt

deps:
	pip install -r requirements.txt

#---------------- UserBot ----------------

bot:
	python TGUserAgent/UserBot.py

init_session:
	python TGUserAgent/initSession.py $(s)

#---------------- API ----------------
runapi:
	uvicorn API.api:app --reload

#---------------- Database ----------------
dropdb:
	rm api/sql_app.db

#---------------- Clean cache ----------------
clean:
	rm -rf __pycache__ && rm -rf api/__pycache__


#---------------- Git ----------------
gadd:
	git add .

gcom: # git commit -am "{com}" | com=<your comment>
	git commit -am "$(com)"

gpush_dev:
	git push origin dev

gpull:
	git pull




