from brownie import Contract


def test_operation(accounts, token, vault, strategy, strategist):
    # First you need to get some funds for the token you are about to use,
    # in this example it impersonate an exchange address to use it's funds.
    amount = 10_000 * 10e18
    reserve = accounts.at("0xd551234ae421e3bcba99a0da6d736074f22192ff", force=True)
    token.transfer(accounts[0], amount, {"from": reserve})

    # Deposit to the vault
    token.approve(vault.address, amount, {"from": accounts[0]})
    vault.deposit(amount, {"from": accounts[0]})
    assert token.balanceOf(vault.address) == amount

    # harvest
    strategy.harvest()
    assert token.balanceOf(strategy.address) != 0

    # tend()
    strategy.tend()

    # withdrawal
    vault.withdraw({"from": accounts[0]})
    assert token.balanceOf(accounts[0]) != 0
