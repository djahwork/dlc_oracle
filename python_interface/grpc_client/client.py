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
                local_pubkey="0313d4a6c1ec5398a2353682ba979579d4c08a28b65f1afc4931696c60e671d5e9",
                local_txid="ff33adc805639b003451a12eee3a5f01480786ebe1e6087b198b46f2dc6936ab",
                local_fund_address="tb1qx7m5vx28mm6cmrj4gkwjm27qjtgzsu85d7k8kj",
                local_change_address="tb1qxq386xe64jytpydna35me0aqwgk3rxqlc9jhsl",
                remote_pubkey="025b02828008b6b757b04fdce6e67175a51201d30fae207916bafae210e512d388",
                remote_txid="ff33adc805639b003451a12eee3a5f01480786ebe1e6087b198b46f2dc6936ab",
                remote_fund_address="tb1qxnk3v6c5knt53drts85vuf05uzyrawvlwkwajf",
                remote_change_address="tb1qn92klx003crrkplc7208x9n2xw5786le52hn96"
            )

        return stub.CreateDLC(request)
