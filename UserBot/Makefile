#---------------- Requirements ----------------
.PHONY freeze:
	pip freeze > requirements.txt

.PHONY deps:
	pip install -r requirements.txt

#---------------- UserBot ----------------

.PHONY bot:
	python TGUserAgent/UserBot.py

.PHONY init_session:
	python TGUserAgent/initSession.py $(s)

#---------------- Clean cache ----------------
.PHONY clean:
	rm -rf __pycache__ && rm -rf TGUserAgent/__pycache__

#---------------- Git ----------------
.PHONY gadd:
	git add .

.PHONY gcom: # git commit -am "{com}" | com=<your comment>
	git commit -am "$(com)"

.PHONY gpush_dev:
	git push origin dev

.PHONY gpull:
	git pull




