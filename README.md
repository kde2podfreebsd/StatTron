# Stattron

## [TG User Agent Bot Documentation](https://github.com/bubblesortdudoser/Stattron/blob/main/UserBot/README.md) ⬅️

## Installation & Preparation
#### 1. Clone repo
```.sh
git clone https://github.com/bubblesortdudoser/Stattron
cd Statron
```
#### 2. Create venv
```.sh
python -m venv venv
```

#### 3. Install deps
```.sh
cd UserBot/
make deps
```

#### 4. Create database
```.sh
cd TGUserAgent/database/
python dbworker.py init

python dbworker.py rebuild # rebuild db
```
-----------  


### Project architecture
```.sh
Telemetr
├── API
│   ├── api.py
│   ├── crud.py
│   ├── database.py
│   ├── Dockerfile
│   ├── __init__.py
│   ├── Makefile
│   ├── models.py
│   └── schemas.py
├── nginx-conf
│   ├── fastcgi.conf
│   ├── gunicorn.service
│   ├── gunicorn.socket
│   ├── mime.types
│   ├── nginx.conf
│   └── proxy.conf
├── README.md
└── UserBot
    ├── __init__.py
    ├── Makefile
    ├── README.md
    ├── requirements.txt
    └── TGUserAgent
        ├── database
        │   ├── Accounts.py
        │   ├── Channels.py
        │   ├── database.py
        │   ├── dbworker.py
        │   ├── __init__.py
        │   ├── Messages.py
        │   └── userbot.sqlite
        ├── downloads
        ├── __init__.py
        ├── messageHandler.py
        ├── sessions
        │   └── donqhomo.session
        └── UserBot.py

7 directories, 30 files

```


