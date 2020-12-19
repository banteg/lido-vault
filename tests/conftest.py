import pytest


@pytest.fixture(scope="function", autouse=True)
def shared_setup(fn_isolation):
    pass


@pytest.fixture
def ape(accounts):
    return accounts[0]


@pytest.fixture
def vault(LidoVault, ape):
    return LidoVault.deploy({"from": ape})


@pytest.fixture
def lido(interface, accounts):
    lido = interface.Lido("0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84")
    oracle = accounts.at(lido.getOracle(), force=True)
    return interface.Lido(lido, owner=oracle)
