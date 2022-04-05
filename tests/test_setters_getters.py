from brownie import config
import brownie


def test_constructor(vault, gov, strategy, comp, idle, idleToken, staking_reward):
    assert strategy.name() == f"StrategyIdleV2 {idleToken.name()}"
    reward_tokens = strategy.getRewardTokens()
    assert staking_reward.address in reward_tokens
    assert comp.address in reward_tokens


def test_incorrect_vault(pm, guardian, gov, rewards, strategyFactory, ERC20Mock):
    token = guardian.deploy(ERC20Mock)
    Vault = pm(config["dependencies"][0]).Vault
    vault = guardian.deploy(Vault)
    vault.initialize(token, gov, rewards, "", "")
    with brownie.reverts("strat/want-ne-underlying"):
        strategyFactory(vault)


def test_double_init(strategy, strategist):
    with brownie.reverts("Strategy already initialized"):
        strategy.init(
            strategist,
            strategist,
            [],
            strategist,
            strategist,
            strategist,
            strategist
        )
