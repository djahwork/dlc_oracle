from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from db.models import create_contract, take_contract, fetch_contract, fetch_pending_contracts
from grpc_client.client import send_dlc_request
from db.models import ContractId, ContractData, TakeContractData

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "DLC Oracle API"}

@router.post("/api/contract/new")
async def new_contract(data: ContractData):
    create_contract(data)
    return JSONResponse(content={"message": "Contract saved"})

@router.post("/api/contract/take")
async def take(data: TakeContractData):
    take_contract(data)
    return JSONResponse(content={"message": "Contract taken"})

@router.get("/api/contract/pending")
async def show_contracts():
    contracts = fetch_pending_contracts()
    results = [
        {
            "id": contract.contract_id,
            "status": contract.status,
            "way": contract.way,
            "product": contract.product,
            "underlying": contract.underlying,
            "currency": contract.currency,
            "strike": contract.strike,
            "price": contract.price
        }
        for contract in contracts
    ]
    return JSONResponse(content={"results": results})

@router.get("/api/contract/show/{contract_id}")
async def show_contract(data: ContractId):
    return fetch_contract(data.contract_id)

@router.post("/api/dlc/new")
async def new_dlc(data: ContractId):
    contract = fetch_contract(data.contract_id)

    try:
        grpc_result = send_dlc_request(contract.maker, contract.taker)
    except Exception as err:
        return JSONResponse(content={"message": f"error: {err}"})
    else:
        return JSONResponse(content={
            "fund_tx": grpc_result.fund_tx,
            "refund_tx": grpc_result.refund_tx,
            "cets": [res for res in grpc_result.cet_txs]
        })
