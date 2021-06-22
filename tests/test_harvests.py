from utils import actions, checks
import pytest


def test_profitable_harvest(
    chain, accounts, token, vault, strategy, user, strategist, amount, RELATIVE_APPROX
):
    # Deposit to the vault
    token.approve(vault.address, amount, {"from": user})
    vault.deposit(amount, {"from": user})
    assert token.balanceOf(vault.address) == amount

    # Harvest 1: Send funds through the strategy
    chain.sleep(1)
    strategy.harvest()
    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount

    # TODO: Add some code before harvest #2 to simulate earning yield
    profit_amount = 0
    actions.generate_profit(profit_amount)

    # Harvest 2: Realize profit
    chain.sleep(1)
    strategy.harvest()
    chain.sleep(3600 * 6)  # 6 hrs needed for profits to unlock
    chain.mine(1)
    profit = token.balanceOf(vault.address)  # Profits go to vault
    # TODO: Uncomment the lines below
    # assert token.balanceOf(strategy) + profit > amount
    # assert vault.pricePerShare() > before_pps


def test_lossy_harvest(
    chain, accounts, token, vault, strategy, user, strategist, amount, RELATIVE_APPROX
):
    # Deposit to the vault
    token.approve(vault.address, amount, {"from": user})
    vault.deposit(amount, {"from": user})
    assert token.balanceOf(vault.address) == amount

    # Harvest 1: Send funds through the strategy
    chain.sleep(1)
    strategy.harvest()
    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount

    # TODO: Add some code before harvest #2 to simulate a lower pps
    loss_amount = 0
    actions.generate_loss(loss_amount)

    # Harvest 2: Realize loss
    chain.sleep(1)
    strategy.harvest()
    chain.sleep(3600 * 6)  # 6 hrs needed for profits to unlock
    chain.mine(1)
    profit = token.balanceOf(vault.address)  # Profits go to vault
    # TODO: Manually calculate impact on totalGain / totalLoss / totalDebt and fill the numbers
    totalGain = 0
    totalLoss = 0
    totalDebt = 0
    checks.check_accounting(vault, strategy, totalGain, totalLoss, totalDebt)

    # User will withdraw accepting losses
    vault.withdraw(vault.balanceOf(user), user, 10_000, {"from": user})
    assert token.balanceOf(user) == amount + totalLoss


def test_choppy_harvest(
    chain, accounts, token, vault, strategy, user, strategist, amount, RELATIVE_APPROX
):
    # Deposit to the vault
    token.approve(vault.address, amount, {"from": user})
    vault.deposit(amount, {"from": user})
    assert token.balanceOf(vault.address) == amount

    # Harvest 1: Send funds through the strategy
    chain.sleep(1)
    strategy.harvest({"from": strategist})
    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount

    # TODO: Add some code before harvest #2 to simulate a lower pps
    loss_amount = 0
    actions.generate_loss(loss_amount)

    # Harvest 2: Realize loss
    chain.sleep(1)
    strategy.harvest({"from": strategist})

    # TODO: Manually calculate impact on totalGain / totalLoss / totalDebt and fill the numbers
    totalGain = 0
    totalLoss = 0
    totalDebt = 0
    checks.check_accounting(vault, strategy, totalGain, totalLoss, totalDebt)

    # TODO: Add some code before harvest #3 to simulate a higher pps ()
    profit_amount = 0
    actions.generate_profit(profit_amount)

    chain.sleep(1)
    strategy.harvest({"from": strategist})

    profit = token.balanceOf(vault.address)  # Profits go to vault

    # TODO: Manually calculate impact on totalGain / totalLoss / totalDebt and fill the numbers
    # take into account that losses will be accumulated
    totalGain = 0
    totalLoss = 0
    totalDebt = 0
    checks.check_accounting(vault, strategy, totalGain, totalLoss, totalDebt)

    # User will withdraw accepting losses
    vault.withdraw({"from": user})
    assert token.balanceOf(user) == amount + totalLoss - totalGain
