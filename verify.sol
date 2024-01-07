// SPDX-License-Identifier: MIT

// Deployed at https://goerli.etherscan.io/address/0x6243b6eb4d56e0969f4d5e72c020f7c024b0b52b#code#L35

pragma solidity ^0.8.6;

import "hardhat/console.sol";

function ecdsaRecover(bytes32 messageHash, bytes memory signature) pure returns(address) {
    bytes32 r;
    bytes32 s;
    uint8 v;
    address ret;

    assembly {
        r := mload(add(signature, 32))
        s := mload(add(signature, 64))
        v := byte(0, mload(add(signature, 96)))
        if lt(v, 27) {v := add(v, 27)}
    }

    ret = ecrecover(messageHash, v, r, s);

    console.log("ecrecover input");
    console.logBytes32(messageHash);
    console.log(v);
    console.logBytes32(r);
    console.logBytes32(s);
    console.log("address:", ret);

    return ret;
}

/** 
 * @title test sign.py
 * @dev https://etherscan.io/address/0xc889b800ddaa43d828365a75194A9BAf21445111#code
 */
contract Verif {

    // Signature contains timestamp divided by SIGNATURE_FEE_TIMESTAMP; SIGNATURE_FEE_TIMESTAMP should be the same on relay;
    uint private constant SIGNATURE_FEE_TIMESTAMP = 1800;  // 30 min

    // Signature will be valid for `SIGNATURE_FEE_TIMESTAMP` * `signatureFeeCheckNumber` seconds after creation
    uint internal signatureFeeCheckNumber = 3;

    // encode message with received values and current timestamp;
    // check that signature is same message signed by address with RELAY_ROLE;
    // make `signatureFeeCheckNumber` attempts, each time decrementing timestampEpoch (workaround for old signature)
    function feeCheck(address token, bytes calldata signature, uint transferFee, uint bridgeFee, uint amount) public view returns(address) {
        bytes32 messageHash;
        address signer;
        uint timestampEpoch = block.timestamp / SIGNATURE_FEE_TIMESTAMP;

        for (uint i = 0; i < signatureFeeCheckNumber; i++) {
            messageHash = keccak256(abi.encodePacked(
                    "\x19Ethereum Signed Message:\n32",
                    keccak256(abi.encodePacked(token, timestampEpoch, transferFee, bridgeFee, amount))
                ));

            signer = ecdsaRecover(messageHash, signature);
            //if (hasRole(FEE_PROVIDER_ROLE, signer))
                //return;
            if (token == signer)
                return signer;
            timestampEpoch--;
        }
        revert("Signature check failed");
    }
}