import pytest
from brownie import config
from brownie import Contract


@pytest.fixture
def gov(accounts):
    yield accounts.at("0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52", force=True)


@pytest.fixture
def user(accounts):
    yield accounts[0]


@pytest.fixture
def rewards(accounts):
    yield accounts[1]


@pytest.fixture
def guardian(accounts):
    yield accounts[2]


@pytest.fixture
def management(accounts):
    yield accounts[3]


@pytest.fixture
def strategist(accounts):
    yield accounts[4]


@pytest.fixture
def keeper(accounts):
    yield accounts[5]


@pytest.fixture
def token():
    token_address = "0xdAC17F958D2ee523a2206206994597C13D831ec7"  # USDT
    # token_address = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # USDC
    yield Contract(token_address)


@pytest.fixture
def token_whale(accounts):
    yield accounts.at(
        "0x5754284f345afc66a98fbb0a0afe71e0f007b949", force=True
    )  # Reserve = Tether: Treasury
    # yield accounts.at("0x55fe002aeff02f77364de339a1292923a15844b8", force=True) #Reserve = Circle


@pytest.fixture
def amount(accounts, token, user, token_whale):
    amount = 10_000 * 10 ** token.decimals()
    # In order to get some funds for the token you are about to use,
    # it impersonate an exchange address to use it's funds.
    reserve = token_whale
    token.transfer(user, amount, {"from": reserve})
    yield amount


@pytest.fixture
def cToken():
    token_address = "0xf650C3d88D12dB855b8bf7D11Be6C55A4e07dCC9"  # cUSDT
    # token_address = "0x39AA39c021dfbaE8faC545936693aC917d5E7563" # cUSDC
    yield Contract(token_address)


@pytest.fixture
def trade_factory():
    yield Contract("0x99d8679bE15011dEAD893EB4F5df474a4e6a8b29")


@pytest.fixture
def ymechs_safe():
    yield Contract("0x2C01B4AD51a67E2d8F02208F54dF9aC4c0B778B6")


@pytest.fixture
def comp_token():
    token_address = "0xc00e94Cb662C3520282E6f5717214004A7f26888"
    yield Contract(token_address)


@pytest.fixture
def comp_whale(accounts):
    yield accounts.at(
        "0x5608169973d639649196a84ee4085a708bcbf397", force=True
    )  # Compound: Team 3


@pytest.fixture
def weth():
    token_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    yield Contract(token_address)


@pytest.fixture
def weth_amount(user, weth):
    weth_amount = 10 ** weth.decimals()
    user.transfer(weth, weth_amount)
    yield weth_amount


@pytest.fixture
def vault(pm, gov, rewards, guardian, management, token):
    Vault = pm(config["dependencies"][0]).Vault
    vault = guardian.deploy(Vault)
    vault.initialize(token, gov, rewards, "", "", guardian, management)
    vault.setDepositLimit(2**256 - 1, {"from": gov})
    vault.setManagement(management, {"from": gov})
    yield vault


@pytest.fixture
def strategy(
    strategist, keeper, vault, cToken, Strategy, gov, trade_factory, ymechs_safe
):
    strategy = strategist.deploy(Strategy, vault, cToken, "StrategyMorphoUSDT")
    strategy.setKeeper(keeper)
    vault.addStrategy(strategy, 10_000, 0, 2**256 - 1, 1_000, {"from": gov})
    trade_factory.grantRole(
        trade_factory.STRATEGY(),
        strategy.address,
        {"from": ymechs_safe, "gas_price": "0 gwei"},
    )
    strategy.setTradeFactory(trade_factory.address, {"from": gov})
    yield strategy


@pytest.fixture
def uni_address():
    yield "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"


@pytest.fixture
def sushi_address():
    yield "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"


@pytest.fixture(scope="session")
def RELATIVE_APPROX():
    yield 1e-5


# Function scoped isolation fixture to enable xdist.
# Snapshots the chain before each test and reverts after test completion.
@pytest.fixture(scope="function", autouse=True)
def shared_setup(fn_isolation):
    pass
