# Yearn Lido St. Ether Vault

A wrapper for Lido stETH which uses underlying shares instead of balances which can change outside transfers.

The contract follows Yearn Vault conventions.

Mainnet deployment: [0x15a2B3CfaFd696e1C783FE99eed168b78a3A371e](https://etherscan.io/address/0x15a2b3cfafd696e1c783fe99eed168b78a3a371e)

## Interface

The contract implements ERC20, as well as `permit`. It's all standard and not documented here.

Only the non-standard functionality is outlined below.

### `__default__()`
A shortcut to submit ether to Lido and deposit the received stETH into the Vault.

### `deposit()`, `deposit(uint256)`, `deposit(uint256,address)`
Deposit stETH tokens into the Vault

Parameters:
- `tokens` The amount of stETH tokens to deposit (default: `balanceOf(msg.sender)`)
- `recipient` The account to credit with the minted shares (default: `msg.sender`)

Returns: The amount of minted shares

### `withdraw()`, `withdraw(uint256)`, `withdraw(uint256,address)`
Withdraw stETH tokens from the Vault.

Parameters:
- `shares` The amount of shares to burn for stETH (default: `balanceOf(msg.sender)`)
- `recipient` The account to credit with stETH (default: `msg.sender`)

Returns: The amount of withdrawn stETH

### `pricePerShare()`
Get the vault share to stETH ratio.

Returns: The value of a single share
