#include <gtest/gtest.h>
#include "../src/dlc_service.h"  // Your gRPC service implementation

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

using grpc::ServerContext;
using oracle::DLCRequest;
using oracle::DLCReply;

class DlcServiceTest : public ::testing::Test {
protected:
    DlcService service;  // Your DlcService class implementing the gRPC server
};

TEST_F(DlcServiceTest, CreateDlc_ReturnsTransactionsAndSignatures) {
    ServerContext context;
    oracle::DLCRequest *request;
    oracle::DLCReply *reply;

    std::vector<std::string> outcome_labels = {"BTC=1000", "BTC=3000"};

    const std::vector<DlcOutcome> outcomes = {
        {Amount::CreateBySatoshiAmount(10000), Amount::CreateBySatoshiAmount(0)},
        {Amount::CreateBySatoshiAmount(7000), Amount::CreateBySatoshiAmount(3000)}
    };

    std::vector<cfd::core::SchnorrPubkey> r_values;
    std::vector<cfd::Privkey> r_privkeys;
    for (size_t i = 0; i < outcomes.size(); ++i) {
        auto r_priv = cfd::Privkey::GenerageRandomKey();
        r_privkeys.push_back(r_priv);
        auto r_pub = cfd::core::SchnorrPubkey::FromPrivkey(r_priv);
        r_values.push_back(r_pub);
    }

    std::vector<std::vector<cfd::dlc::ByteData256>> outcome_msgs;
    for (const auto& label : outcome_labels) {
        cfd::dlc::ByteData256 msg = cfd::core::HashUtil::Sha256(label);
        outcome_msgs.push_back({msg});
    }

    ///////////////// LOCAL INPUTS //////////////////////////////
    const Pubkey local_pubkey(request->local_pubkey());
    const Address local_change_address(request->local_change_address());
    const Address local_final_address(request->local_fund_address());
    const std::vector<TxInputInfo> local_inputs_info = {
        TxInputInfo{TxIn(Txid(request->local_txid()), 0, 0), 108}
    };
    const Amount local_input_amount = Amount::CreateBySatoshiAmount(1500);
    const Amount local_collateral_amount = Amount::CreateBySatoshiAmount(1000);

    const PartyParams local_params = {
        local_pubkey, local_change_address.GetLockingScript(),
        local_final_address.GetLockingScript(), local_inputs_info,
        local_input_amount, local_collateral_amount
    };

    ///////////////// REMOTE INPUTS //////////////////////////////
    const Pubkey remote_pubkey(request->remote_pubkey());
    const Address remote_change_address(request->remote_change_address());
    const Address remote_final_address(request->remote_fund_address());
    const std::vector<TxInputInfo> remote_inputs_info = {
        TxInputInfo{TxIn(Txid(request->remote_txid()), 0, 0), 108}
    };
    const Amount remote_input_amount = Amount::CreateBySatoshiAmount(1500);
    const Amount remote_collateral_amount = Amount::CreateBySatoshiAmount(1000);

    const PartyParams remote_params = {
        remote_pubkey, remote_change_address.GetLockingScript(),
        remote_final_address.GetLockingScript(), remote_inputs_info,
        remote_input_amount, remote_collateral_amount
    };

    ////////////////////////////////////////////////////

    const uint32_t MATURITY_TIME = 1579072156;
    const uint32_t FEE_RATE = 1;

    Amount fund_input = local_input_amount + remote_input_amount;

    auto dlc_transactions = DlcManager::CreateDlcTransactions(
        outcomes, local_params, remote_params, MATURITY_TIME, FEE_RATE
    );

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

    //grpc::Status status = service.CreateDLC(&context, &request, &reply);

    //EXPECT_TRUE(status.ok());          // R-values present
}
