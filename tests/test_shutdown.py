# TODO: Add tests that show proper operation of this strategy through "emergencyExit"
#       Make sure to demonstrate the "worst case losses" as well as the time it takes

import brownie
import pytest

AddressZero = "0x0000000000000000000000000000000000000000"

def test_emergency_permissions_deny(strategy, strategist, gov, guardian, management, accounts):
  with brownie.reverts("!authorized"):
    strategy.setEmergencyExit({"from": accounts[9]})

def test_emergency_permissions_strategist(strategy, strategist, gov, guardian, management, accounts):
    strategy.setEmergencyExit({"from": strategist})
    assert strategy.emergencyExit() == True

def test_emergency_permissions_gov(strategy, strategist, gov, guardian, management, accounts):
    strategy.setEmergencyExit({"from": gov})
    assert strategy.emergencyExit() == True

def test_emergency_permissions_guardian(strategy, strategist, gov, guardian, management, accounts):
    strategy.setEmergencyExit({"from": guardian})
    assert strategy.emergencyExit() == True

def test_emergency_permissions_management(strategy, strategist, gov, guardian, management, accounts):
    strategy.setEmergencyExit({"from": management})
    assert strategy.emergencyExit() == True


def test_vault_shutdown_can_withdraw(
  chain, token, vault, strategy, user, amount, RELATIVE_APPROX
):
  ## Deposit in Vault
  token.approve(vault.address, amount, {"from": user})
  vault.deposit(amount, {"from": user})
  assert token.balanceOf(vault.address) == amount

  if(token.balanceOf(user) > 0):
      token.transfer(AddressZero, token.balanceOf(user), {"from": user})

  # Harvest 1: Send funds through the strategy
  strategy.harvest()
  chain.mine(100)
  assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount

  ## Set Emergency
  vault.setEmergencyShutdown(True)

  ## Withdraw (does it work, do you get what you expect)
  vault.withdraw({"from": user})

  assert pytest.approx(token.balanceOf(user), rel=RELATIVE_APPROX) == amount


def test_basic_shutdown(
    chain, token, vault, strategy, user, strategist, amount, RELATIVE_APPROX
):
    # Deposit to the vault
    token.approve(vault.address, amount, {"from": user})
    vault.deposit(amount, {"from": user})
    assert token.balanceOf(vault.address) == amount

    # Harvest 1: Send funds through the strategy
    strategy.harvest()
    chain.mine(100)
    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount

    ## Earn interest
    chain.sleep(3600 * 24 * 1) ## Sleep 1 day
    chain.mine(1)
    

    # Harvest 2: Realize profit
    strategy.harvest()
    chain.sleep(3600 * 6)  # 6 hrs needed for profits to unlock
    chain.mine(1)

    ## Set emergency
    strategy.setEmergencyExit({"from": strategist})

    strategy.harvest() ## Remove funds from strategy

    assert token.balanceOf(strategy) == 0
    assert token.balanceOf(vault) >= amount ## The vault has all funds 
    ## NOTE: May want to tweak this based on potential loss during migration