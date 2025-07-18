import sqlite3

def get_connection():
    return sqlite3.connect("db/app.db")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT,
            way TEXT,
            product TEXT,
            underlying TEXT,
            currency TEXT,
            strike TEXT,
            price TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS counterparts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_id INTEGER NOT NULL,
            role TEXT CHECK(role IN ('maker', 'taker')) NOT NULL,
            pubkey TEXT NOT NULL,
            collateral TEXT NOT NULL,
            txid TEXT NOT NULL,
            fund_address TEXT NOT NULL,
            change_address TEXT NOT NULL,
            FOREIGN KEY (contract_id) REFERENCES contracts (id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()
