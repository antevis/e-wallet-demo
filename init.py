import sqlite3
import utils

wallet_spec = [
    {'w_id': 'w1', 'pwd': 'pwd1', 'balance': 100.0},
    {'w_id': 'w2', 'pwd': 'pwd2', 'balance': 180.0},
    {'w_id': 'w3', 'pwd': 'pwd3', 'balance': 25.0},
    {'w_id': 'w4', 'pwd': 'pwd4', 'balance': 190.0},
]

limit = 200
walletTableSql = f'''CREATE TABLE wallets(id INTEGER PRIMARY KEY AUTOINCREMENT,
                    walletID TEXT UNIQUE, passwordHash TEXT, balance REAL
                    CHECK(balance >= 0 and balance <={limit}))'''


conn  = sqlite3.connect('ewallet.db')
c = conn.cursor()
c.execute(walletTableSql)

c.execute('''
    CREATE TABLE transactions(id INTEGER PRIMARY KEY AUTOINCREMENT,
    sourceWID INTEGER, targetWID INTEGER, amount REAL,
    FOREIGN KEY(sourceWID) REFERENCES wallets(id),
    FOREIGN KEY(targetWID) REFERENCES wallets(id))''')


for wallet in wallet_spec:
    pwdHash = utils.hash_pwd(wallet['pwd'])
    wallet_data = (wallet['w_id'], pwdHash, wallet['balance'])
    c.execute("INSERT INTO wallets VALUES(NULL, ?, ?, ?)", wallet_data)

conn.commit()
conn.close()
