import pytest


@pytest.fixture
def vault(LidoVault, accounts):
    return LidoVault.deploy({"from": accounts[0]})
