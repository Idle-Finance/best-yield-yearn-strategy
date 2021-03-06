# Best Yield Yearn Strategy

Idle Finance Best Yield Yearn-strategy

This strategy deposits tokens to Idle Finance Best Yield Strategy.

The strategy stakes tokens and accrue rewards if necessary. Those accrued rewards are sold by ySwaps which allows strategies to outsource swap functions. To set up ySwaps use`updateTradeFactory` method and set tokens to sell by calling `setRewardTokens` method.

## Idle Finance

Idle is a decentralized protocol dedicated to bringing automatic asset allocation and aggregation to the interest-bearing tokens economy. This protocol bundles stable crypto-assets (stablecoins) into tokenized baskets that are programmed to automatically rebalance based on different management logics.

[Docs - developers.idle.finance](https://docs.idle.finance/)

## Getting Started

Create .env file with the following environment variables.

```bash
ETHERSCAN_TOKEN=<Your Etherscan token>
WEB3_INFURA_PROJECT_ID=<Your Infura Project Id> # If you use infura
```

To add RPC provider:

```bash
brownie networks add Ethereum alchemy-mainnet  chainId=1 host=https://eth-mainnet.alchemyapi.io/v2/<ALCHEMY_API_KEY> explorer=https://api.etherscan.io/api muticall2=0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696
```

To set up mainnet forking :

```bash
brownie networks add development alchemy-mainnet-fork cmd=ganache-cli fork=alchemy-mainnet mnemonic=brownie port=8545 accounts=10 host=http://127.0.0.1 timeout=120
```

For specific options and more information about each command, type:
`brownie networks --help`

## Testing

To run testing on forking mainnet type:

```bash
brownie test --network alchemy-mainnet-fork
```

use `--interactive` option to launch interactive console when a test fails.

### Debugging

type:

```bash
tx.traceback()
```

To see the call trace type:

```bash
tx.call_trace()
```

To see the emitted events type:

```bash
tx.info()
```

## Deployed Contracts

Minimal proxy is used for developments

| name                     | address                                    |
| ------------------------ | ------------------------------------------ |
| IdleDAI strategy (Logic) | 0x968B072BefFCd1A654D523290DcFE9b6F8139a4F |

### ape tax

| name             | address                                    |
| ---------------- | ------------------------------------------ |
| IdleDAI strategy | 0x70c17FF2A05ddC9C5bC36dB02C4ABF8B3e9f96D0 |
