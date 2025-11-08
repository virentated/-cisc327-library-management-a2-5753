"""
Tests using MOCKS (verifying interactions)
Focus: PaymentGateway behavior for pay_late_fees() and refund_late_fee_payment().
"""

import pytest
from unittest.mock import Mock
import services.library_service as ls
from services.payment_service import PaymentGateway



def test_mock_payment_success(mocker):
    #Verify process_payment is called correctly when payment succeeds
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 5.0})
    mocker.patch("services.library_service.get_book_by_id", return_value={"title": "MockBook"})

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = {"status": "success", "transaction_id": "TXN1111"}

    result = ls.pay_late_fees("123456", 1, mock_gateway)
    assert result["success"] is True
    mock_gateway.process_payment.assert_called_once_with("123456", 5.0)


def test_mock_payment_declined(mocker):
    #Verify mock call and decline handling
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 10.0})
    mocker.patch("services.library_service.get_book_by_id", return_value={"title": "MockBook"})

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = {"status": "declined", "reason": "Insufficient funds"}

    result = ls.pay_late_fees("123456", 1, mock_gateway)
    assert result["success"] is False
    mock_gateway.process_payment.assert_called_once()


def test_mock_invalid_patron_not_called():
    #Invalid patron IDs should not trigger external API calls
    mock_gateway = Mock(spec=PaymentGateway)
    result = ls.pay_late_fees("xx12", 1, mock_gateway)
    mock_gateway.process_payment.assert_not_called()
    assert "invalid" in result["message"].lower()


def test_mock_network_error(mocker):
    #Simulate network error (exception thrown by mock)
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 5.0})
    mocker.patch("services.library_service.get_book_by_id", return_value={"title": "MockBook"})

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.side_effect = Exception("Network down")

    result = ls.pay_late_fees("123456", 1, mock_gateway)
    assert result["success"] is False
    assert "network" in result["message"].lower()


# MOCK TESTS for refund_late_fee_payment()
def test_mock_refund_success():
    #Verify refund is successful and mock called once
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = {"status": "refunded"}

    result = ls.refund_late_fee_payment("TXN1234", 5.0, mock_gateway)
    assert result["success"] is True
    mock_gateway.refund_payment.assert_called_once_with("TXN1234", 5.0)


def test_mock_refund_invalid_transaction():
    #Invalid transaction ID should prevent gateway call
    mock_gateway = Mock(spec=PaymentGateway)
    result = ls.refund_late_fee_payment("BADID", 5.0, mock_gateway)
    mock_gateway.refund_payment.assert_not_called()
    assert "invalid" in result["message"].lower()


@pytest.mark.parametrize("amt", [-5, 0, 20])
def test_mock_refund_invalid_amounts(amt):
    #Invalid amounts (negative, zero, or >15) should block refund calls
    mock_gateway = Mock(spec=PaymentGateway)
    result = ls.refund_late_fee_payment("TXN1234", amt, mock_gateway)
    mock_gateway.refund_payment.assert_not_called()
    assert "invalid" in result["message"].lower()
