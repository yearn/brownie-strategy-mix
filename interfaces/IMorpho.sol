// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.6.12;
pragma experimental ABIEncoderV2;

interface IMorpho {
    function supply(
        address _poolTokenAddress,
        address _onBehalf,
        uint256 _amount,
        uint256 _maxGasForMatching
    ) external;

    function withdraw(address _poolTokenAddress, uint256 _amount) external;

    function claimRewards(
        address[] calldata _cTokenAddresses,
        bool _tradeForMorphoToken
    ) external returns (uint256 claimedAmount);
}
