import brownie
from brownie import Contract, Wei
import pytest


def test_strategy_setup(
    token, comp_token, vault, strategy, trade_factory, sushi_address, uni_address
):
    uint256_max = 2**256 - 1
    assert token.allowance(strategy.address, strategy.MORPHO()) == uint256_max

    # assert that the default router is sushi
    assert strategy.currentV2Router() == sushi_address
    # assert allowance for comp to Sushi and Uni
    uint96_max = 2**96 - 1
    assert comp_token.allowance(strategy.address, sushi_address) == uint96_max
    assert comp_token.allowance(strategy.address, uni_address) == uint96_max

    assert strategy.tradeFactory() == trade_factory.address
    assert comp_token.allowance(strategy.address, trade_factory.address) == uint96_max


def test_toggle_swap_router(strategy, sushi_address, uni_address):
    assert strategy.currentV2Router() == sushi_address
    strategy.setToggleV2Router()
    assert strategy.currentV2Router() == uni_address


def test_set_min_comp_to_claim(strategy):
    assert strategy.minCompToClaimOrSell() == Wei("0.1 ether")
    new_value = Wei("11.11 ether")
    strategy.setMinCompToClaimOrSell(new_value)
    assert strategy.minCompToClaimOrSell() == new_value


def test_set_max_gas_for_matching(strategy):
    assert strategy.maxGasForMatching() == 100000
    new_value = Wei("0.05212 ether")
    strategy.setMaxGasForMatching(new_value)
    assert strategy.maxGasForMatching() == new_value


def test_disabling_trade_factory(strategy, comp_token, gov, trade_factory):
    assert strategy.tradeFactory() == trade_factory.address
    strategy.removeTradeFactoryPermissions({"from": gov})
    assert strategy.tradeFactory() == "0x0000000000000000000000000000000000000000"
    assert comp_token.allowance(strategy.address, trade_factory.address) == 0
