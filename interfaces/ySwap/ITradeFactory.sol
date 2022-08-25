// SPDX-License-Identifier: AGPL-3.0
// Feel free to change the license, but this is what we use

pragma solidity 0.6.12;
pragma experimental ABIEncoderV2;

interface ITradeFactory {
    function enable(address, address) external;

    function grantRole(bytes32 role, address account) external;

    function STRATEGY() external view returns (bytes32);
}
