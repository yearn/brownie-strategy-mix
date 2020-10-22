// SPDX-License-Identifier: GPL-3.0
// Feel free to change the license, but this is what we use

// Feel free to change this version of Solidity. We support >=0.6.0 <0.7.0;
pragma solidity 0.6.12;
pragma experimental ABIEncoderV2;

// These are the core Yearn libraries
import {BaseStrategy, StrategyParams} from "@yearnvaultsV2/contracts/BaseStrategy.sol";
import "@openzeppelinV3/contracts/token/ERC20/IERC20.sol";
import "@openzeppelinV3/contracts/math/SafeMath.sol";
import "@openzeppelinV3/contracts/utils/Address.sol";
import "@openzeppelinV3/contracts/token/ERC20/SafeERC20.sol";

// Import interfaces for many popular DeFi projects, or add your own!
//import "../interfaces/<protocol>/<Interface>.sol";

contract Strategy is BaseStrategy {
    using SafeERC20 for IERC20;
    using Address for address;
    using SafeMath for uint256;

    constructor(address _vault) public BaseStrategy(_vault) {}

    // ******** OVERRIDE THESE METHODS FROM BASE CONTRACT ************

    /*
     * Provide an accurate expected value for the return this strategy
     * would provide to the Vault if `report()` was called right now
     */
    function expectedReturn() public override view returns (uint256) {
        // TODO: Build a more accurate estimate using the value of all returns in terms of `want`
        return 0;
    }

    /*
     * Provide an accurate estimate for the total amount of assets (principle + return)
     * that this strategy is currently managing, denominated in terms of `want` tokens.
     * This total should be "realizable" e.g. the total value that could *actually* be
     * obtained from this strategy if it were to divest it's entire position based on
     * current on-chain conditions.
     *
     * NOTE: care must be taken in using this function, since it relies on external
     *       systems, which could be manipulated by the attacker to give an inflated
     *       (or reduced) value produced by this function, based on current on-chain
     *       conditions (e.g. this function is possible to influence through flashloan
     *       attacks, oracle manipulations, or other DeFi attack mechanisms).
     *
     * NOTE: It is up to governance to use this function in order to correctly order
     *       this strategy relative to its peers in order to minimize losses for the
     *       Vault based on sudden withdrawals. This value should be higher than the
     *       total debt of the strategy and higher than it's expected value to be "safe".
     */
    function estimatedTotalAssets() public override view returns (uint256) {
        // TODO: Build a more accurate estimate using the value of all positions in terms of `want`
        return want.balanceOf(address(this));
    }

    /*
     * Perform any strategy unwinding or other calls necessary to capture
     * the "free return" this strategy has generated since the last time it's
     * core position(s) were adusted. Examples include unwrapping extra rewards.
     * This call is only used during "normal operation" of a Strategy, and should
     * be optimized to minimize losses as much as possible. It is okay to report
     * "no returns", however this will affect the credit limit extended to the
     * strategy and reduce it's overall position if lower than expected returns
     * are sustained for long periods of time.
     */
    function prepareReturn() internal override {
        // TODO: Do stuff here to free up any returns back into `want`
    }

    /*
     * Perform any adjustments to the core position(s) of this strategy given
     * what change the Vault made in the "investable capital" available to the
     * strategy. Note that all "free capital" in the strategy after the report
     * was made is available for reinvestment. Also note that this number could
     * be 0, and you should handle that scenario accordingly.
     */
    function adjustPosition() internal override {
        // TODO: Do something to invest excess `want` tokens (from the Vault) into your positions
    }

    /*
     * Make as much capital as possible "free" for the Vault to take. Some slippage
     * is allowed, since when this method is called the strategist is no longer receiving
     * their performance fee. The goal is for the strategy to divest as quickly as possible
     * while not suffering exorbitant losses. This function is used during emergency exit
     * instead of `prepareReturn()`
     */
    function exitPosition() internal override {
        // TODO: Do stuff here to free up as much as possible of all positions back into `want`
    }

    /*
     * Liquidate as many assets as possible to `want`, irregardless of slippage,
     * up to `_amount`. Any excess should be re-invested here as well.
     */
    function liquidatePosition(uint256 _amount) internal override {
        // TODO: Do stuff here to free up `_amount` from all positions back into `want`
    }

    /*
     * Provide a signal to the keeper that `tend()` should be called. The keeper will provide
     * the estimated gas cost that they would pay to call `tend()`, and this function should
     * use that estimate to make a determination if calling it is "worth it" for the keeper.
     * This is not the only consideration into issuing this trigger, for example if the position
     * would be negatively affected if `tend()` is not called shortly, then this can return `true`
     * even if the keeper might be "at a loss" (keepers are always reimbursed by yEarn)
     *
     * NOTE: this call and `harvestTrigger` should never return `true` at the same time.
     * NOTE: if `tend()` is never intended to be called, it should always return `false`
     */
    function tendTrigger(uint256 gasCost) public override view returns (bool) {
        gasCost; // TODO: Do something with gas costs
        return false; // TODO: Provide a trigger when a tend should be performed (optional)
    }

    /*
     * Provide a signal to the keeper that `harvest()` should be called. The keeper will provide
     * the estimated gas cost that they would pay to call `harvest()`, and this function should
     * use that estimate to make a determination if calling it is "worth it" for the keeper.
     * This is not the only consideration into issuing this trigger, for example if the position
     * would be negatively affected if `harvest()` is not called shortly, then this can return `true`
     * even if the keeper might be "at a loss" (keepers are always reimbursed by yEarn)
     *
     * NOTE: this call and `tendTrigger` should never return `true` at the same time.
     */
    function harvestTrigger(uint256 gasCost) public override view returns (bool) {
        gasCost; // TODO: Do something with gas costs
        return false; // TODO: Provide a trigger when a harvest should be performed
    }

    /*
     * Do anything necesseary to prepare this strategy for migration, such
     * as transfering any reserve or LP tokens, CDPs, or other tokens or stores of value.
     */
    function prepareMigration(address _newStrategy) internal override {
        // TODO: Transfer any non-`want` tokens to the new strategy
        want.transfer(_newStrategy, want.balanceOf(address(this))); // (Optional)
    }

    // NOTE: Override this if you typically manage tokens inside this contract
    //       that you don't want swept away from you randomly.
    //       By default, only contains `want`
    // function protectedTokens() internal override view returns (address[] memory)
}
