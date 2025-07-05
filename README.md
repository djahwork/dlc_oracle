# DLC Oracle

This project implements a gRPC-based oracle service for use with Discreet Log Contracts (DLCs). It includes integration with the `cfd-dlc` library and can be used with both C++ and Python gRPC clients.

## Manual Setup Guide (Without Docker)

Follow the steps below to build and run this project manually on a Linux system.

---

### ✅ Prerequisites

Install required packages:

```bash
sudo apt update
sudo apt install -y \
  build-essential cmake git wget curl unzip pkg-config \
  libssl-dev libtool autoconf automake \
  python3 python3-pip python3-setuptools \
  protobuf-compiler
```

---

### 📅 Clone the Project

```bash
git clone --recurse-submodules https://github.com/djahwork/dlc_oracle.git
cd dlc_oracle
```

---

### ⚙️ Install nlohmann JSON

```bash
sudo mkdir -p /usr/include/nlohmann
sudo wget -O /usr/include/nlohmann/json.hpp https://github.com/nlohmann/json/releases/latest/download/json.hpp
```

---

### 📦 Install `cfd-dlc`

```bash
git clone https://github.com/p2pderivatives/cfd-dlc.git
rm ./cfd-dlc/CMakeLists.txt
cp ./CMakeLists.txt ./cfd-dlc/

cd cfd-dlc
./scripts/install_cfd.sh
./scripts/build.sh
cd build
sudo make install
cd ../..
```

Export library path:

```bash
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
```

To make it persistent:

```bash
echo 'export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
```

---

### 🗃️ Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

---

### 🧱 Build Abseil C++

```bash
git clone https://github.com/abseil/abseil-cpp.git
cd abseil-cpp
git checkout lts_2023_08_02
mkdir build && cd build
cmake .. -DCMAKE_POSITION_INDEPENDENT_CODE=ON -DCMAKE_BUILD_TYPE=Release
make -j4
sudo make install
cd ../..
```

---

### 🔌 Build gRPC & Protobuf from Source

```bash
git clone --recurse-submodules --depth=1 -b v1.58.0 https://github.com/grpc/grpc
cd grpc
mkdir -p cmake/build
cd cmake/build
cmake ../.. -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=/usr/local
make -j4
sudo make install
cd ../../..
```

---

### 📆 Generate gRPC Code from `.proto`

```bash
protoc -I=proto --grpc_out=. --plugin=protoc-gen-grpc=$(which grpc_cpp_plugin) proto/oracle.proto
protoc -I=proto --cpp_out=. proto/oracle.proto
```

---

### ⚒️ Build the gRPC Code


```bash
g++ -std=c++17 -c -o oracle.pb.o proto/oracle.pb.cc -I/usr/local/include
g++ -std=c++17 -c -o oracle.grpc.pb.o proto/oracle.grpc.pb.cc -I/usr/local/include
```

---

### 🚀 Python gRPC (Optional)

Install Python packages:

```bash
pip install grpcio grpcio-tools
```

Generate Python gRPC stubs:

```bash
python3 -m grpc_tools.protoc -I=proto --python_out=. --grpc_python_out=. proto/oracle.proto
```

---
