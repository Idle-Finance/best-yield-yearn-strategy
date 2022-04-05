// SPDX-License-Identifier: AGPL-3.0
pragma solidity 0.6.12;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract ERC20Mock is ERC20("Mock", "MOCK") {
    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }

    function burn(address from, uint256 amount) external {
        _mint(from, amount);
    }
}
