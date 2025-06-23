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
    const Amount WIN_AMOUNT = Amount::CreateBySatoshiAmount(2000);
    const Amount LOSE_AMOUNT = Amount::CreateBySatoshiAmount(0);
    const std::vector<DlcOutcome> OUTCOMES = {{WIN_AMOUNT, LOSE_AMOUNT}, {LOSE_AMOUNT, WIN_AMOUNT}};

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
        OUTCOMES, local_params, remote_params, MATURITY_TIME, FEE_RATE
        );
    auto fund_tx = dlc_transactions.fund_transaction;
    auto refund_tx = dlc_transactions.refund_transaction;
    auto fund_tx_id = fund_tx.GetTransaction().GetTxid();

    std::string prefix = "Refund Tx to sign: ";
    reply->set_message(prefix + refund_tx.GetHex());
    return grpc::Status::OK;
}
