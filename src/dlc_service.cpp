#include "dlc_service.h"

#include <cfddlc/cfddlc_transactions.h>
#include <cfdcore/cfdcore_key.h>
#include <cfdcore/cfdcore_util.h>
#include <cfddlc/cfddlc_common.h>

using cfd::core::Amount;
using cfd::core::Pubkey;
using cfd::core::Address;
using cfd::core::TxIn;
using cfd::core::Txid;
using cfd::dlc::DlcOutcome;
using cfd::dlc::TxInputInfo;
using cfd::dlc::PartyParams;
using cfd::dlc::DlcManager;

grpc::Status DlcService::CreateDLC(
    grpc::ServerContext*, const oracle::DLCRequest* request, oracle::DLCReply* reply
) {
    std::vector<std::string> outcome_labels = {"BTC=1000", "BTC=3000"};

    const std::vector<DlcOutcome> outcomes = {
        {Amount::CreateBySatoshiAmount(10000), Amount::CreateBySatoshiAmount(0)},
        {Amount::CreateBySatoshiAmount(7000), Amount::CreateBySatoshiAmount(3000)}
    };
    /*
    const cfd::Privkey oracle_priv = cfd::Privkey::GenerageRandomKey();
    const cfd::core::SchnorrPubkey oracle_pub = cfd::core::SchnorrPubkey::FromPrivkey(oracle_priv);

    std::vector<cfd::Privkey> oracle_k_values;
    std::vector<cfd::core::SchnorrPubkey> oracle_r_points;
    for (size_t i = 0; i < outcomes.size(); ++i) {
        auto r_priv = cfd::Privkey::GenerageRandomKey();
        auto r_pub = cfd::core::SchnorrPubkey::FromPrivkey(r_priv);
        oracle_k_values.push_back(r_priv);
        oracle_r_points.push_back(r_pub);
    }

    std::vector<std::vector<cfd::dlc::ByteData256>> outcome_msgs;
    for (const auto& label : outcome_labels) {
        cfd::dlc::ByteData256 msg = cfd::core::HashUtil::Sha256(label);
        outcome_msgs.push_back({msg});
    }
    */
    //const Pubkey local_pubkey(request->local_pubkey());
    std::cout << "request local pubkey: " << request->local_pubkey() << std::endl;
    const Pubkey local_pubkey("0313d4a6c1ec5398a2353682ba979579d4c08a28b65f1afc4931696c60e671d5e9");
    const Address local_change_address("tb1qxq386xe64jytpydna35me0aqwgk3rxqlc9jhsl");
    const Address local_final_address("tb1qx7m5vx28mm6cmrj4gkwjm27qjtgzsu85d7k8kj");
    const std::vector<TxInputInfo> local_inputs_info = {
        TxInputInfo{TxIn(Txid("ff33adc805639b003451a12eee3a5f01480786ebe1e6087b198b46f2dc6936ab"), 0, 0), 108}
    };
    const Amount local_input_amount = Amount::CreateBySatoshiAmount(100965);
    const Amount local_collateral_amount = Amount::CreateBySatoshiAmount(10000);

    const PartyParams local_params = {
        local_pubkey, local_change_address.GetLockingScript(),
        local_final_address.GetLockingScript(), local_inputs_info,
        local_input_amount, local_collateral_amount
    };

    const Pubkey remote_pubkey("025b02828008b6b757b04fdce6e67175a51201d30fae207916bafae210e512d388");
    const Address remote_change_address("tb1qn92klx003crrkplc7208x9n2xw5786le52hn96");
    const Address remote_final_address("tb1qxnk3v6c5knt53drts85vuf05uzyrawvlwkwajf");
    const std::vector<TxInputInfo> remote_inputs_info = {
        TxInputInfo{TxIn(Txid("ff33adc805639b003451a12eee3a5f01480786ebe1e6087b198b46f2dc6936ab"), 0, 0), 108}
    };
    const Amount remote_input_amount = Amount::CreateBySatoshiAmount(25035);
    const Amount remote_collateral_amount = Amount::CreateBySatoshiAmount(0);

    const PartyParams remote_params = {
        remote_pubkey, remote_change_address.GetLockingScript(),
        remote_final_address.GetLockingScript(), remote_inputs_info,
        remote_input_amount, remote_collateral_amount
    };

    const uint32_t MATURITY_TIME = 1579072156;
    const uint32_t FEE_RATE = 1;

    std::cout << "test" << std::endl;

    auto dlc_transactions = DlcManager::CreateDlcTransactions(
        outcomes, local_params, remote_params, MATURITY_TIME, FEE_RATE
    );

    std::cout << "test" << std::endl;
    std::cout << "fund tx: " << dlc_transactions.fund_transaction.GetHex() << std::endl;
    for(const auto& cet: dlc_transactions.cets){
        std::cout << "cet: " << cet.GetHex() << std::endl;
    }
    std::cout << "refund tx: " << dlc_transactions.refund_transaction.GetHex() << std::endl;
    return grpc::Status::OK;
    /*
    Amount fund_input = local_input_amount + remote_input_amount;

    reply->set_fund_tx(dlc_transactions.fund_transaction.GetHex());
    reply->set_refund_tx(dlc_transactions.refund_transaction.GetHex());

    for (const auto& cet : dlc_transactions.cets) {
        reply->add_cet_txs(cet.GetHex());
    }

    for (const auto& r : r_values) {
        reply->add_r_values(r.GetData().GetHex());
    }

    for (const auto& msg_vec : outcome_msgs) {
        for (const auto& msg : msg_vec) {
            reply->add_outcome_messages(msg.GetHex());
        }
    }

    return grpc::Status::OK;*/
}
