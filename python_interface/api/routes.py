from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from db.models import create_contract, take_contract, fetch_contracts
from grpc_client.client import send_dlc_request
from pydantic import BaseModel

router = APIRouter()

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

class TakeContractData(ContractData):
    contract_id: int

@router.get("/")
async def root():
    return {"message": "DLC Oracle API"}

@router.post("/api/contract/new")
async def new_contract(data: ContractData):
    create_contract(data)
    return JSONResponse(content={"message": "Contract saved"})

@router.post("/api/contract/take")
async def take(data: TakeContractData):
    result = take_contract(data)
    if not result:
        return JSONResponse(content={"message": "Error"}, status_code=500)

    grpc_result = send_dlc_request(result, data)
    return JSONResponse(content={"message": grpc_result.message})

@router.get("/api/contract")
async def show_contracts():
    return fetch_contracts()

@router.post("/api/dlc/new")
async def new_dlc():
    response = send_dlc_request()
    return JSONResponse(content={"message": response.message})
