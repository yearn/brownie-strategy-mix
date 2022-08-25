// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.6.12;
pragma experimental ABIEncoderV2;

interface IMorpho {
    function supply(
        address _poolTokenAddress,
        address _onBehalf,
        uint256 _amount
    ) external;

    function supply(
        address _poolTokenAddress,
        address _onBehalf,
        uint256 _amount,
        uint256 _maxGasForMatching
    ) external;

    function borrow(address _poolTokenAddress, uint256 _amount) external;

    function borrow(
        address _poolTokenAddress,
        uint256 _amount,
        uint256 _maxGasForMatching
    ) external;

    function withdraw(address _poolTokenAddress, uint256 _amount) external;

    function repay(
        address _poolTokenAddress,
        address _onBehalf,
        uint256 _amount
    ) external;

    function liquidate(
        address _poolTokenBorrowedAddress,
        address _poolTokenCollateralAddress,
        address _borrower,
        uint256 _amount
    ) external;

    function claimRewards(
        address[] calldata _cTokenAddresses,
        bool _tradeForMorphoToken
    ) external returns (uint256 claimedAmount);
}
