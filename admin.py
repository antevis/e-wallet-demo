import utils

options = {
    'a': 'add wallet',
    't': 'show transactions',
    'w': 'show wallets',
    'q': 'quit'}

print('Admin dashboard')
print()

while True:
    for k,v in options.items():
        print(f'{k}: {v}')
    action = input('> ')
    if action == 'q':
        break
    elif action == 't':
        utils.get_transactions()
    elif action == 'w':
        utils.get_wallets()
    elif action == 'a':
        wID = input('> walletID: ')
        password = input('> password: ')
        balance =  input('> balance : ')

        result = utils.add_wallet(wID, password, balance)
        print(result)
        print()
