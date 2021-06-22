# This file is reserved for standard actions like deposits


def user_deposits(user, vault, token, amount):
    if token.allowance(user, vault) < amount:
        token.approve(vault, 2 ** 256 - 1, {"from": user})
    vault.deposit(amount, {"from": user})


def simulate_profit(amount):
    # TODO: add action for simulating profit
    return
