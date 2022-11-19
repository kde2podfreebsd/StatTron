import os
from flask import Flask

app = Flask(__name__)
HELLO_MESSAGE="Server#1"
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://root:root@172.21.0.3:5432/stattron_db") # в Docker пробрасывается URI на postgresql
SQLALCHEMY_TRACK_MODIFICATIONS = False

