#!/bin/bash

protoc -I=. --grpc_out=../src/ --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` ./oracle.proto
protoc -I=. --cpp_out=../src/ ./oracle.proto
python -m grpc_tools.protoc -I=. --python_out=../python_interface/ --grpc_python_out=../python_interface/ ./oracle.proto
