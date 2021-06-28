import pytest
from utils import actions


def test_revoke_strategy_from_vault(
    chain, token, vault, strategy, amount, user, gov, RELATIVE_APPROX
):
    # Deposit to the vault and harvest
    token.approve(vault.address, amount, {"from": user})
    vault.deposit(amount, {"from": user})
    chain.sleep(1)
    strategy.harvest({'from': gov})
    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount

    # In order to pass this tests, you will need to implement prepareReturn.
    # TODO: uncomment the following lines.
    # vault.revokeStrategy(strategy.address, {"from": gov})
    # chain.sleep(1)
    # strategy.harvest({'from': gov})
    # assert pytest.approx(token.balanceOf(vault.address), rel=RELATIVE_APPROX) == amount


def test_revoke_strategy_from_strategy(
    chain, token, vault, strategy, amount, gov, user, RELATIVE_APPROX
):
    # Deposit to the vault and harvest
    token.approve(vault.address, amount, {"from": user})
    vault.deposit(amount, {"from": user})
    chain.sleep(1)
    strategy.harvest({'from': gov})
    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount

    strategy.setEmergencyExit()
    chain.sleep(1)
    strategy.harvest({'from': gov})
    assert pytest.approx(token.balanceOf(vault.address), rel=RELATIVE_APPROX) == amount


def test_revoke_with_profit(
    chain, token, vault, strategy, amount, user, gov, RELATIVE_APPROX
):
    token.approve(vault.address, amount, {"from": user})
    vault.deposit(amount, {"from": user})
    chain.sleep(1)
    strategy.harvest({"from": gov})
    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount

    # TODO: customize generate_profit function
    profit_amount = amount * 0.05 # generating a 5% profit
    actions.generate_profit(profit_amount)

    # Revoke strategy
    # In order to pass this tests, you will need to implement prepareReturn.
    # TODO: uncomment the following lines.
    # vault.revokeStrategy(strategy.address, {"from": gov})
    # chain.sleep(1)
    # strategy.harvest({"from": gov})
    # assert pytest.approx(token.balanceOf(vault.address), rel=RELATIVE_APPROX) == amount
