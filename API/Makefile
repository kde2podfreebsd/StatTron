#---------------- Requirements ----------------
freeze:
	pip freeze > requirements.txt

deps:
	pip install -r requirements.txt

#---------------- API ----------------
runapi:
	uvicorn api:app --reload

#---------------- Database ----------------
dropdb:
	rm api.db

#---------------- Clean cache ----------------
clean:
	rm -rf __pycache__

#---------------- Git ----------------
gadd:
	git add .

gcom: # git commit -am "{com}" | com=<your comment>
	git commit -am "$(com)"

gpush_dev:
	git push origin dev

gpull:
	git pull




