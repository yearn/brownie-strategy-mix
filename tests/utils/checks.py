import brownie
from brownie import interface
import pytest

# This file is reserved for standard checks


def check_vault_empty(vault):
    assert vault.totalAssets() == 0
    assert vault.totalSupply() == 0


def check_strategy_empty(strategy):
    assert strategy.estimatedTotalAssets() == 0
    vault = interface.VaultAPI(strategy.vault())
    assert vault.strategies(strategy).dict()["totalDebt"] == 0


def check_revoked_strategy(vault, strategy):
    print("TODO: check_revoked_strategy")
    return
