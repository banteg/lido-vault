import math


def test_share_price(vault, lido, report_beacon_balance_increase):
    before = lido.getPooledEthByShares("1 ether")
    assert vault.pricePerShare() == before
    report_beacon_balance_increase(lido)
    after = lido.getPooledEthByShares("1 ether")
    assert after > before
    assert vault.pricePerShare() == after


def test_deposit_max(vault, lido, ape):
    lido.submit(ape, {"from": ape, "amount": "1 ether"})
    ape_steth_balance_before = lido.balanceOf(ape)
    assert ape_steth_balance_before > 0

    lido.approve(vault, ape_steth_balance_before, {"from": ape})
    vault.deposit({"from": ape})
    assert lido.balanceOf(ape) == 0
    assert lido.balanceOf(vault) == ape_steth_balance_before
    assert vault.balanceOf(ape) == lido.sharesOf(vault)
    assert vault.totalSupply() == vault.balanceOf(ape)


def test_deposit_amount(vault, lido, ape):
    lido.submit(ape, {"from": ape, "amount": "3 ether"})
    ape_steth_balance_before = lido.balanceOf(ape)
    assert ape_steth_balance_before > 0

    lido.approve(vault, ape_steth_balance_before, {"from": ape})
    vault.deposit("2 ether", {"from": ape})
    assert lido.balanceOf(ape) > 0
    assert lido.balanceOf(vault) > 0
    assert lido.balanceOf(ape) + lido.balanceOf(vault) == ape_steth_balance_before
    assert vault.balanceOf(ape) == lido.sharesOf(vault)
    assert vault.totalSupply() == vault.balanceOf(ape)


def test_deposit_for(vault, lido, whale, ape):
    lido.submit(whale, {"from": whale, "amount": "1 ether"})
    ape_steth_balance_before = lido.balanceOf(whale)
    assert ape_steth_balance_before > 0

    lido.approve(vault, ape_steth_balance_before, {"from": whale})
    vault.deposit("1 ether", ape, {"from": whale})
    assert lido.balanceOf(whale) == 0
    assert lido.balanceOf(vault) == ape_steth_balance_before
    assert vault.balanceOf(whale) == 0
    assert vault.balanceOf(ape) == lido.sharesOf(vault)
    assert vault.totalSupply() == vault.balanceOf(ape)


def test_withdraw_same_rate(vault, lido, ape):
    lido.submit(ape, {"from": ape, "amount": "1 ether"})
    ape_steth_balance_before = lido.balanceOf(ape)
    assert ape_steth_balance_before > 0

    lido.approve(vault, ape_steth_balance_before, {"from": ape})
    vault.deposit({"from": ape})
    assert lido.balanceOf(ape) == 0
    assert vault.balanceOf(ape) == lido.sharesOf(vault)
    assert vault.totalSupply() == vault.balanceOf(ape)

    vault.withdraw({"from": ape})
    assert lido.balanceOf(ape) == ape_steth_balance_before
    assert vault.balanceOf(ape) == 0
    assert vault.totalSupply() == 0


def test_partial_withdraw_same_rate(vault, lido, ape):
    lido.submit(ape, {"from": ape, "amount": "3 ether"})
    ape_shares_before = lido.sharesOf(ape)
    assert lido.balanceOf(ape) > 0

    lido.approve(vault, lido.balanceOf(ape), {"from": ape})
    vault.deposit({"from": ape})
    assert lido.balanceOf(ape) == 0
    assert lido.sharesOf(vault) == ape_shares_before
    assert vault.balanceOf(ape) == ape_shares_before
    assert vault.totalSupply() == vault.balanceOf(ape)

    vault.withdraw("2 ether", {"from": ape})
    assert lido.sharesOf(ape) > 0
    assert vault.balanceOf(ape) > 0
    assert lido.sharesOf(ape) + vault.balanceOf(ape) == ape_shares_before
    assert vault.totalSupply() == vault.balanceOf(ape)


def test_withdraw_diff_rate(vault, lido, ape, report_beacon_balance_increase):
    lido.submit(ape, {"from": ape, "amount": "1 ether"})
    ape_steth_balance_before = lido.balanceOf(ape)
    ape_shares_before = lido.sharesOf(ape)
    assert ape_steth_balance_before > 0
    assert ape_shares_before > 0

    lido.approve(vault, ape_steth_balance_before, {"from": ape})
    vault.deposit({"from": ape})
    assert lido.balanceOf(ape) == 0
    assert vault.balanceOf(ape) == lido.sharesOf(vault)
    assert vault.totalSupply() == vault.balanceOf(ape)

    ape_vault_balance = vault.balanceOf(ape)
    report_beacon_balance_increase(lido)
    assert vault.balanceOf(ape) == ape_vault_balance

    vault.withdraw({"from": ape})
    assert lido.balanceOf(ape) > ape_steth_balance_before
    assert math.fabs(lido.sharesOf(ape) - ape_shares_before) < 10
    assert vault.balanceOf(ape) == 0
    assert vault.totalSupply() == 0
