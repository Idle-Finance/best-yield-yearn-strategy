
def clone(
    strategyLogic, vault, proxyFactoryInitializable, strategist, idleToken, reward_tokens, sushiswap, health_check, multi_rewards
):
    data = strategyLogic.init.encode_input(
        vault,
        strategist,
        reward_tokens,
        idleToken,
        multi_rewards,
        sushiswap,
        health_check
    )
    tx = proxyFactoryInitializable.deployMinimal(
        strategyLogic,
        data,
        {"from": strategist})

    strategyAddress = tx.events["ProxyCreated"]["proxy"]
    return strategyAddress
