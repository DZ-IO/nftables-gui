
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy(session_options={"autoflush": False})

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
    
    def print(self):
        print(self.id)
        print(self.username)
        print(self.email)
        print(self.role)
        print(self.is_active)
        print(self.password)
    
    def check_password(self, password):
        return self.password == password

class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    family = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    chains = db.relationship('Chain', backref='table', lazy=True, cascade="all, delete-orphan")
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Table %r>' % self.name
    
class Chain(db.Model):
    __tablename__ = 'chain'
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('table.name'), nullable=False)
    family = db.Column(db.String(120), nullable=True)
    policy = db.Column(db.String(120), nullable=True)
    rules = db.relationship('Rule', backref='chain', lazy=True, cascade="all, delete-orphan")
    description = db.Column(db.String(120), nullable=True)

    def get_table(self):
        return Table.query.filter_by(name=self.table_id, family=self.family).first()


    def __repr__(self):
        return '<Chain %r>' % self.name

class UserChain(Chain):


    def __repr__(self):
        return '<UserChain %r>' % self.name

class BaseChain(Chain):
    type = db.Column(db.String(120), nullable=True)
    hook_type = db.Column(db.String(120), nullable=True)
    priority = db.Column(db.Integer, nullable=True)


    def __repr__(self):
        return '<BaseChain %r>' % self.name
class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chain_id = db.Column(db.Integer, db.ForeignKey('chain.name'), nullable=False)
    family = db.Column(db.String(120), nullable=False)
    expr = db.Column(db.String(120), nullable=False)
    handle = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    statement = db.relationship('Statement', backref='rule', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return '<Rule %r>' % self.handle
    
    def table(self):
        chain = Chain.query.filter_by(name=self.chain_id, family=self.family).first()
        return chain.get_table()
    
class Statement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rule_id = db.Column(db.Integer, db.ForeignKey('rule.id'), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    src_ip = db.Column(db.String(120), nullable=True)
    dst_ip = db.Column(db.String(120), nullable=True)
    src_port = db.Column(db.String(120), nullable=True)
    dst_port = db.Column(db.String(120), nullable=True)
    protocol = db.Column(db.String(120), nullable=True)
    
    def __repr__(self):
        return '<Statement %r>' % self.id

class TerminalStatement(Statement):
    reject = db.Column(db.String(120), nullable=True)
    drop = db.Column(db.String(120), nullable=True)
    accept = db.Column(db.String(120), nullable=True)
    queue = db.Column(db.String(120), nullable=True)
    return_ = db.Column(db.String(120), nullable=True)
    jump = db.Column(db.String(120), nullable=True)
    go_to = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return '<TerminalStatement %r>' % self.id

class NotTerminalStatement(Statement):
    limit = db.Column(db.String(120), nullable=True)
    log = db.Column(db.String(120), nullable=True)
    counter = db.Column(db.String(120), nullable=True)
    nflog = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return '<NotTerminalStatement %r>' % self.id

    
class Set(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    family = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    entries = db.relationship('Entry', backref='set', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return '<Set %r>' % self.name
    
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    set_id = db.Column(db.Integer, db.ForeignKey('set.id'), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    
    def __repr__(self):
        return '<Entry %r>' % self.key

class Map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    family = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    entries = db.relationship('MapEntry', backref='map', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return '<Map %r>' % self.name

class MapEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    map_id = db.Column(db.Integer, db.ForeignKey('map.id'), nullable=False)
    key = db.Column(db.String(120), nullable=False)
    value = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    
    def __repr__(self):
        return '<MapEntry %r>' % self.key