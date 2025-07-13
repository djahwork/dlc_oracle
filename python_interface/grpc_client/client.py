import grpc
import oracle_pb2
import oracle_pb2_grpc

def send_dlc_request(creator=None, buyer=None):
    with grpc.insecure_channel("0.0.0.0:50051") as channel:
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
            # raise Exception("Missing creator or buyer inputs")
            request = oracle_pb2.DLCRequest(
                local_pubkey="test_local_pub",
                local_txid="test_local_txid",
                local_fund_address="local_fund_address",
                local_change_address="local_change_address",
                remote_pubkey="remote_pubkey",
                remote_txid="remote_txid",
                remote_fund_address="remote_fund_address",
                remote_change_address="remote_change_address"
            )

        return stub.CreateDLC(request)
