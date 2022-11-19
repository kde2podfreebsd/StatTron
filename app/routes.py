import os
from flask import jsonify, current_app
from flask import Blueprint
from sqlalchemy import func

from models.Names import Names
from models.Messages import Message
from models.Accounts import Account, create_account
from models.Channels import Channel

bp = Blueprint('routes', __name__)

@bp.route("/")
def index():
    return "True"
    # return  jsonify([
    #     {"response": current_app.config['HELLO_MESSAGE']},
    #     {"db_path": current_app.config['SQLALCHEMY_DATABASE_URI']}
    # ])

@bp.route("/name")
def name():
    n = Names.query.order_by(func.random()).first()
    return jsonify({"names" : "%s = %d" % (n.name, n.amount) })

# http://<ip:port>/add_random
@bp.route("/add_random")
def add_random():
    n = Names()
    n.fill_random()
    n.save()
    return jsonify({"added" : "%s = %d" % (n.name, n.amount)})

@bp.route("/add_account")
def add_account():
    register_account = create_account(
        api_id=123,
        api_hash="hash123",
        phone="89162107493",
        username="donqhomo",
        host="149.154.167.50",
        port=443,
        public_key="-----BEGIN RSA PUBLIC KEY-----MII <...> AB-----END RSA PUBLIC KEY-----"
    )
    print(register_account)
    return "True"