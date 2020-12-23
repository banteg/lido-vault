import brownie
import pytest


@pytest.fixture(autouse=True)
def setup(accounts, lido, vault):
    lido.submit(accounts[0], {"from": accounts[0], "amount": "1 ether"})
    balance = lido.balanceOf(accounts[0])
    lido.approve(vault, balance, {"from": accounts[0]})
    vault.deposit(balance, {"from": accounts[0]})


def test_sender_balance_decreases(accounts, vault):
    sender_balance = vault.balanceOf(accounts[0])
    amount = sender_balance // 4

    vault.approve(accounts[1], amount, {'from': accounts[0]})
    vault.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert vault.balanceOf(accounts[0]) == sender_balance - amount


def test_receiver_balance_increases(accounts, vault):
    receiver_balance = vault.balanceOf(accounts[2])
    amount = vault.balanceOf(accounts[0]) // 4

    vault.approve(accounts[1], amount, {'from': accounts[0]})
    vault.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert vault.balanceOf(accounts[2]) == receiver_balance + amount


def test_caller_balance_not_affected(accounts, vault):
    caller_balance = vault.balanceOf(accounts[1])
    amount = vault.balanceOf(accounts[0])

    vault.approve(accounts[1], amount, {'from': accounts[0]})
    vault.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert vault.balanceOf(accounts[1]) == caller_balance


def test_caller_approval_affected(accounts, vault):
    approval_amount = vault.balanceOf(accounts[0])
    transfer_amount = approval_amount // 4

    vault.approve(accounts[1], approval_amount, {'from': accounts[0]})
    vault.transferFrom(accounts[0], accounts[2], transfer_amount, {'from': accounts[1]})

    assert vault.allowance(accounts[0], accounts[1]) == approval_amount - transfer_amount


def test_receiver_approval_not_affected(accounts, vault):
    approval_amount = vault.balanceOf(accounts[0])
    transfer_amount = approval_amount // 4

    vault.approve(accounts[1], approval_amount, {'from': accounts[0]})
    vault.approve(accounts[2], approval_amount, {'from': accounts[0]})
    vault.transferFrom(accounts[0], accounts[2], transfer_amount, {'from': accounts[1]})

    assert vault.allowance(accounts[0], accounts[2]) == approval_amount


def test_total_supply_not_affected(accounts, vault):
    total_supply = vault.totalSupply()
    amount = vault.balanceOf(accounts[0])

    vault.approve(accounts[1], amount, {'from': accounts[0]})
    vault.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert vault.totalSupply() == total_supply


def test_returns_true(accounts, vault):
    amount = vault.balanceOf(accounts[0])
    vault.approve(accounts[1], amount, {'from': accounts[0]})
    tx = vault.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert tx.return_value is True


def test_transfer_full_balance(accounts, vault):
    amount = vault.balanceOf(accounts[0])
    receiver_balance = vault.balanceOf(accounts[2])

    vault.approve(accounts[1], amount, {'from': accounts[0]})
    vault.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert vault.balanceOf(accounts[0]) == 0
    assert vault.balanceOf(accounts[2]) == receiver_balance + amount


def test_transfer_zero_lidos(accounts, vault):
    sender_balance = vault.balanceOf(accounts[0])
    receiver_balance = vault.balanceOf(accounts[2])

    vault.approve(accounts[1], sender_balance, {'from': accounts[0]})
    vault.transferFrom(accounts[0], accounts[2], 0, {'from': accounts[1]})

    assert vault.balanceOf(accounts[0]) == sender_balance
    assert vault.balanceOf(accounts[2]) == receiver_balance


def test_transfer_zero_lidos_without_approval(accounts, vault):
    sender_balance = vault.balanceOf(accounts[0])
    receiver_balance = vault.balanceOf(accounts[2])

    vault.transferFrom(accounts[0], accounts[2], 0, {'from': accounts[1]})

    assert vault.balanceOf(accounts[0]) == sender_balance
    assert vault.balanceOf(accounts[2]) == receiver_balance


def test_insufficient_balance(accounts, vault):
    balance = vault.balanceOf(accounts[0])

    vault.approve(accounts[1], balance + 1, {'from': accounts[0]})
    with brownie.reverts():
        vault.transferFrom(accounts[0], accounts[2], balance + 1, {'from': accounts[1]})


def test_insufficient_approval(accounts, vault):
    balance = vault.balanceOf(accounts[0])

    vault.approve(accounts[1], balance - 1, {'from': accounts[0]})
    with brownie.reverts():
        vault.transferFrom(accounts[0], accounts[2], balance, {'from': accounts[1]})


def test_no_approval(accounts, vault):
    balance = vault.balanceOf(accounts[0])

    with brownie.reverts():
        vault.transferFrom(accounts[0], accounts[2], balance, {'from': accounts[1]})


def test_revoked_approval(accounts, vault):
    balance = vault.balanceOf(accounts[0])

    vault.approve(accounts[1], balance, {'from': accounts[0]})
    vault.approve(accounts[1], 0, {'from': accounts[0]})

    with brownie.reverts():
        vault.transferFrom(accounts[0], accounts[2], balance, {'from': accounts[1]})


def test_transfer_to_self(accounts, vault):
    sender_balance = vault.balanceOf(accounts[0])
    amount = sender_balance // 4

    vault.approve(accounts[0], sender_balance, {'from': accounts[0]})
    vault.transferFrom(accounts[0], accounts[0], amount, {'from': accounts[0]})

    assert vault.balanceOf(accounts[0]) == sender_balance
    assert vault.allowance(accounts[0], accounts[0]) == sender_balance - amount


def test_transfer_to_self_no_approval(accounts, vault):
    amount = vault.balanceOf(accounts[0])

    with brownie.reverts():
        vault.transferFrom(accounts[0], accounts[0], amount, {'from': accounts[0]})


def test_transfer_event_fires(accounts, vault):
    amount = vault.balanceOf(accounts[0])

    vault.approve(accounts[1], amount, {'from': accounts[0]})
    tx = vault.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert len(tx.events) == 1
    assert tx.events["Transfer"].values() == [accounts[0], accounts[2], amount]
