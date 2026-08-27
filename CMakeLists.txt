cmake_minimum_required(VERSION 3.10)
project(jbits)

set(CMAKE_CXX_STANDARD 17)

add_executable(jbits
    src/main.cpp
    src/crypto.cpp
    src/block.cpp
    src/ledger.cpp
)