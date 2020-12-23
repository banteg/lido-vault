import pytest
from brownie import Wei


@pytest.fixture(scope="function", autouse=True)
def shared_setup(fn_isolation):
    pass


@pytest.fixture(scope='module')
def ape(accounts):
    return accounts[0]


@pytest.fixture(scope='module')
def whale(accounts):
    return accounts[1]


@pytest.fixture()
def vault(LidoVault, ape):
    return LidoVault.deploy({"from": ape})


@pytest.fixture(scope='module')
def lido(interface, accounts):
    lido = interface.Lido("0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84")
    oracle = accounts.at(lido.getOracle(), force=True)
    return interface.Lido(lido, owner=oracle)


class Helpers:
    @staticmethod
    def filter_events_from(addr, events):
      return list(filter(lambda evt: evt.address == addr, events))

    @staticmethod
    def report_beacon_balance_increase(lido):
        beacon_stat = lido.getBeaconStat().dict()
        total_pooled_ether = lido.getTotalPooledEther()
        new_beacon_balance = Wei(total_pooled_ether * 1.5) + "1 ether"
        lido.pushBeacon(beacon_stat['beaconValidators'], new_beacon_balance)


@pytest.fixture(scope='module')
def helpers():
    return Helpers
