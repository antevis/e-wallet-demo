import argparse
import json
import socket

HOST = 'localhost'
PORT = 50007

# !!! WARNING! PASSWORD BEING SENT AS PLAIN TEXT.
# FOR DEMONSTRATION PURPOSES ONLY.
def transfer(sourceWID, srcPwd, targetWID, amount):
    tran_data = json.dumps({
        "sourceWID": sourceWID,
        "srcPwd": srcPwd,
        "targetWID": targetWID,
        "amount": amount})

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(tran_data.encode())
        data = s.recv(1024).decode()

    print(data)


def run():
    def amount_type(string):
        try:
            return float(string)
        except:
            raise argparse.ArgumentTypeError('Invalid value')

    parser = argparse.ArgumentParser(description='E-wallet transfer')
    parser.add_argument('source', help="Source wallet")
    parser.add_argument('password', help="Source wallet password")
    parser.add_argument('target', help="Target wallet")
    parser.add_argument('amount', help="Transfer amount", type=amount_type)

    args = parser.parse_args()

    transfer(args.source, args.password, args.target, args.amount)

if __name__ == "__main__":
    run()
