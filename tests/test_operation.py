import brownie
from brownie import Contract
import pytest


def test_operation(
    accounts, token, vault, strategy, strategist, amount, RELATIVE_APPROX
):
    # Deposit to the vault
    token.approve(vault.address, amount, {"from": accounts[0]})
    vault.deposit(amount, {"from": accounts[0]})
    assert token.balanceOf(vault.address) == amount

    # harvest
    strategy.harvest({"from": strategist})
    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount

    # tend()
    strategy.tend({"from": strategist})

    # withdrawal
    vault.withdraw({"from": accounts[0]})
    assert pytest.approx(token.balanceOf(accounts[0]), rel=RELATIVE_APPROX) == amount


def test_emergency_exit(
    accounts, token, vault, strategy, strategist, amount, RELATIVE_APPROX
):
    # Deposit to the vault
    token.approve(vault.address, amount, {"from": accounts[0]})
    vault.deposit(amount, {"from": accounts[0]})
    strategy.harvest({"from": strategist})
    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount

    # set emergency and exit
    strategy.setEmergencyExit()
    strategy.harvest({"from": strategist})
    assert strategy.estimatedTotalAssets() < amount


def test_profitable_harvest(
    accounts, token, vault, strategy, strategist, amount, RELATIVE_APPROX, chain
):
    # Deposit to the vault
    token.approve(vault.address, amount, {"from": accounts[0]})
    vault.deposit(amount, {"from": accounts[0]})
    assert token.balanceOf(vault.address) == amount
    before_pps = vault.pricePerShare()

    # Harvest 1: Send funds from vault through the strategy
    strategy.harvest({"from": strategist})
    assert strategy.estimatedTotalAssets() == amount

    # TODO: Add some code before harvest #2 to simulate earning yield

    # Harvest 2: Realize profit
    strategy.harvest({"from": strategist})
    chain.sleep(3600 * 6) # Allow profits to unlock
    chain.mine(1)
    profit = token.balanceOf(vault.address) # Profits go to vault

    # TODO: Uncomment the checks below 
    # assert token.balanceOf(strategy) + profit > amount
    # assert vault.pricePerShare() > before_pps


def test_change_debt(gov, token, vault, strategy, strategist, amount, RELATIVE_APPROX):
    # Deposit to the vault and harvest
    token.approve(vault.address, amount, {"from": gov})
    vault.deposit(amount, {"from": gov})
    vault.updateStrategyDebtRatio(strategy.address, 5_000, {"from": gov})
    strategy.harvest({"from": strategist})
    half = int(amount / 2)

    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == half

    vault.updateStrategyDebtRatio(strategy.address, 10_000, {"from": gov})
    strategy.harvest({"from": strategist})
    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount

    # In order to pass this tests, you will need to implement prepareReturn.
    # TODO: uncomment the following lines.
    # vault.updateStrategyDebtRatio(strategy.address, 5_000, {"from": gov})
    # strategy.harvest()
    # assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == half


def test_sweep(gov, vault, strategy, token, amount, weth, weth_amout):
    # Strategy want token doesn't work
    token.transfer(strategy, amount, {"from": gov})
    assert token.address == strategy.want()
    assert token.balanceOf(strategy) > 0
    with brownie.reverts("!want"):
        strategy.sweep(token, {"from": gov})

    # Vault share token doesn't work
    with brownie.reverts("!shares"):
        strategy.sweep(vault.address, {"from": gov})

    # TODO: If you add protected tokens to the strategy.
    # Protected token doesn't work
    # with brownie.reverts("!protected"):
    #     strategy.sweep(strategy.protectedToken(), {"from": gov})

    weth.transfer(strategy, weth_amout, {"from": gov})
    assert weth.address != strategy.want()
    assert weth.balanceOf(gov) == 0
    strategy.sweep(weth, {"from": gov})
    assert weth.balanceOf(gov) == weth_amout


def test_triggers(gov, vault, strategy, token, amount, weth, weth_amout, strategist):
    # Deposit to the vault and harvest
    token.approve(vault.address, amount, {"from": gov})
    vault.deposit(amount, {"from": gov})
    vault.updateStrategyDebtRatio(strategy.address, 5_000, {"from": gov})
    strategy.harvest({"from": strategist})

    strategy.harvestTrigger(0)
    strategy.tendTrigger(0)
