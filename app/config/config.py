import os
from flask import Flask

app = Flask(__name__)
HELLO_MESSAGE="Server#1"
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///data.db") # в Docker пробрасывается URI на postgresql
SQLALCHEMY_TRACK_MODIFICATIONS = False
