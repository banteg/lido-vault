def test_ape_in(vault, lido, ape, helpers):
    ape.transfer(vault, "1 ether")
    assert lido.balanceOf(ape) == 0
    assert vault.balanceOf(ape) > 0
    vault_shares_before_withdraw = lido.sharesOf(vault)
    assert vault.balanceOf(ape) == vault_shares_before_withdraw
    helpers.report_beacon_balance_increase(lido)
    vault.withdraw()
    assert lido.balanceOf(ape) > 0
    assert lido.sharesOf(vault) <= 1 # dust due to rounding error
    assert lido.sharesOf(ape) + lido.sharesOf(vault) == vault_shares_before_withdraw
    assert vault.balanceOf(ape) == 0


def test_ape_in_share_ratio_diff_from_one(vault, lido, ape, helpers):
    helpers.report_beacon_balance_increase(lido) # make sure price per share is not 1
    assert lido.getPooledEthByShares("1 ether") != "1 ether"
    ape.transfer(vault, "1 ether")
    assert vault.balanceOf(ape) == lido.sharesOf(vault)
