import pytest
from brownie import config, Contract, interface
from util import clone


STRATEGY_CONFIGS = {
    "DAI": {
        "idleToken": {
            "address": "0x3fE7940616e5Bc47b0775a0dccf6237893353bB4"
        },
        "whale": "0x40ec5b33f54e0e8a33a975908c5ba1c14e5bbbdf",
        "token_address": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
        "amount": 10000 * 1e18,
    },
    "SUSD": {
        "idleToken": {
            "address": "0xF52CDcD458bf455aeD77751743180eC4A595Fd3F"
        },
        "whale": "0x519b70055af55a007110b4ff99b0ea33071c720a",
        "token_address": "0x57Ab1ec28D129707052df4dF418D58a2D46d5f51",  # dxDAO
        "amount": 100_000 * 1e18,
    },
    "USDC": {
        "idleToken": {
            "address": "0x5274891bEC421B39D23760c04A6755eCB444797C"
        },
        "whale": "0x55fe002aeff02f77364de339a1292923a15844b8",  # circle
        "token_address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "amount": 100_000 * 1e6,
    },
    "WBTC": {
        "idleToken": {
            "address": "0x8C81121B15197fA0eEaEE1DC75533419DcfD3151"
        },
        "whale": "0xBF72Da2Bd84c5170618Fbe5914B0ECA9638d5eb5",  # maker
        "token_address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
        "amount": 100 * 1e6,
    },
    "USDT": {
        "idleToken": {
            "address": "0xF34842d05A1c888Ca02769A633DF37177415C2f8"
        },
        "whale": "0xf977814e90da44bfa03b6295a0616a897441acec",  # binance
        "token_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "amount": 100_000 * 1e6,
    },
    "FEI": {
        "idleToken": {
            "address": "0xb2d5CB72A621493fe83C6885E4A776279be595bC"
        },
        "whale": "0xba12222222228d8ba445958a75a0704d566bf2c8",   # binance vault
        "token_address": "0x956F47F50A910163D8BF957Cf5846D573E7f87CA",
        "amount": 10_000 * 1e18,
    },
    "RAI": {
        "idleToken": {
            "address": "0x5C960a3DCC01BE8a0f49c02A8ceBCAcf5D07fABe"
        },
        "whale": "0x752f119bd4ee2342ce35e2351648d21962c7cafe",  # RAI whale
        "token_address": "0x03ab458634910AaD20eF5f1C8ee96F1D6ac54919",
        "amount": 10_000 * 1e18,
    },
    "TUSD": {
        "idleToken": {
            "address": "0xc278041fDD8249FE4c1Aad1193876857EEa3D68c"
        },
        "whale": "0xf977814e90da44bfa03b6295a0616a897441acec",  # binance
        "token_address": "0x0000000000085d4780B73119b644AE5ecd22b376",
        "amount": 10_000 * 1e18,
    }
}


@ pytest.fixture(params=list(STRATEGY_CONFIGS.keys()))
def strategy_config(request):
    yield STRATEGY_CONFIGS[request.param]

# ***** Accounts *****


@ pytest.fixture
def gov(accounts):
    yield accounts.at("0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52", force=True)


@ pytest.fixture
def user(accounts):
    yield accounts[0]


@ pytest.fixture
def rewards(accounts):
    yield accounts[1]


@ pytest.fixture
def guardian(accounts):
    yield accounts[2]


@ pytest.fixture
def management(accounts):
    yield accounts[3]


@ pytest.fixture
def strategist(accounts):
    yield accounts[4]


@ pytest.fixture
def keeper(accounts):
    yield accounts[5]


# ***** Contracts *****

@ pytest.fixture
def health_check():
    yield Contract("0xDDCea799fF1699e98EDF118e0629A974Df7DF012")


@ pytest.fixture
def trade_factory():
    # yield Contract("0xBf26Ff7C7367ee7075443c4F95dEeeE77432614d")
    yield Contract("0x99d8679bE15011dEAD893EB4F5df474a4e6a8b29")


@ pytest.fixture
def multi_rewards(MultiRewards, idleToken, gov, staking_reward):
    multi_rewards = gov.deploy(
        MultiRewards, gov, idleToken
    )
    staking_reward.mint(gov, 1e25)

    staking_reward.approve(multi_rewards, 1e25, {"from": gov})
    multi_rewards.addReward(
        staking_reward, gov,
        3600 * 24 * 180, {"from": gov}
    )
    multi_rewards.notifyRewardAmount(staking_reward, 1e25, {"from": gov})
    yield multi_rewards


