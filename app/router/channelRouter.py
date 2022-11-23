import logging
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

@bp.route("/channels", methods=['GET'])
def get_channels():
    if request.method == 'GET':
        channels = Channel.query.filter(Channel.channel_id is not None).all()
        return jsonify(list(map(lambda x: representation_channel(x), channels)))

@bp.route("/channel/<channel_id>", methods=['GET', 'PATCH'])
def get_channel(channel_id):
    if request.method == 'GET':
        channel = Channel.query.filter_by(channel_id=channel_id).first()
        output = representation_channel(channel) if channel is not None else jsonify('Channel does not exist')
        return jsonify(output)

    if request.method == 'PATCH':
        channel = Channel.query.filter_by(channel_id=channel_id).first()
        channel.category = request.json['category'] if request.json.get('category') is not None else channel.category
        output = channel.update(channel=channel)
        return jsonify(output)

@bp.route("/channels/<username>", methods=['GET'])
def get_account_channels(username):
    if request.method == 'GET':
        account = Account.query.filter_by(username=username).first()
        return jsonify(list(map(lambda x: representation_channel(x), account.channels)))

#TODO: сделать методы join_channel и left_channel
@bp.route("/join_channel/<username>", methods=['POST'])
def join_channel(username):
    if request.method == 'POST':
        account = Account.query.filter_by(username=username).first()
        if account is not None:
            logging.info(account)
            if request.json.get('channel_id') is not None:
                os.system(f"python userBot/userAgent.py join {username} {request.json.get('channel_id')}")

            return 'True'
        else:
            logging.warning("Account doesnt exist")
            return 'Account doesnt exist'

@bp.route("/left_channel/<username>", methods=['POST'])
def left_channel(username):
    if request.method == 'POST':
        account = Account.query.filter_by(username=username).first()
        if account is not None:
            logging.info(account)
            if request.json.get('channel_id') is not None:
                os.system(f"python userBot/userAgent.py left {username} {request.json.get('channel_id')}")
            return 'True'
        else:
            logging.warning("Account doesnt exist")
            return 'Account doesnt exist'






