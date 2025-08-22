import pytest
from backend.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        from database import init_db
        init_db()  # Reset database for tests
        yield client

def test_authorize_payment_success(client):
    response = client.post('/api/authorize', json={
        'card_number': '1234567890123456',
        'amount': 100.0
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['message'] == 'Transaction success'

def test_authorize_payment_invalid_card(client):
    response = client.post('/api/authorize', json={
        'card_number': '123',
        'amount': 100.0
    })
    assert response.status_code == 200
    assert response.json['status'] == 'failed'
    assert response.json['message'] == 'Transaction failed'

def test_authorize_payment_invalid_amount(client):
    response = client.post('/api/authorize', json={
        'card_number': '1234567890123456',
        'amount': 0
    })
    assert response.status_code == 400
    assert response.json['status'] == 'error'

def test_get_transactions(client):
    client.post('/api/authorize', json={
        'card_number': '1234567890123456',
        'amount': 100.0
    })
    response = client.get('/api/transactions')
    assert response.status_code == 200
    assert len(response.json) >= 1