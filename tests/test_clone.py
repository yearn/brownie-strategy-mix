# TODO: Uncomment if your strategy is clonable

# from utils import actions

# def test_clone(
#     vault, strategy, token, amount, gov, user, RELATIVE_APPROX
# ):
#     # send strategy to steady state
#     actions.first_deposit_and_harvest(vault, strategy, token, user, gov, amount, RELATIVE_APPROX)

#     # TODO: add clone logic
#     cloned_strategy = strategy.clone(vault, {'from': gov})

#     # free funds from old strategy
#     vault.revokeStrategy(strategy, {'from': gov})
#     strategy.harvest({'from': gov})
#     assert strategy.estimatedTotalAssets() == 0

#     # take funds to new strategy
#     cloned_strategy.harvest({'from': gov})
#     assert cloned_strategy.estimatedTotalAssets() > 0
