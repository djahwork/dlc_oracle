cmake_minimum_required(VERSION 3.16)

project(dlc_oracle LANGUAGES CXX)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Core)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Core)

find_package(Protobuf CONFIG REQUIRED)
find_package(gRPC CONFIG REQUIRED)

include_directories(
  /usr/local/include/grpcpp
  /usr/local/include            # cfd-core headers
  /usr/local/include/cfdcore
  /usr/local/include/cfddlc
)

link_directories(
  /usr/local/lib
)

add_executable(dlc_oracle
  main.cpp
  grpc_server.h grpc_server.cpp
  dlc_service.h dlc_service.cpp
  oracle.grpc.pb.cc oracle.pb.cc
  oracle.grpc.pb.h oracle.pb.h
)
target_link_libraries(
    dlc_oracle PRIVATE
    Qt${QT_VERSION_MAJOR}::Core
    gRPC::grpc++
    protobuf::libprotobuf
    cfd
    cfdcore
    cfddlc
)

target_include_directories(dlc_oracle PRIVATE ${Protobuf_INCLUDE_DIRS})

include(GNUInstallDirs)
install(TARGETS dlc_oracle
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
