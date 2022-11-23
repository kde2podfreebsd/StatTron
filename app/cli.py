import os
import click
from flask import Blueprint

from models.Messages import Message
from models.Accounts import Account
from models.Channels import Channel

from db import conn

bp = Blueprint('commands', __name__)

@bp.cli.command("test")
@click.option('-name', default="test_exec")
def say_my_name(name):
    print("test_exec %s " % name)

@bp.cli.command("create_db")
@click.option('-name', default="Noname")
def create_db(name):
    print("creating db %s " % name)
    conn.drop_all()
    conn.create_all()
    conn.session.commit()

@bp.cli.command("bot")
@click.option('-bot', default="bot")
def bot(bot):
    print("start %s " % bot)
    os.system("python userBot/test.py")

