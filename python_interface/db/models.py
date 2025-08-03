from .database import get_connection
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

class ContractId(BaseModel):
    contract_id: int

class ContractData(BaseModel):
    status: str
    way: str
    product: str
    underlying: str
    currency: str
    strike: str
    price: str
    pubkey: str
    collateral: str
    txid: str
    fund_address: str
    change_address: str

class Counterpart(BaseModel):
    role: str = None
    pubkey: str = None
    txid: str = None
    fund_address: str = None
    change_address: str = None
    collateral: str = None

class Contract(BaseModel):
    contract_id: int
    status: str
    way: str
    product: str
    underlying: str
    currency: str
    strike: str
    price: str
    maker: Counterpart
    taker: Counterpart

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

def take_contract(contract_id, taker):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('UPDATE contracts SET status="in_progress" WHERE id=?', (data.contract_id,))
    cursor.execute('''
        INSERT INTO counterparts (contract_id, role, pubkey, collateral, txid, fund_address, change_address)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (contract_id, 'taker', taker.pubkey, taker.collateral, taker.txid, taker.fund_address, taker.change_address)
    )

    conn.commit()
    conn.close()

def fetch_pending_contracts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            contracts.id,
            contracts.status,
            contracts.way,
            contracts.product,
            contracts.underlying,
            contracts.currency,
            contracts.strike,
            contracts.price
        FROM contracts
        WHERE contracts.status = "pending"
    ''')
    results = cursor.fetchall()

    conn.close()

    contracts = [Contract(
        contract_id=res[0],
        status=res[1],
        way=res[2],
        product=res[3],
        underlying=res[4],
        currency=res[5],
        strike=res[6],
        price=res[7],
        maker=Counterpart(),
        taker=Counterpart()
    ) for res in results]

    return contracts

def fetch_contract(contract_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            contracts.id,
            contracts.status,
            contracts.way,
            contracts.product,
            contracts.underlying,
            contracts.currency,
            contracts.strike,
            contracts.price,
            maker.role,
            maker.pubkey,
            maker.txid,
            maker.fund_address,
            maker.change_address,
            maker.collateral,
            taker.role,
            taker.pubkey,
            taker.txid,
            taker.fund_address,
            taker.change_address,
            taker.collateral
        FROM contracts
        INNER JOIN counterparts AS maker ON contracts.id = maker.contract_id AND maker.role = "maker"
        INNER JOIN counterparts AS taker ON contracts.id = taker.contract_id AND taker.role = "taker"
        WHERE contracts.id = ?
    ''', (contract_id,))
    res = cursor.fetchone()

    conn.close()

    contract = Contract(
        contract_id=res[0],
        status=res[1],
        way=res[2],
        product=res[3],
        underlying=res[4],
        currency=res[5],
        strike=res[6],
        price=res[7],
        maker=Counterpart(
            role=res[8],
            pubkey=res[9],
            txid=res[10],
            fund_address=res[11],
            change_address=res[12],
            collateral=res[13]
        ),
        taker=Counterpart(
            role=res[14],
            pubkey=res[15],
            txid=res[16],
            fund_address=res[17],
            change_address=res[18],
            collateral=res[19]
        )
    )

    return contract
