# -*- coding:utf8 -*-
__author__ = 'Sky'

from . import db, login_manager
from datetime import datetime

class Role(db.Model):
    __tablename__ = 'rolse'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    permission = db.Column(db.Integer)
    # users = db.relationsship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role_id = db.Column(db.Integer)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    introduction = db.Column(db.String(500))
    last_seen = db.Column(db.DateTime(), default=datetime.now)
    register_time = db.Column(db.DateTime(), default=datetime.now)
    avatar_url = db.Column(db.String(128))

    def __repr__(self):
        return '<User %r>' % self.username

