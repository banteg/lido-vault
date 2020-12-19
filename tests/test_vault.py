def test_share_price(vault, lido):
    before = lido.getPooledEthByShares("1 ether")
    assert vault.pricePerShare() == before
    lido.pushBeacon(0, "100 ether")
    after = lido.getPooledEthByShares("1 ether")
    assert after > before
    assert vault.pricePerShare() == after


def test_deposit(vault, lido, ape):
    lido.submit(ape, {"from": ape, "amount": "1 ether"})
    assert lido.balanceOf(ape) > 0
    lido.approve(vault, lido.balanceOf(ape), {"from": ape})
    vault.deposit()
    assert lido.balanceOf(ape) == 0
    assert vault.balanceOf(ape) > 0
    assert vault.totalSupply() == vault.balanceOf(ape)
    lido.pushBeacon(0, "100 ether")
    vault.withdraw()
    assert lido.balanceOf(ape) > 0
    assert vault.balanceOf(ape) == 0
    assert vault.totalSupply() == 0


def test_ape_in(vault, lido, ape):
    ape.transfer(vault, "1 ether")
    assert lido.balanceOf(ape) == 0
    assert vault.balanceOf(ape) > 0
    lido.pushBeacon(0, "100 ether")
    vault.withdraw()
    assert lido.balanceOf(ape) > 0
    assert vault.balanceOf(ape) == 0
