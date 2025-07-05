# Utiliser une image Ubuntu comme base
FROM ubuntu:22.04

# Installer les outils de base
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
    && apt-get clean

RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /usr/include/nlohmann
RUN wget https://github.com/nlohmann/json/releases/latest/download/json.hpp

# Créer le répertoire de travail pour l'application
WORKDIR /app

# Copier les fichiers du projet dans l'image Docker
COPY . /app

RUN git clone https://github.com/p2pderivatives/cfd-dlc.git && \
	rm ./cfd-dlc/CMakeLists.txt
COPY ./CMakeLists.txt /app/cfd-dlc

RUN cd cfd-dlc && \
    ./scripts/install_cfd.sh && \
    ./scripts/build.sh && \
    cd build && \
    make install

ENV LD_LIBRARY_PATH /usr/local/lib:$LD_LIBRARY_PATH

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

RUN git clone https://github.com/abseil/abseil-cpp.git
RUN cd abseil-cpp && \
    git checkout lts_2023_08_02 && \
    mkdir build && \
    cd build && \
    cmake .. -DCMAKE_POSITION_INDEPENDENT_CODE=ON -DCMAKE_BUILD_TYPE=Release && \
    make -j 4 && \
    make install
    
RUN git clone --recurse-submodules --depth=1 -b v1.58.0 https://github.com/grpc/grpc

RUN cd grpc && \ 
    mkdir -p cmake/build && \
    cd cmake/build && \ 
    cmake ../.. -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=/usr/local && \
    make -j 4 && \
    make install
    
RUN protoc -I=. --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` oracle.proto
RUN protoc -I=. --cpp_out=. oracle.proto

RUN g++ -c -std=c++17 -o oracle.o oracle.cpp -I/usr/local/include
RUN g++ -c -std=c++17 -o oracle.pb.o oracle.pb.cc -I/usr/local/include
RUN g++ -c -std=c++17 -o oracle.grpc.pb.o oracle.grpc.pb.cc -I/usr/local/include

RUN g++ -std=c++17 -o oracle oracle.o oracle.pb.o oracle.grpc.pb.o -L/usr/local/lib -lgrpc++ -lprotobuf -pthread -lgrpc -lgpr -labsl_base -labsl_synchronization -labsl_log_internal_check_op -labsl_log_internal_message -labsl_cord -labsl_cordz_info -labsl_cordz_functions -lcfd -lcfdcore -lcfddlc

RUN pip install grpcio grpcio-tools

RUN python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. oracle.proto

# Command to run the application
#CMD ["python", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD ["/bin/bash"]
