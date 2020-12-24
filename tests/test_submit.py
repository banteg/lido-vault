def test_ape_in_same_share_price(vault, lido, ape, helpers):
    ape.transfer(vault, "1 ether")
    assert lido.balanceOf(ape) == 0
    assert vault.balanceOf(ape) > 0
    vault_sheth_balance_before_withdraw = lido.balanceOf(vault)
    vault_shares_before_withdraw = lido.sharesOf(vault)
    assert vault.balanceOf(ape) == vault_shares_before_withdraw
    vault.withdraw({"from": ape})
    assert lido.balanceOf(ape) == vault_sheth_balance_before_withdraw
    assert lido.balanceOf(vault) == 0
    assert vault.balanceOf(ape) == 0


def test_ape_in_diff_share_price(vault, lido, ape, helpers):
    ape.transfer(vault, "1 ether")
    assert lido.balanceOf(ape) == 0
    assert vault.balanceOf(ape) > 0
    vault_shares_before_withdraw = lido.sharesOf(vault)
    assert vault.balanceOf(ape) == vault_shares_before_withdraw
    helpers.report_beacon_balance_increase(lido)
    assert vault.balanceOf(ape) == vault_shares_before_withdraw
    vault.withdraw({"from": ape})
    assert lido.balanceOf(ape) > 0
    assert lido.sharesOf(vault) <= 1 # dust due to rounding error
    assert lido.sharesOf(ape) + lido.sharesOf(vault) == vault_shares_before_withdraw
    assert vault.balanceOf(ape) == 0


def test_ape_in_share_ratio_diff_from_one(vault, lido, ape, helpers):
    helpers.report_beacon_balance_increase(lido) # make sure price per share is not 1
    assert lido.getPooledEthByShares("1 ether") != "1 ether"
    ape.transfer(vault, "1 ether")
    assert vault.balanceOf(ape) == lido.sharesOf(vault)
