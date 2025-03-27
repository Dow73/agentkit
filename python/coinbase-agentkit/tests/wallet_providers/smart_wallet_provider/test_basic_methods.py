"""tests for smart wallet provider basic methods."""

from decimal import Decimal

import pytest

from coinbase_agentkit.network import Network

from .conftest import (
    MOCK_ADDRESS,
    MOCK_CHAIN_ID,
    MOCK_NETWORK_ID,
    MOCK_ONE_ETH_WEI,
)

# =========================================================
# basic methods tests
# =========================================================


def test_get_address(wallet_provider):
    """Test get_address method."""
    address = wallet_provider.get_address()
    assert address == MOCK_ADDRESS
    assert address.startswith("0x")
    assert len(address) == 42


def test_get_network(wallet_provider):
    """Test get_network method."""
    network = wallet_provider.get_network()
    assert isinstance(network, Network)
    assert network.protocol_family == "evm"
    assert network.network_id == MOCK_NETWORK_ID
    assert network.chain_id == MOCK_CHAIN_ID


def test_get_name(wallet_provider):
    """Test get_name method."""
    assert wallet_provider.get_name() == "cdp_smart_wallet_provider"


def test_get_balance(wallet_provider, mock_web3):
    """Test get_balance method."""
    mock_web3.return_value.eth.get_balance.return_value = MOCK_ONE_ETH_WEI

    balance = wallet_provider.get_balance()

    assert balance == Decimal(MOCK_ONE_ETH_WEI)
    mock_web3.return_value.eth.get_balance.assert_called_once_with(MOCK_ADDRESS)


def test_get_balance_with_zero(wallet_provider, mock_web3):
    """Test get_balance method with zero balance."""
    mock_web3.return_value.eth.get_balance.return_value = 0

    balance = wallet_provider.get_balance()

    mock_web3.return_value.eth.get_balance.assert_called_once_with(MOCK_ADDRESS)
    assert balance == Decimal("0")


def test_get_balance_failure(wallet_provider, mock_web3):
    """Test get_balance method when balance check fails."""
    error_message = "Balance check failed"
    mock_web3.return_value.eth.get_balance.side_effect = Exception(error_message)

    with pytest.raises(Exception, match=error_message):
        wallet_provider.get_balance()


def test_get_balance_with_connection_error(wallet_provider, mock_web3):
    """Test get_balance method with network connection error."""
    mock_web3.return_value.eth.get_balance.side_effect = ConnectionError("Network connection error")

    with pytest.raises(ConnectionError, match="Network connection error"):
        wallet_provider.get_balance()
