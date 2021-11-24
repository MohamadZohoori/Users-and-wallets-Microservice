# Users-and-wallets-Microservice
Further web3 functions such as balance and transactions will be added (tested them before) on windows10 (I had windows7 at home and couldn't use web3)

BTW, if you want to rewrite the database you can use the following in the command prompt:

from models import db
db.create_all()
db.create_all(bind='two')

or uncomment the very same script inside the models.py file. and comment it.

All the tests are done with post man.

The following codes are what I can apply to get the balance of every wallet and also check 
the transactions(once I have windows 10 available to be able to use web3):

import json
from web3 import Web3


infura_url = "https://mainnet.infura.io/v3/80ca094b614b44b3b647ceb01a2b70d0"

web3 = Web3(Web3.HTTPProvider(infura_url))

abi = [{"constant":true,"inputs":[],"name":"mintingFinished","outputs":[{"name":"","type":"bool"}],...

address = "0xd26114cd6EE289AccF82350c8d8487fedB8A0C07"

contract = web3.eth.contract(address=address, abi=abi)

balance = contract.functions.balanceOf('0xd26114cd6EE289AccF82350c8d8487fedB8A0C07').call()
print(web3.fromWei(balance, 'ether'))


