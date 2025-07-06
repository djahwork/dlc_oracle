# Use Ubuntu
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    build-essential \
    autoconf \
    automake \
    python3 \
    python3-pip \
    libtool \
    pkg-config \
    libssl-dev \
    libboost-all-dev \
    git \
    libcurl4-openssl-dev \
    wget \
    curl \
    nano \
    unzip \
    protobuf-compiler \
    libprotobuf-dev \
    qtbase5-dev \
    qtbase5-dev-tools \
    qt6-base-dev \
    qt6-tools-dev \
    qt6-tools-dev-tools \
    && apt-get clean

RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /usr/include/nlohmann
RUN wget https://github.com/nlohmann/json/releases/latest/download/json.hpp

WORKDIR /app

COPY . /app

RUN git clone https://github.com/p2pderivatives/cfd-dlc.git && \
	rm ./cfd-dlc/CMakeLists.txt
COPY docker/CMakeLists.txt /app/cfd-dlc

RUN cd cfd-dlc && \
    ./scripts/install_cfd.sh && \
    ./scripts/build.sh && \
    cd build && \
    make install

ENV LD_LIBRARY_PATH /usr/local/lib:$LD_LIBRARY_PATH

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r api/requirements.txt

RUN git clone https://github.com/abseil/abseil-cpp.git
RUN cd abseil-cpp && \
    git checkout lts_2023_08_02 && \
    mkdir build && \
    cd build && \
    cmake .. -DCMAKE_POSITION_INDEPENDENT_CODE=ON -DCMAKE_BUILD_TYPE=Release && \
    make -j 4 && \
    make install
    
RUN git clone -b v1.58.0 https://github.com/grpc/grpc && \
    cd grpc && \
    git submodule update --init --recursive

RUN cd grpc && \ 
    mkdir -p cmake/build && \
    cd cmake/build && \ 
    cmake ../.. -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=/usr/local && \
    make -j 4 && \
    make install
    
RUN protoc -I=proto/ --grpc_out=src/ --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` proto/oracle.proto
RUN protoc -I=proto/ --cpp_out=src/ proto/oracle.proto
   
# Create build directory and build with CMake
RUN mkdir -p build && cd build && \
    cmake .. && \
    make -j4

RUN pip install grpcio grpcio-tools

RUN python -m grpc_tools.protoc -I=proto/ --python_out=api/ --grpc_python_out=api/ proto/oracle.proto

# Command to run the application
#CMD ["python", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD ["/bin/bash"]
