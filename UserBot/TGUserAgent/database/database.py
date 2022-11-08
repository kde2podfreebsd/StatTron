import os
import sys
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import uuid

app = Flask(__name__)
app.app_context().push()

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'userbot.sqlite')

db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name



if __name__ == "__main__":
    match sys.argv[1]:
        case 'init':
            with app.app_context():
                db.create_all()

        case 'drop':
            with app.app_context():
                db.drop_all()

        case 'rebuild':
            with app.app_context():
                db.drop_all()
                db.create_all()
        case _:
            py = Category(name='Python')
            db.session.add(py)
            db.session.commit()
            categories = Category.query.filter(Category.id != None).all()
            p = Post(title='test1', body='testtest1')
            py.posts.append(p)
            db.session.add(categories[0])
            db.session.commit()

