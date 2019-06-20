import sqlite3
import socket
import json

import utils

HOST = "0.0.0.0"               # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
limit = 200

def transact(sourceWID, srcPwd, targetWID, amount, conn):

    result = "{0}TRANSACTION:{1} | {2:>6} | -> | {3:>6} | {4:8.2f}"\
            .format(utils.colors.BRIGHTCYAN.value,
                    utils.colors.END.value, sourceWID, targetWID, amount)

    c = conn.cursor()
    c.execute('SELECT * FROM wallets WHERE walletID=?', (sourceWID,))
    sourceWallet = c.fetchone()

    if not sourceWallet:
        raise utils.NotFoundError('Source')

    if utils.hash_pwd(srcPwd) != sourceWallet[2]:
        raise utils.PasswordMismatchError()

    c.execute('SELECT * FROM wallets WHERE walletID=?', (targetWID,))
    targetWallet = c.fetchone()

    if not targetWallet:
        raise utils.NotFoundError('Target')

    if amount > sourceWallet[3]:
        raise utils.InsufficientFundsError()

    sourceId = sourceWallet[0]
    targetId = targetWallet[0]

    newSourceWalletAmt = sourceWallet[3] - amount
    newTargetWalletAmt = targetWallet[3] + amount

    # Raises in case the final balance exceeds the limit.
    try:
        c.execute('UPDATE wallets SET balance = ? WHERE id = ?',
        (newSourceWalletAmt, sourceId,))
        c.execute('UPDATE wallets SET balance = ? WHERE id = ?',
        (newTargetWalletAmt, targetId,))
        c.execute('INSERT INTO transactions VALUES(NULL, ?,?,?)',
        (sourceId, targetId, amount,))
        conn.commit()
    except sqlite3.Error as e:
        raise utils.TransactionError(e.args[0])


def run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))

        s.listen(1)

        while True:

            socket_conn, addr = s.accept()

            with socket_conn:
                data = socket_conn.recv(1024).decode()
                if not data: break
                data = json.loads(data)
                result = "{0}TRANSACTION:{1} | {2:>6} | -> | {3:>6} | {4:8.2f}"\
                        .format(utils.colors.BRIGHTCYAN.value,
                                utils.colors.END.value,
                                data['sourceWID'], data['targetWID'],
                                data['amount'])

                sql_conn  = sqlite3.connect('ewallet.db')

                try:
                    transact(**data, conn=sql_conn)
                    result += ': {}Success.{}'.format(utils.colors.GREEN.value,
                                                      utils.colors.END.value)
                except (utils.InsufficientFundsError,
                        utils.ForbiddenError,
                        utils.PasswordMismatchError,
                        utils.TransactionError,
                        utils.NotFoundError) as error:

                    result += ": {1}{0}{2}".format(error.message,
                                                   utils.colors.RED.value,
                                                   utils.colors.END.value)
                finally:
                    sql_conn.close()

                print(result)

                socket_conn.sendall("{}".format(result).encode())

if __name__ == '__main__':
    run()
