from brownie import ZERO_ADDRESS
import brownie


def test_enable_disable_staking(
    chain, token, vault, strategy, user, management, trade_factory
):
    strategy.enableStaking({"from": management})
    assert strategy.enabledStake() is True

    strategy.disableStaking({"from": management})
    assert strategy.enabledStake() is False

    with brownie.reverts():
        strategy.enableStaking({"from": user})
    assert strategy.enabledStake() is False


def test_update_reward_tokens(
    chain, token, vault, strategy, user, management, trade_factory
):
    ldo = "0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32"
    rewards = [ldo]  # Example rewards

    with brownie.reverts():
        strategy.setRewardTokens(rewards, {"from": user})

    strategy.setRewardTokens(rewards, {"from": management})
    assert strategy.getRewardTokens() == rewards


def test_update_trade_factory(
    chain, token, vault, strategy, user, gov, management, trade_factory
):
    # initial setup
    ldo = "0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32"
    rewards = [ldo]  # Example rewards

    strategy.setRewardTokens(rewards, {"from": management})
    assert strategy.getRewardTokens() == rewards

    # check
    strategy.updateTradeFactory(ZERO_ADDRESS, {"from": gov})
    assert strategy.getRewardTokens() == rewards
    assert strategy.tradeFactory() == ZERO_ADDRESS

    with brownie.reverts():
        strategy.updateTradeFactory(trade_factory, {"from": user})
    assert strategy.tradeFactory() == ZERO_ADDRESS
