import os
from flask import jsonify, current_app, request
from flask import Blueprint
from sqlalchemy import func
import asyncio


from models.Accounts import Account
from models.Channels import Channel
from userBot.userAgent import UserBot

bp = Blueprint('channel_router', __name__)
loop = asyncio.get_event_loop()

@bp.route("/channel", methods=['GET'])
def get_channels():
    if request.method == 'GET':
        return Channel.query.filter(Channel.channel_id is not None).all()

@bp.route("/channel/<username>", methods=['GET'])
def get_account_channels(username):
    if request.method == 'GET':
        account = Account.query.filter_by(username=username).first()
        return account.channels if account is not None else 'Account not found'

#TODO: сделать методы join_channel и left_channel
# @bp.route("/join_channel/<username>", methods=['POST'])
# def join_channel(username):
#     if request.method == 'POST':
#         account = Account.query.filter_by(username=username).first()
#         ubot = UserBot(username="donqhomo", debug=False)
#         print(ubot)
#         loop.run_until_complete(ubot.join_chat(chat_id='rozetked', category="IT"))
#         return 'True'






