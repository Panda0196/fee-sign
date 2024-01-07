# https://web3py.readthedocs.io/en/latest/web3.eth.account.html#verify-a-message-with-ecrecover-in-solidity

import os
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3, EthereumTesterProvider
from web3.middleware import construct_sign_and_send_raw_middleware

w3 = Web3(EthereumTesterProvider())

# private_key = os.environ.get("PRIVATE_KEY")
# assert private_key is not None, "You must set PRIVATE_KEY environment variable"
# assert private_key.startswith("0x"), "Private key must start with 0x hex prefix"

# account: LocalAccount = Account.from_key(private_key)
# w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))

# print(f"Your hot wallet address is {account.address}")

# Now you can use web3.eth.send_transaction(), Contract.functions.xxx.transact() functions
# with your local private key through middleware and you no longer get the error
# "ValueError: The method eth_sendTransaction does not exist/is not available



# 1. Sign a Message
from eth_account.messages import encode_defunct

msg = "I♥SF"
private_key = b"\xb2\\}\xb3\x1f\xee\xd9\x12''\xbf\t9\xdcv\x9a\x96VK-\xe4\xc4rm\x03[6\xec\xf1\xe5\xb3d"
message = encode_defunct(text=msg)
signed_message = w3.eth.account.sign_message(message, private_key=private_key)
print("\n\nSigned message:", signed_message)



# 2. Verify a Message
message = encode_defunct(text="I♥SF")
vecover_message = w3.eth.account.recover_message(message, signature=signed_message.signature)
print("\n\nRecover message:", vecover_message)



# 3. Prepare message for ecrecover in Solidity

# ecrecover in Solidity expects v as a native uint8, but r and s as left-padded bytes32
# Remix / web3.js expect r and s to be encoded to hex
# This convenience method will do the pad & hex for us:
def to_32byte_hex(val):
    return Web3.to_hex(Web3.to_bytes(val).rjust(32, b'\0'))

ec_recover_args = (msghash, v, r, s) = (
    Web3.to_hex(signed_message.messageHash),
    signed_message.v,
    to_32byte_hex(signed_message.r),
    to_32byte_hex(signed_message.s),
)
print("\n\nec_recover_args:", ec_recover_args)