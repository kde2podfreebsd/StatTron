import os
from flask import jsonify, current_app, request
from flask import Blueprint
from sqlalchemy import func
import asyncio

from utils.util import representation_channel

from models.Accounts import Account
from models.Channels import Channel
from userBot.userAgent import UserBot

bp = Blueprint('channel_router', __name__)
loop = asyncio.get_event_loop()

@bp.route("/channel", methods=['GET'])
def get_channels():
    if request.method == 'GET':
        channels = Channel.query.filter(Channel.channel_id is not None).all()
        return jsonify(list(map(lambda x: representation_channel(x), channels)))

@bp.route("/channel/<channel_id>", methods=['GET'])
def get_channel(channel_id):
    if request.method == 'GET':
        channel = Channel.query.filter_by(channel_id=channel_id).first()
        output = representation_channel(channel) if channel is not None else jsonify('Channel does not exist')
        return jsonify(output)

@bp.route("/channel/<username>", methods=['GET'])
def get_account_channels(username):
    if request.method == 'GET':
        account = Account.query.filter_by(username=username).first()
        return jsonify(list(map(lambda x: representation_channel(x), account.channels)))

#TODO: сделать методы join_channel и left_channel
# @bp.route("/join_channel/<username>", methods=['POST'])
# def join_channel(username):
#     if request.method == 'POST':
#         account = Account.query.filter_by(username=username).first()
#         ubot = UserBot(username="donqhomo", debug=False)
#         print(ubot)
#         loop.run_until_complete(ubot.join_chat(chat_id='rozetked', category="IT"))
#         return 'True'






