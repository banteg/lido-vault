import brownie
import pytest


def test_sender_balance_decreases(vault, lido, ape, whale):
    whale.transfer(vault, "10 ether")

    whale_balance_before = vault.balanceOf(whale)
    amount = "1 ether"

    vault.transfer(ape, amount, {'from': whale})

    assert vault.balanceOf(whale) == whale_balance_before - amount


def test_receiver_balance_increases(vault, lido, ape, whale):
    whale.transfer(vault, "10 ether")
    amount = "1 ether"
    vault.transfer(ape, "1 ether", {'from': whale})

    ape_balance_before = vault.balanceOf(ape)
    vault.transfer(ape, amount, {'from': whale})

    assert vault.balanceOf(ape) == ape_balance_before + amount


def test_total_supply_not_affected(vault, lido, ape, whale):
    whale.transfer(vault, "10 ether")
    amount = "1 ether"

    total_supply = vault.totalSupply()
    vault.transfer(ape, "1 ether", {'from': whale})

    assert vault.totalSupply() == total_supply


def test_returns_true(vault, lido, ape, whale):
    whale.transfer(vault, "10 ether")

    amount = "1 ether"
    vault.transfer(ape, amount, {'from': whale})

    tx = vault.transfer(ape, amount, {'from': whale})

    assert tx.return_value is True


def test_insufficient_balance(vault, lido, ape, whale):
    whale.transfer(vault, "10 ether")

    with brownie.reverts():
        vault.transfer(ape, "100 ether", {'from': whale})


def test_transfer_full_balance(vault, lido, ape, whale):
    whale.transfer(vault, "10 ether")
    amount = vault.balanceOf(whale)
    ape_balance = vault.balanceOf(ape)

    vault.transfer(ape, amount, {'from': whale})

    assert vault.balanceOf(whale) == 0
    assert vault.balanceOf(ape) == ape_balance + amount


def test_transfer_zero_vaults(vault, lido, ape, whale):
    whale.transfer(vault, "10 ether")
    sender_balance = vault.balanceOf(whale)
    receiver_balance = vault.balanceOf(ape)

    vault.transfer(ape, 0, {'from': whale})

    assert vault.balanceOf(whale) == sender_balance
    assert vault.balanceOf(ape) == receiver_balance


def test_transfer_to_self(vault, lido, ape, whale):
    whale.transfer(vault, "10 ether")
    sender_balance = vault.balanceOf(whale)

    vault.transfer(whale, "1 ether", {'from': whale})

    assert vault.balanceOf(whale) == sender_balance


def test_transfer_event_fires(vault, lido, ape, whale):
    whale.transfer(vault, "10 ether")
    amount = vault.balanceOf(whale)
    tx = vault.transfer(ape, amount, {'from': whale})

    assert len(tx.events) == 1
    assert tx.events["Transfer"].values() == [whale, ape, amount]
