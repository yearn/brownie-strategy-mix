from utils import actions
import brownie
from brownie import Contract


def test_healthcheck(user, vault, token, amount, strategy, chain, strategist, gov):
    # Deposit to the vault
    actions.user_deposit(user, vault, token, amount)

    assert strategy.doHealthCheck()
    assert strategy.healthCheck() == Contract("health.ychad.eth")

    chain.sleep(1)
    strategy.harvest({"from": strategist})

    chain.sleep(24 * 3600)
    chain.mine()

    strategy.setDoHealthCheck(True, {"from": gov})

    # TODO: generate a unacceptable loss
    loss_amount = amount * 0.05
    actions.generate_loss(loss_amount)

    # Harvest should revert because the loss in unacceptable
    with brownie.reverts("!healthcheck"):
        strategy.harvest({"from": strategist})

    # we disable the healthcheck
    strategy.setDoHealthCheck(False, {"from": gov})

    # the harvest should go through, taking the loss
    tx = strategy.harvest({"from": strategist})
    assert tx.events["Harvested"]["loss"] == loss_amount

    vault.withdraw({"from": user})
    assert token.balanceOf(user) < amount  # user took losses
