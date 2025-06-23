#ifndef GRPC_SERVER_H
#define GRPC_SERVER_H

#include <grpcpp/grpcpp.h>
#include <QtCore/QObject>

class GrpcServer : public QObject {
    Q_OBJECT
public:
    explicit GrpcServer(const std::string& address, QObject* parent = nullptr);
    ~GrpcServer() override;

    bool start();
    void stop();

private:
    std::string address_;
    std::unique_ptr<grpc::Server> server_;
};

#endif // GRPC_SERVER_H
