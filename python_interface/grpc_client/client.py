import grpc
import oracle_pb2
import oracle_pb2_grpc
from db.models import Counterpart

def send_dlc_request(maker: Counterpart = None, taker: Counterpart = None):
    with grpc.insecure_channel("0.0.0.0:50051") as channel:
        stub = oracle_pb2_grpc.DLCStub(channel)

        if maker and taker:
            request = oracle_pb2.DLCRequest(
                local_pubkey=maker.pubkey,
                local_txid=maker.txid,
                local_fund_address=maker.fund_address,
                local_change_address=maker.change_address,
                remote_pubkey=taker.pubkey,
                remote_txid=taker.txid,
                remote_fund_address=taker.fund_address,
                remote_change_address=taker.change_address
            )
        else:
            raise Exception("Missing maker or taker inputs")

        return stub.CreateDLC(request)
