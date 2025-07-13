#include "grpc_server.h"
#include "dlc_service.h"
#include <grpcpp/ext/proto_server_reflection_plugin.h>

#include <grpcpp/server_builder.h>
#include <iostream>
//#include <thread>

GrpcServer::GrpcServer(const std::string& addr, QObject* parent)
    : QObject(parent), address_(addr) {}

GrpcServer::~GrpcServer() { stop(); }

bool GrpcServer::start() {
    grpc::reflection::InitProtoReflectionServerBuilderPlugin();

    grpc::ServerBuilder builder;
    builder.AddListeningPort(address_, grpc::InsecureServerCredentials());

    // Register your service(s)
    auto dlc_service = std::make_unique<DlcService>();
    builder.RegisterService(dlc_service.get());         // ownership kept by server

    server_ = builder.BuildAndStart();
    if (!server_) {
        std::cerr << "Failed to start gRPC server on " << address_ << '\n';
        return false;
    }

    std::cout << "gRPC server listening on " << address_ << std::endl;
    // Run server in a background thread so Qt event‑loop continues.
    //std::thread([s = server_.get()] { s->Wait(); }).detach();
    server_->Wait();
    return true;
}

void GrpcServer::stop() {
    if (server_) server_->Shutdown();
}
