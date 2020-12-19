# @version 0.2.8
# @notice Yearn-compatible wrapper for stETH
# @author banteg
# @license MIT
from vyper.interfaces import ERC20

implements: ERC20


interface stETH:
    def getPooledEthByShares(_sharesAmount: uint256) -> uint256: view
    def getSharesByPooledEth(_pooledEthAmount: uint256) -> uint256: view
    def submit(referral: address) -> uint256: payable


event Transfer:
    sender: indexed(address)
    receiver: indexed(address)
    value: uint256


event Approval:
    owner: indexed(address)
    spender: indexed(address)
    value: uint256


name: public(String[64])
symbol: public(String[32])
decimals: public(uint256)

balanceOf: public(HashMap[address, uint256])
allowance: public(HashMap[address, HashMap[address, uint256]])
totalSupply: public(uint256)

steth: constant(address) = 0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84


@external
def __init__():
    self.name = 'Yearn Lido St. Ether Vault'
    self.symbol = 'yvstETH'
    self.decimals = 18


@internal
def _mint(owner: address, amount: uint256):
    self.totalSupply += amount
    self.balanceOf[owner] += amount
    log Transfer(ZERO_ADDRESS, owner, amount)


@internal
def _burn(owner: address, amount: uint256):
    self.totalSupply -= amount
    self.balanceOf[owner] -= amount
    log Transfer(owner, ZERO_ADDRESS, amount)


@external
@payable
def __default__():
    tokens: uint256 = stETH(steth).submit(ZERO_ADDRESS, value=msg.value)
    shares: uint256 = stETH(steth).getSharesByPooledEth(tokens)
    self._mint(msg.sender, shares)


@external
def deposit(tokens: uint256 = MAX_UINT256, recipient: address = msg.sender) -> uint256:
    shares: uint256 = stETH(steth).getSharesByPooledEth(tokens)
    self._mint(recipient, shares)
    assert ERC20(steth).transferFrom(msg.sender, self, tokens)
    return shares


@external
def withdraw(shares: uint256 = MAX_UINT256, recipient: address = msg.sender) -> uint256:
    tokens: uint256 = stETH(steth).getPooledEthByShares(shares)
    self._burn(msg.sender, shares)
    assert ERC20(steth).transfer(recipient, tokens)
    return tokens


@view
@external
def pricePerShare() -> uint256:
    if self.totalSupply == 0:
        return 10 ** self.decimals
    return stETH(steth).getPooledEthByShares(10 ** self.decimals)


@internal
def _transfer(sender: address, receiver: address, amount: uint256):
    assert receiver not in [self, ZERO_ADDRESS]
    self.balanceOf[sender] -= amount
    self.balanceOf[receiver] += amount
    log Transfer(sender, receiver, amount)


@external
def transfer(receiver: address, amount: uint256) -> bool:
    self._transfer(msg.sender, receiver, amount)
    return True


@external
def transferFrom(sender: address, receiver: address, amount: uint256) -> bool:
    if (self.allowance[sender][msg.sender] < MAX_UINT256):
        self.allowance[sender][msg.sender] -= amount
        log Approval(sender, msg.sender, self.allowance[sender][msg.sender])
    self._transfer(sender, receiver, amount)
    return True


@external
def approve(spender: address, amount: uint256) -> bool:
    self.allowance[msg.sender][spender] = amount
    log Approval(msg.sender, spender, amount)
    return True
