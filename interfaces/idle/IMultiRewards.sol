// SPDX-License-Identifier: AGPL-3.0
pragma solidity 0.6.12;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/// @notice https://github.com/Idle-Finance/idle-gauges/blob/main/contracts/Multirewards.solidity
/// staking rewards is distributed through the Multirewards contract
interface IMultiRewards {
    /* ========== VIEWS ========== */

    function stakingToken() external view returns (IERC20);

    function balanceOf(address account) external view returns (uint256);

    function earned(address account, address _rewardsToken) external view returns (uint256);

    /* ========== MUTATIVE FUNCTIONS ========== */

    /// @notice stake `amount` of `stakingToken` to accrue rewards
    /// @dev NOTE:Cannot stake amount zero
    /// @param amount to stake
    function stake(uint256 amount) external;

    /// @notice unstake `amount` of `stakingToken`
    /// @dev NOTE:Cannot withdraw amount zero
    /// @param amount to unstake
    function withdraw(uint256 amount) external;

    /// @notice claim multiple rewards
    function getReward() external;

    /// @notice alias `getReward()` and `withdraw()`
    /// @dev NOTE:Cannot withdraw amount zero
    function exit() external;
}
