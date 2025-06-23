from flask import Flask, jsonify, request, render_template
import sqlite3
import json
import grpc
import oracle_pb2
import oracle_pb2_grpc

app = Flask(__name__)

class Contract:
    def __init__(self):
        pass

@app.route('/')
def home():

    location = 'app.db'
    conn = sqlite3.connect(location)
    c = conn.cursor()

    c.execute('''
       CREATE TABLE IF NOT EXISTS contracts(
           id integer PRIMARY KEY AUTOINCREMENT,
           status text,
           way text,
           product text,
           underlying text,
           currency text,
           strike text,
           price text
    )''')

    c.execute('''
       CREATE TABLE IF NOT EXISTS counterparts(
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           contract_id INTEGER NOT NULL,
           role TEXT CHECK(role IN ('creator', 'buyer')) NOT NULL,
           pubkey TEXT NOT NULL,
           collateral TEXT NOT NULL,
           txid TEXT NOT NULL,
           fund_address TEXT NOT NULL,
           change_address TEXT NOT NULL,
           FOREIGN KEY (contract_id) REFERENCES contracts (id) ON DELETE CASCADE
    )''')

    conn.commit()
    return render_template('index.html')

@app.route('/api/contract/new', methods=['POST'])
def new_contract():
    data = request.get_json()
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO contracts (status, strike, way, product, underlying, currency, price) VALUES ' \
        '(?, ?, ?, ?, ?, ?, ?)', (data["status"], data["strike"], data["way"], data["product"], data["underlying"], data["currency"], data["price"])
    )
    contract_id = cursor.lastrowid

    cursor.execute('''
            INSERT INTO counterparts (contract_id, role, pubkey, collateral, txid, fund_address, change_address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (contract_id, 'creator', data["pubkey"], data["collateral"], data["txid"], data["fund_address"], data["change_address"])
    )

    conn.commit()
    conn.close()
    return jsonify({"message": "Contract saved"}), 200

@app.route('/api/contract/take', methods=['POST'])
def take_contract():
    data = request.get_json()
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE contracts SET status="in_progress" WHERE id='+data["contract_id"]+'' )
    cursor.execute(
        'INSERT INTO counterparts (contract_id, role, pubkey, collateral, txid, fund_address, change_address) VALUES ' \
        '(?, ?, ?, ?, ?, ?, ?)', (data["contract_id"], 'buyer', data["pubkey"], data["collateral"], data["txid"], data["fund_address"], data["change_address"])
    )
    conn.commit()

    cursor.execute('''
        SELECT
            contracts.id AS contract_id,
            counterparts.pubkey,
            counterparts.txid,
            counterparts.fund_address,
            counterparts.change_address
        FROM contracts
        INNER JOIN counterparts
        ON contracts.id = counterparts.contract_id AND counterparts.role = 'creator'
    ''')
    res = cursor.fetchone()

    conn.close()

    with grpc.insecure_channel('localhost:50051') as channel:
        # Create a stub (client)
        stub = oracle_pb2_grpc.DLCStub(channel)
        # Create a request
        request = oracle_pb2.DLCRequest(
            local_pubkey=res[1],
            local_txid=res[2],
            local_fund_address=res[3],
            local_change_address=res[4],
            remote_pubkey=data["pubkey"],
            remote_txid=data["txid"],
            remote_fund_address=data["fund_address"],
            remote_change_address=data["change_address"]
        )
        response = stub.CreateDLC(request)
        return jsonify({"message": response.message}), 200

    return jsonify({"message": "Error"}), 500

@app.route('/api/contract', methods=['GET'])
def show_all_contract():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            contracts.id AS contract_id,
            contracts.status,
            contracts.way,
            contracts.product,
            contracts.underlying,
            contracts.currency,
            contracts.strike,
            contracts.price,
            counterparts.role,
            counterparts.pubkey,
            counterparts.collateral,
            counterparts.id AS counterpart_id
        FROM contracts
        INNER JOIN counterparts
        ON contracts.id = counterparts.contract_id
    ''')
    res = cursor.fetchall()
    conn.close()
    res = {
        "results": [{
        "id": r[0], "status": r[1], "way": r[2],
        "product": r[3], "underlying": r[4], "currency": r[5], "strike": r[6],
        "price": r[7], "role": r[8], "pubkey": r[9], "collateral": r[10],
        "counterpart_id": r[11]
        } for r in res]
    }
    return json.dumps(res)

@app.route('/api/dlc/new', methods=['POST'])
def new_dlc():
    with grpc.insecure_channel('localhost:50051') as channel:
        # Create a stub (client)
        stub = oracle_pb2_grpc.DLCStub(channel)
        # Create a request
        request = oracle_pb2.DLCRequest(
            name="Python Client"
        )
        # Call the SayHello method
        response = stub.CreateDLC(request)
        return jsonify({"message": response.message}), 200

if __name__ == '__main__':
    app.run(debug=True)
