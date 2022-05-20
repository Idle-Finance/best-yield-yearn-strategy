from brownie import StrategyIdle


def main():
    strategy = StrategyIdle.at("0x968B072BefFCd1A654D523290DcFE9b6F8139a4F")
    StrategyIdle.publish_source(strategy)


if __name__ == "__main__":
    main()
