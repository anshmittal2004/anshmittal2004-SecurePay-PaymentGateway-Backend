import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_hash TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log_transaction(card_hash, amount, status):
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute('INSERT INTO transactions (card_hash, amount, status) VALUES (?, ?, ?)',
              (card_hash, amount, status))
    conn.commit()
    transaction_id = c.lastrowid
    conn.close()
    return transaction_id

def get_all_transactions():
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute('SELECT id, card_hash, amount, status, timestamp FROM transactions')
    transactions = [
        {'id': row[0], 'card_hash': row[1], 'amount': row[2], 'status': row[3], 'timestamp': row[4]}
        for row in c.fetchall()
    ]
    conn.close()
    return transactions