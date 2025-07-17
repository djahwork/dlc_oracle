from .database import get_connection
from fastapi.encoders import jsonable_encoder

def create_contract(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO contracts (status, strike, way, product, underlying, currency, price)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (data.status, data.strike, data.way, data.product, data.underlying, data.currency, data.price)
    )

    contract_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO counterparts (contract_id, role, pubkey, collateral, txid, fund_address, change_address)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (contract_id, 'maker', data.pubkey, data.collateral, data.txid, data.fund_address, data.change_address)
    )

    conn.commit()
    conn.close()

def take_contract(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('UPDATE contracts SET status="in_progress" WHERE id=?', (data.contract_id,))
    cursor.execute('''
        INSERT INTO counterparts (contract_id, role, pubkey, collateral, txid, fund_address, change_address)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (data.contract_id, 'taker', data.pubkey, data.collateral, data.txid, data.fund_address, data.change_address)
    )

    cursor.execute('''
        SELECT pubkey, txid, fund_address, change_address
        FROM counterparts
        WHERE contract_id=? AND role='maker'
    ''', (data.contract_id,))
    result = cursor.fetchone()

    conn.commit()
    conn.close()
    return result

def fetch_contracts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            contracts.id, contracts.status, contracts.way, contracts.product,
            contracts.underlying, contracts.currency, contracts.strike,
            contracts.price, counterparts.role, counterparts.pubkey,
            counterparts.collateral, counterparts.id
        FROM contracts
        INNER JOIN counterparts ON contracts.id = counterparts.contract_id
    ''')
    rows = cursor.fetchall()
    conn.close()

    return {"results": [dict(zip([
        "id", "status", "way", "product", "underlying", "currency",
        "strike", "price", "role", "pubkey", "collateral", "counterpart_id"
    ], row)) for row in rows]}
