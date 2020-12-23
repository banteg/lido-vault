def test_ape_in(vault, lido, ape):
    ape.transfer(vault, "1 ether")
    assert lido.balanceOf(ape) == 0
    assert vault.balanceOf(ape) > 0
    lido.pushBeacon(0, "100 ether")
    vault.withdraw()
    assert lido.balanceOf(ape) > 0
    assert vault.balanceOf(ape) == 0


def test_ape_in_share_ratio_diff_from_one(vault, lido, ape, report_beacon_balance_increase):
    report_beacon_balance_increase(lido) # make sure price per share is not 1
    assert lido.getPooledEthByShares("1 ether") != "1 ether"
    ape.transfer(vault, "1 ether")
    assert vault.balanceOf(ape) == lido.sharesOf(vault)
