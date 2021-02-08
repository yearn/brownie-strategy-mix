def test_revoke_strategy_from_vault(token, vault, strategy, amount, gov):
    # Deposit to the vault and harvest
    token.approve(vault.address, amount, {"from": gov})
    vault.deposit(amount, {"from": gov})
    strategy.harvest()
    assert token.balanceOf(strategy.address) == amount

    # In order to pass this tests, you will need to implement prepareReturn.
    # TODO: uncomment the following lines.
    # vault.revokeStrategy(strategy.address, {"from": gov})
    # strategy.harvest()
    # assert token.balanceOf(vault.address) == amount


def test_revoke_strategy_from_strategy(token, vault, strategy, amount, gov):
    # Deposit to the vault and harvest
    token.approve(vault.address, amount, {"from": gov})
    vault.deposit(amount, {"from": gov})
    strategy.harvest()
    assert token.balanceOf(strategy.address) == amount

    strategy.setEmergencyExit()
    strategy.harvest()
    assert token.balanceOf(vault.address) == amount
