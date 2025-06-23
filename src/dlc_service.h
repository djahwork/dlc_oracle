#ifndef DLC_SERVICE_H
#define DLC_SERVICE_H

#include <grpcpp/grpcpp.h>
#include <cfdcore/cfdcore_amount.h>
#include "oracle.grpc.pb.h"

class DlcService final : public oracle::DLC::Service {
public:
    grpc::Status CreateDLC(grpc::ServerContext*, const oracle::DLCRequest*, oracle::DLCReply*) override;
};


#endif // DLC_SERVICE_H
