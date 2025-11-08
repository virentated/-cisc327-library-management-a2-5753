"""
Tests using STUBS (fake return values without verification)
Focus: Database/business logic stubbing for pay_late_fees().
"""

import services.library_service as ls
from unittest.mock import Mock
from services.payment_service import PaymentGateway


def test_stub_fee_and_book_success(mocker):
    #Stub calculate_late_fee_for_book and get_book_by_id to simulate valid fee & book
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 5.0})
    mocker.patch("services.library_service.get_book_by_id", return_value={"title": "StubBook"})

    fake_gateway = Mock(spec=PaymentGateway)
    fake_gateway.process_payment.return_value = {"status": "success", "transaction_id": "TXN0001"}

    result = ls.pay_late_fees("123456", 1, fake_gateway)
    assert result["success"] is True
    assert "paid" in result["message"].lower()


def test_stub_zero_fee_no_payment(mocker):
    #Stub a zero-fee scenario to check no payment occurs
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 0.0})
    mocker.patch("services.library_service.get_book_by_id", return_value={"title": "StubBook"})

    fake_gateway = Mock(spec=PaymentGateway)
    result = ls.pay_late_fees("123456", 1, fake_gateway)

    fake_gateway.process_payment.assert_not_called()
    assert "no late fee" in result["message"].lower()


def test_stub_missing_book(mocker):
    #Stub missing book record to trigger 'book not found'
    mocker.patch("services.library_service.calculate_late_fee_for_book", return_value={"fee_amount": 5.0})
    mocker.patch("services.library_service.get_book_by_id", return_value=None)

    fake_gateway = Mock(spec=PaymentGateway)
    result = ls.pay_late_fees("123456", 99, fake_gateway)

    assert result["success"] is False
    assert "book not found" in result["message"].lower()
