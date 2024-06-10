import random
import time

def mock_payment_gateway():
    # Simulate network delay
    time.sleep(2)
    
    # Randomly determine if the payment is successful or failed
    success_rate = 0.9  # 90% success rate
    is_successful = random.random() < success_rate
    
    if is_successful:
        # Generate a mock transaction ID
        transaction_id = f"TRANS{random.randint(100000, 999999)}"
        return {
            'status': 'success',
            'transaction_id': transaction_id,
            'message': 'Payment was successful'
        }
    else:
        return {
            'status': 'failure',
            'transaction_id': None,
            'message': 'Payment failed due to insufficient funds'
        }
