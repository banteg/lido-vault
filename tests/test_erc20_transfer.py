import brownie
import pytest


@pytest.fixture(autouse=True)
def before_each(accounts, vault):
    accounts[0].transfer(vault, "1 ether")


def test_sender_balance_decreases(accounts, vault):
    sender_balance = vault.balanceOf(accounts[0])
    amount = sender_balance // 4

    vault.transfer(accounts[1], amount, {'from': accounts[0]})

    assert vault.balanceOf(accounts[0]) == sender_balance - amount


def test_receiver_balance_increases(accounts, vault):
    receiver_balance = vault.balanceOf(accounts[1])
    amount = vault.balanceOf(accounts[0]) // 4

    vault.transfer(accounts[1], amount, {'from': accounts[0]})

    assert vault.balanceOf(accounts[1]) == receiver_balance + amount


def test_total_supply_not_affected(accounts, vault):
    total_supply = vault.totalSupply()
    amount = vault.balanceOf(accounts[0])

    vault.transfer(accounts[1], amount, {'from': accounts[0]})

    assert vault.totalSupply() == total_supply


def test_returns_true(accounts, vault):
    amount = vault.balanceOf(accounts[0])
    tx = vault.transfer(accounts[1], amount, {'from': accounts[0]})

    assert tx.return_value is True


def test_transfer_full_balance(accounts, vault):
    amount = vault.balanceOf(accounts[0])
    receiver_balance = vault.balanceOf(accounts[1])

    vault.transfer(accounts[1], amount, {'from': accounts[0]})

    assert vault.balanceOf(accounts[0]) == 0
    assert vault.balanceOf(accounts[1]) == receiver_balance + amount


def test_transfer_zero_lidos(accounts, vault):
    sender_balance = vault.balanceOf(accounts[0])
    receiver_balance = vault.balanceOf(accounts[1])

    vault.transfer(accounts[1], 0, {'from': accounts[0]})

    assert vault.balanceOf(accounts[0]) == sender_balance
    assert vault.balanceOf(accounts[1]) == receiver_balance


def test_transfer_to_self(accounts, vault):
    sender_balance = vault.balanceOf(accounts[0])
    amount = sender_balance // 4

    vault.transfer(accounts[0], amount, {'from': accounts[0]})

    assert vault.balanceOf(accounts[0]) == sender_balance


def test_insufficient_balance(accounts, vault):
    balance = vault.balanceOf(accounts[0])

    with brownie.reverts():
        vault.transfer(accounts[1], balance + 1, {'from': accounts[0]})


def test_transfer_event_fires(accounts, vault):
    amount = vault.balanceOf(accounts[0])
    tx = vault.transfer(accounts[1], amount, {'from': accounts[0]})

    assert len(tx.events) == 1
    assert tx.events["Transfer"].values() == [accounts[0], accounts[1], amount]


def test_transfer_safety_net_zero_address(accounts, vault):
    with brownie.reverts():
        vault.transfer('0x' + '0' * 40, 1, {'from': accounts[0]})


def test_transfer_safety_net_self(accounts, vault):
    with brownie.reverts():
        vault.transfer(vault, 1, {'from': accounts[0]})
