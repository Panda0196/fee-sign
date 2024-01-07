// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.22;

contract Recover {
  function ecr (bytes32 msgh, uint8 v, bytes32 r, bytes32 s) public pure
  returns (address sender) {
    return ecrecover(msgh, v, r, s);
  }
}