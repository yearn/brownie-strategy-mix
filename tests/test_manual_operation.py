from utils import actions
from utils import utils

# TODO: check that all manual operation works as expected
# manual operation: those functions that are called by management to affect strategy's position
# e.g. repay debt manually
# e.g. emergency unstake
def test_manual_function1(
    chain, token, vault, strategy, amount, gov, user, management, RELATIVE_APPROX
):
    # set up steady state
    actions.first_deposit_and_harvest(
        vault, strategy, token, user, gov, amount, RELATIVE_APPROX
    )

    # use manual function
    # strategy.manual_function(arg1, arg2, {"from": management})

    # shut down strategy and check accounting
    strategy.updateStrategyDebtRatio(strategy, 0, {"from": gov})
    strategy.harvest({"from": gov})
    utils.sleep()
    return