@ pytest.fixture
def ymechs_safe():
    yield Contract("0x2C01B4AD51a67E2d8F02208F54dF9aC4c0B778B6")


# ***** Tokens *****


@ pytest.fixture
def token(strategy_config):
    # this should be the address of the ERC-20 used by the strategy/vault (DAI)
    yield interface.ERC20(strategy_config["token_address"])


@ pytest.fixture
def staking_reward(ERC20Mock, accounts):
    yield ERC20Mock.deploy({"from": accounts[0]})


@ pytest.fixture
def idleToken(strategy_config):
    yield Contract(strategy_config["idleToken"]['address'])


@ pytest.fixture
def comp():
    yield interface.ERC20("0xc00e94Cb662C3520282E6f5717214004A7f26888")


@ pytest.fixture
def idle():
    yield interface.ERC20("0x875773784Af8135eA0ef43b5a374AaD105c5D39e")


@ pytest.fixture
def weth():
    yield interface.ERC20("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")

# ***** Router *****


@ pytest.fixture
def sushiswap(Contract):
    yield Contract("0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F")

# ***** Token Amount *****


@ pytest.fixture
def amount(accounts, token, user, strategy_config):
    # In order to get some funds for the token you are about to use,
    # it impersonate an exchange address to use it's funds.
    reserve = accounts.at(strategy_config["whale"], force=True)
    amount = strategy_config["amount"]
    token.transfer(
        user, amount, {"from": reserve}
    )
    yield amount


@ pytest.fixture
def weth_amout(user, weth):
    weth_amout = 10 ** weth.decimals()
    user.transfer(weth, weth_amout)
    yield weth_amout


# ***** Vault *****

@ pytest.fixture
def vault(pm, gov, rewards, guardian, management, token):
    Vault = pm(config["dependencies"][0]).Vault
    vault = guardian.deploy(Vault)
    vault.initialize(token, gov, rewards, "", "", guardian, management, {"from": gov})
    vault.setDepositLimit(2 ** 256 - 1, {"from": gov})
    vault.setManagement(management, {"from": gov})
    yield vault

# ***** Strategy *****


@ pytest.fixture
def proxyFactoryInitializable(accounts, ProxyFactoryInitializable):
    yield accounts[0].deploy(ProxyFactoryInitializable)


@ pytest.fixture()
def strategy(vault, strategyFactory, trade_factory, keeper, gov, ymechs_safe, staking_reward, comp, idle):
    strategy = strategyFactory(vault, True)

    vault.setDepositLimit(2 ** 256 - 1, {"from": gov})
    vault.addStrategy(
        strategy.address, 10_000, 0,
        2 ** 256 - 1, 0, {"from": gov}
    )

    strategy.setKeeper(keeper)
    strategy.setDoHealthCheck(True, {"from": gov})

    # trade factory
    trade_factory.grantRole(
        trade_factory.STRATEGY(), strategy, {"from": ymechs_safe}
    )
    strategy.updateTradeFactory(trade_factory, {"from": gov})

    # set rewards
    staking_rewards = [staking_reward, comp]  # rewards
    strategy.setRewardTokens(staking_rewards, {"from": gov})

    # enable staking
    strategy.enableStaking({"from": gov})

    yield strategy


@ pytest.fixture()
def strategyFactory(
        strategist, proxyFactoryInitializable, idleToken, sushiswap, StrategyIdle, health_check, gov, multi_rewards, staking_reward, comp, idle
):
    def factory(vault, proxy=True):
        reward_tokens = []

        strategyLogic = StrategyIdle.deploy(
            vault,
            reward_tokens,
            idleToken,
            multi_rewards,
            sushiswap,
            health_check,
            {"from": strategist}
        )

        if proxy:
            strategyAddress = clone(
                strategyLogic, vault, proxyFactoryInitializable, strategist, idleToken, reward_tokens, sushiswap, health_check, multi_rewards
            )
        else:
            strategyAddress = strategyLogic.address

        strategy = StrategyIdle.at(strategyAddress, owner=strategist)
        return strategy
    yield factory


@ pytest.fixture(scope="session")
def RELATIVE_APPROX():
    yield 1e-5
