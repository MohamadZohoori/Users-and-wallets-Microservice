from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'one.db')
app.config['SQLALCHEMY_BINDS'] = {'two' : 'sqlite:///' + os.path.join(basedir, 'two.db')}
                                  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False     


# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)
###############################################################
# Wallets Class/Model
class Wallets(db.Model):
  __bind_key__ = 'two'
  id = db.Column(db.Integer, primary_key=True)
  address = db.Column(db.String(800), unique=True,nullable = False)
  owner = db.Column(db.String(100), unique=True,nullable = False)
  bal = db.Column(db.Integer)

  def __init__(self, address,owner,bal):
    self.address = address
    self.owner = owner
    self.bal = bal

# User Schema
class WalletSchema(ma.Schema):
  class Meta:
    __bind_key__ = 'two'
    fields = ('id', 'address','owner','bal')

# Init schema
wallet_schema = WalletSchema()
wallets_schema = WalletSchema(many=True)

# Create a Wallet
@app.route('/wallet', methods=['POST'])
def add_wallet():
  __bind_key__ = 'two'  

  all_users = Users.query.all()
  
  for i in range(len(all_users)):
    u = Users.query.get(i+1) 
    new_wallet = Wallets(u.walletAddress,u.name,u.bal)
    db.session.add(new_wallet)
    db.session.commit()

  return wallet_schema.jsonify(new_wallet)


# Get All Wallets
@app.route('/wallet', methods=['GET'])
def get_wallets():
 
  all_wallets = Wallets.query.all()
  result = wallets_schema.dump(all_wallets)
  return jsonify(result)

# Get Single Wallet
@app.route('/wallet/<id>', methods=['GET'])
def get_wallet(id):

  wallet = Wallets.query.get(id)
  return wallet_schema.jsonify(wallet)

# Update a Wallets
@app.route('/wallet', methods=['PUT'])
def update_wallet():
  
  wallet = Wallets.query.all()
  all_users = Users.query.all()

  diff = len(all_users) - len(wallet) 

  for i in range(diff):
    u = Users.query.get(len(wallet)+i+1) 
    new_wallet = Wallets(u.walletAddress,u.name,u.bal)
    db.session.add(new_wallet)
    db.session.commit()

  return wallet_schema.jsonify(new_wallet)

# Delete Wallet
@app.route('/wallet/<id>', methods=['DELETE'])
def delete_wallet(id):
  wallet = Wallets.query.get(id)
  db.session.delete(wallet)
  db.session.commit()

  return wallet_schema.jsonify(wallet)
###############################################################
# Users Class/Model
class Users(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True, nullable = False)
  email = db.Column(db.String(800), unique=True, nullable = False)
  walletAddress = db.Column(db.String(800), unique=True, nullable = False)
  bal = db.Column(db.Integer)


  def __init__(self, name, email, walletAddress,bal):
    self.name = name
    self.email = email
    self.walletAddress = walletAddress
    self.bal = bal

# User Schema
class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'email', 'walletAddress','bal')

# Init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Create a User
@app.route('/user', methods=['POST'])
def add_user():
  name = request.json['name']
  email = request.json['email']
  walletAddress = request.json['walletAddress']
  bal = request.json['bal']


  new_user = Users(name, email, walletAddress,bal)
  db.session.add(new_user)
  db.session.commit()
  return user_schema.jsonify(new_user)
  
  @app.route('/wallet', methods=['POST'])
  def add_wallet():
    __bind_key__ = 'two'  

    new_wallet = Wallets(walletAddress,name,bal)
    db.session.add(new_wallet)
    db.session.commit()
    return wallet_schema.jsonify(new_wallet)
 
   
#from models import db
#db.create_all()
#db.create_all(bind='two')

# Get All Users
@app.route('/user', methods=['GET'])
def get_users():
  all_users = Users.query.all()
  result = users_schema.dump(all_users)
  return jsonify(result)

# Get Single User
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
  user = Users.query.get(id)
  #u = Users.query.get(id)
  #print(u.name)
  return user_schema.jsonify(user)

# Update a User
@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
  user = Users.query.get(id)

  name = request.json['name']
  email = request.json['email']
  walletAddress = request.json['walletAddress']
  bal = request.json['bal'] 

  user.name = name
  user.email = email
  user.walletAddress = walletAddress
  user.bal = bal

  db.session.commit()

  return user_schema.jsonify(user)

# Delete User
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
  user = Users.query.get(id)
  db.session.delete(user)
  db.session.commit()

  return user_schema.jsonify(user)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)