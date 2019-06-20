import hashlib, binascii
from enum import Enum
import sqlite3

salt = b'saltienistic-salty-salt'
def hash_pwd(pwd):
    dk = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt, 100000)
    return binascii.hexlify(dk).decode()

def get_transactions():
    conn = sqlite3.connect('ewallet.db')

    try:

        c = conn.cursor()
        c.execute('''SELECT amount, srcW.walletID as srcWID, tgtW.walletID as tgtWID from transactions
                    INNER JOIN wallets as srcW ON srcW.id = transactions.sourceWID
                    INNER JOIN wallets as tgtW ON tgtW.id = transactions.targetWID''')
        trans = c.fetchall()

        print(' source | target | amount')
        print('--------|--------|--------')
        [print(f' {tran[1]:<7}| {tran[2]:<7}|{tran[0]:>8.2f}') for tran in trans]
        print('--------|--------|--------')
        print()
    except sqlite3.Error as e:
        print(f'Failed to get the transactions: {e.args[0]}')
    finally:
        conn.close()

def get_wallets():
    conn = sqlite3.connect('ewallet.db')

    try:
        c = conn.cursor()
        c.execute('SELECT walletID, balance FROM wallets')
        wallets = c.fetchall()
        c.execute('SELECT SUM(balance) FROM wallets')
        total = c.fetchone()

        print(' walletID | balance')
        print('----------|---------')
        [print(f' {w[0]:<9}|{w[1]:>8.2f}') for w in wallets]
        print('----------|---------')
        print(f'total     |{total[0]:>8.2f}')
        print()

    except sqlite3.Error as e:
        print(f'Failed to get the wallets: {e.args[0]}')
    finally:
        conn.close()

def add_wallet(wID, password, balance):

    try:
        balance = float(balance)
    except ValueError as error:
        return '{1}Error, {0}{2}'.format(error,
                                         colors.RED.value,
                                         colors.END.value)
    pwdHash = utils.hash_pwd(wallet['pwd'])
    conn = sqlite3.connect('ewallet.db')
    try:
        c = conn.cursor()
        c.execute("INSERT INTO wallets VALUES(NULL, ?, ?, ?)", (wID, pwdHash, balance))
        conn.commit()
        return f'{colors.GREEN.value}Success{colors.END.value}'
    except sqlite3.Error as e:
        return f'{colors.GREEN.value}Failed to add the wallet: {e.args[0]}{colors.END.value}'
    finally:
        conn.close()


class InsufficientFundsError(Exception):
    def __init__(self):
        self.message = 'Insufficient funds.'

class PasswordMismatchError(Exception):
    def __init__(self):
        self.message = 'Password mismatch.'

class ForbiddenError(Exception):
    def __init__(self, message):
        self.message = message

class TransactionError(Exception):
    def __init__(self, message):
        self.message = message

class NotFoundError(Exception):
    def __init__(self, message):
        self.expression = 'Wallet not found'
        self.message = message

class colors(Enum):
    WHITE = '\033[0m'
    GREEN = '\033[32m'
    RED = '\033[31m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    BRIGHTCYAN = '\033[96m'
    YELLOW = '\033[33m'
    MAGENTA = '\033[35m'
    BOLD = '\033[1m'
    END = '\033[0m'
