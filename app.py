
from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
from database import init_db, log_transaction, get_all_transactions

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

@app.route('/api/authorize', methods=['POST'])
def authorize_payment():
    data = request.json
    card_number = data.get('card_number')
    amount = data.get('amount')
    
    # Validate input
    if not card_number or not amount or amount <= 0:
        return jsonify({'status': 'error', 'message': 'Invalid card number or amount'}), 400
    
    # Hash card number for security
    hashed_card = hashlib.sha256(card_number.encode()).hexdigest()
    
    # Mock authorization: success if card number is 16 digits
    status = 'success' if len(card_number) == 16 else 'failed'
    transaction_id = log_transaction(hashed_card, amount, status)
    
    return jsonify({
        'status': status,
        'transaction_id': transaction_id,
        'message': f'Transaction {status}'
    })

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    transactions = get_all_transactions()
    return jsonify(transactions)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
