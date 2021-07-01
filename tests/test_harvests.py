from utils import actions, checks, utils
import pytest

# tests harvesting a strategy that returns profits correctly
def test_profitable_harvest(
    chain, accounts, token, vault, strategy, user, strategist, amount, RELATIVE_APPROX
):
    # Deposit to the vault
    actions.user_deposit(user, vault, token, amount)

    # Harvest 1: Send funds through the strategy
    chain.sleep(1)
    strategy.harvest({"from": strategist})
    total_assets = strategy.estimatedTotalAssets()
    assert pytest.approx(total_assets, rel=RELATIVE_APPROX) == amount

    # TODO: Add some code before harvest #2 to simulate earning yield
    profit_amount = 0
    actions.generate_profit(profit_amount)

    # check that estimatedTotalAssets estimates correctly
    assert total_assets + profit_amount == strategy.estimatedTotalAssets()

    before_pps = vault.pricePerShare()
    # Harvest 2: Realize profit
    chain.sleep(1)
    tx = strategy.harvest({"from": strategist})
    checks.check_harvest_profit(tx, profit_amount)

    chain.sleep(3600 * 6)  # 6 hrs needed for profits to unlock
    chain.mine(1)
    profit = token.balanceOf(vault.address)  # Profits go to vault

    assert token.balanceOf(strategy) + profit > amount
    assert vault.pricePerShare() > before_pps


# tests harvesting a strategy that reports losses
def test_lossy_harvest(
    chain, accounts, token, vault, strategy, user, strategist, amount, RELATIVE_APPROX
):
    # Deposit to the vault
    actions.user_deposit(user, vault, token, amount)

    # Harvest 1: Send funds through the strategy
    chain.sleep(1)
    strategy.harvest({"from": strategist})
    total_assets = strategy.estimatedTotalAssets()
    assert pytest.approx(total_assets, rel=RELATIVE_APPROX) == amount

    # TODO: Add some code before harvest #2 to simulate a lower pps
    loss_amount = amount * 0.05
    actions.generate_loss(loss_amount)

    # check that estimatedTotalAssets estimates correctly
    assert total_assets - loss_amount == strategy.estimatedTotalAssets()

    # Harvest 2: Realize loss
    chain.sleep(1)
    tx = strategy.harvest({"from": strategist})
    checks.check_harvest_loss(tx, loss_amount)
    chain.sleep(3600 * 6)  # 6 hrs needed for profits to unlock
    chain.mine(1)

    # User will withdraw accepting losses
    vault.withdraw(vault.balanceOf(user), user, 10_000, {"from": user})
    assert token.balanceOf(user) + loss_amount == amount


# tests harvesting a strategy twice, once with loss and another with profit
# it checks that even with previous profit and losses, accounting works as expected
def test_choppy_harvest(
    chain, accounts, token, vault, strategy, user, strategist, amount, RELATIVE_APPROX
):
    # Deposit to the vault
    actions.user_deposit(user, vault, token, amount)

    # Harvest 1: Send funds through the strategy
    chain.sleep(1)
    strategy.harvest({"from": strategist})

    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount

    # TODO: Add some code before harvest #2 to simulate a lower pps
    loss_amount = amount * 0.05
    actions.generate_loss(loss_amount)

    # Harvest 2: Realize loss
    chain.sleep(1)
    tx = strategy.harvest({"from": strategist})
    checks.check_harvest_loss(tx, loss_amount)

    # TODO: Add some code before harvest #3 to simulate a higher pps ()
    profit_amount = amount * 0.1  # 10% profit
    actions.generate_profit(profit_amount)

    chain.sleep(1)
    tx = strategy.harvest({"from": strategist})
    checks.check_harvest_profit(tx, profit_amount)

    # User will withdraw accepting losses
    vault.withdraw({"from": user})

    # User will take 100% losses and 100% profits
    assert token.balanceOf(user) == amount + profit_amount - loss_amount
