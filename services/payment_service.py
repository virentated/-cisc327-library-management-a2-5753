import random

class PaymentGateway:
   

    def process_payment(self, amount: float) -> dict:
        #Simulate processing a payment for the given amount.
        if amount <= 0:
            raise ValueError("Invalid payment amount.")

        approved = random.choice([True, True, True, False])  # 75% chance of success
        if approved:
            return {"status": "success", "transaction_id": f"TXN{random.randint(1000, 9999)}"}
        else:
            return {"status": "declined", "reason": "Insufficient funds"}

    def refund_payment(self, amount: float) -> dict:
        #Simulate refunding a payment for the given amount.
        if amount <= 0:
            raise ValueError("Invalid refund amount.")

        success = random.choice([True, True, False])  # ~66% chance of success
        if success:
            return {"status": "refunded", "amount": amount}
        else:
            return {"status": "failed", "reason": "Gateway error"}
