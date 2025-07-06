import grpc
import oracle_pb2
import oracle_pb2_grpc

def send_dlc_request(creator=None, buyer=None):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = oracle_pb2_grpc.DLCStub(channel)

        if creator and buyer:
            request = oracle_pb2.DLCRequest(
                local_pubkey=creator[0],
                local_txid=creator[1],
                local_fund_address=creator[2],
                local_change_address=creator[3],
                remote_pubkey=buyer.pubkey,
                remote_txid=buyer.txid,
                remote_fund_address=buyer.fund_address,
                remote_change_address=buyer.change_address
            )
        else:
            request = oracle_pb2.DLCRequest(name="Python Client")

        return stub.CreateDLC(request)
