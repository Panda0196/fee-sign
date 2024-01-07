# https://web3py.readthedocs.io/en/latest/web3.eth.account.html#verify-a-message-with-ecrecover-in-solidity

import os
import time
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3, EthereumTesterProvider
from web3.middleware import construct_sign_and_send_raw_middleware

w3 = Web3(EthereumTesterProvider())


# Get private key
private_key = os.environ.get("PRIVATE_KEY")
if private_key is None:
    private_key = input("\nInput private key: ")
assert private_key.startswith("0x"), "\nPrivate key must start with 0x hex prefix"

account: LocalAccount = Account.from_key(private_key)
w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))
print(f"\nWallet address: {account.address}")


# Input parameters
print("\nfunction feeCheck(address token, bytes calldata signature, uint transferFee, uint bridgeFee, uint amount)\n")
token = input("address token: ")
assert token.startswith("0x"), "\nToken address must start with 0x hex prefix"
assert len(token) == 42, "\nToken address length mush be 42"
transferFee = int(input("uint transferFee: "))
bridgeFee = int(input("uint bridgeFee: "))
amount = int(input("uint amount: "))


# 1. Sign a Message
from eth_account.messages import encode_defunct
hash = Web3.solidity_keccak(["address", "uint256", "uint256", "uint256", "uint256"], [token, int(time.time()/1800), transferFee, bridgeFee, amount])
# print("\nHash message:", Web3.to_hex(hash))

# msg_hash = defunct_hash_message(hexstr=hash.hex(hash))
# signed_message = w3.eth.account.signHash(msg_hash, private_key=private_key)

msg_hash = encode_defunct(hexstr=Web3.to_hex(hash))
signed_message = w3.eth.account.sign_message(msg_hash, private_key=private_key)
print("\nSigned message:", signed_message)


# 2. Verify a Message
vecover_message = w3.eth.account.recover_message(msg_hash, signature=signed_message.signature)
print("\nMessage signer:", vecover_message)



# 3. Prepare message for ecrecover in Solidity

# ecrecover in Solidity expects v as a native uint8, but r and s as left-padded bytes32
# Remix / web3.js expect r and s to be encoded to hex
# This convenience method will do the pad & hex for us:
# def to_32byte_hex(val):
#     return Web3.to_hex(Web3.to_bytes(val).rjust(32, b'\0'))

# ec_recover_args = (msghash, v, r, s) = (
#     Web3.to_hex(signed_message.messageHash),
#     signed_message.v,
#     to_32byte_hex(signed_message.r),
#     to_32byte_hex(signed_message.s),
# )
# print("\nec_recover_args:", ec_recover_args)