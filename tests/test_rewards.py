import pytest


def test_rewards(
    chain, token, vault, strategy, user, amount, idleToken, multi_rewards, staking_reward, RELATIVE_APPROX, gov
):
    # Deposit to the vault
    token.approve(vault.address, amount, {"from": user})
    vault.deposit(amount, {"from": user})
    assert token.balanceOf(vault.address) == amount

    # enable staking
    strategy.enableStaking({"from": gov})

    # harvest
    price = idleToken.tokenPrice()
    chain.sleep(1)
    strategy.harvest()

    assert pytest.approx(
        strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX
    ) == amount

    days = 14
    chain.sleep(days * 24 * 60 * 60)
    chain.mine(1)

    assert staking_reward.balanceOf(strategy) == 0
    assert pytest.approx(
        multi_rewards.balanceOf(strategy), rel=RELATIVE_APPROX
    ) == amount * 1e18 / price

    # harvest
    chain.sleep(1)
    strategy.harvest()

    assert staking_reward.balanceOf(strategy) > 0
