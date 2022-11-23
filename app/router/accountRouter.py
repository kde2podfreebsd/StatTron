import os
from flask import jsonify, current_app, request
from flask import Blueprint
from sqlalchemy import func

from utils.util import representation_account
from models.Accounts import Account

bp = Blueprint('account_router', __name__)


@bp.route("/account", methods=['POST', 'GET'])
def accounts():
    if request.method == 'POST':
        new_account = Account()
        output = new_account.create(
            api_id=request.json['api_id'],  # int
            api_hash=request.json['api_hash'],
            phone=request.json['phone'],
            username=request.json['username'],
            host=request.json['host'] if request.json.get('host') is not None else None,
            port=request.json['port'] if request.json.get('port') is not None else None,  # int
            public_key=request.json['public_key'] if request.json.get('public_key') is not None else None
        )
        return jsonify(output)

    if request.method == 'GET':
        accounts = Account.query.filter(Account.username is not None).all()
        return jsonify(list(map(lambda x: representation_account(x), accounts)))

@bp.route("/account/<username>", methods=['PATCH', 'GET', 'DELETE'])
def account(username):
    if request.method == 'GET':
        account = Account.query.filter_by(username=username).first()
        output = representation_account(account) if account is not None else jsonify('Account does not exist')
        return jsonify(output)

    if request.method == 'PATCH':
        account = Account.query.filter_by(username=username).first()
        if account is not None:
            account.api_id = request.json['api_id'] if request.json.get('api_id') is not None else account.api_id  # int
            account.api_hash = request.json['api_hash'] if request.json.get('api_hash') is not None else account.api_hash,
            account.phone = request.json['phone'] if request.json.get('phone') is not None else account.phone,
            account.username = request.json['username'] if request.json.get('username') is not None else account.username,
            account.host = request.json['host'] if request.json.get('host') is not None else account.host,
            account.port = request.json['port'] if request.json.get('port') is not None else account.port,  # int
            account.public_key = request.json['public_key'] if request.json.get('public_key') is not None else account.public_key
            output = account.update(account = account)
            return jsonify(output)
        else:
            return jsonify({"status": False, "msg": "Account doesnt found"})

    if request.method == 'DELETE':
        if Account.query.filter_by(username=username).first() is not None:
            return jsonify(Account.query.filter_by(username=username).first().delete())
        else:
            return jsonify({"status": False, "msg": "Account doesnt found"})

