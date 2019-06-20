import unittest
import server
import utils
import sqlite3

class TestServer(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect('ewallet.db')

    def test_missing_source(self):
        source_wID = 'w6'
        pwd = 'pwd1'
        target_wID = 'w2'
        amount = 10.

        self.assertRaises(utils.NotFoundError, server.transact,
                          source_wID, pwd, target_wID, amount, self.conn)

    def test_missing_target(self):
        source_wID = 'w1'
        pwd = 'pwd1'
        target_wID = 'w6'
        amount = 10.

        self.assertRaises(utils.NotFoundError, server.transact,
                          source_wID, pwd, target_wID, amount, self.conn)

    def test_password_mismatch(self):
        source_wID = 'w1'
        pwd = 'whatever'
        target_wID = 'w2'
        amount = 10.

        self.assertRaises(utils.PasswordMismatchError, server.transact,
                          source_wID, pwd, target_wID, amount, self.conn)

    def test_insufficient_funds(self):
        source_wID = 'w1'
        pwd = 'pwd1'
        target_wID = 'w3'
        amount = 120.

        self.assertRaises(utils.InsufficientFundsError, server.transact,
                          source_wID, pwd, target_wID, amount, self.conn)

    def test_transaction_error(self):
        source_wID = 'w1'
        pwd = 'pwd1'
        target_wID = 'w4'
        amount = 20.

        self.assertRaises(utils.TransactionError, server.transact,
                          source_wID, pwd, target_wID, amount, self.conn)

if __name__ == '__main__':
    unittest.main()
