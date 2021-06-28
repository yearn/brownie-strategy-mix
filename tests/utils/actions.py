import pytest
from brownie import chain
import utils

# This file is reserved for standard actions like deposits
def user_deposit(user, vault, token, amount):
    if token.allowance(user, vault) < amount:
        token.approve(vault, 2 ** 256 - 1, {"from": user})
    vault.deposit(amount, {"from": user})
    assert token.balanceOf(vault.address) == amount


# TODO: add args as required
def generate_profit(amount):
    # TODO: add action for simulating profit
    return


# TODO: add args as required
def generate_loss(amount):
    # TODO: add action for simulating profit
    return


def first_deposit_and_harvest(
    vault, strategy, token, user, gov, amount, RELATIVE_APPROX
):
    # Deposit to the vault and harvest
    token.approve(vault.address, amount, {"from": user})
    vault.deposit(amount, {"from": user})
    chain.sleep(1)
    strategy.harvest({"from": gov})
    utils.sleep()
    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount
