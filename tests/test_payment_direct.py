from services.payment_service import PaymentGateway

def test_process_payment_executes():
    gateway = PaymentGateway()
    result = gateway.process_payment(25.0)
    assert "status" in result

def test_refund_payment_executes():
    gateway = PaymentGateway()
    result = gateway.refund_payment(25.0)
    assert "status" in result
