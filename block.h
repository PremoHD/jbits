#pragma once
#include <string>

struct Block {
    int index;
    std::string prev_hash;
    long timestamp;
    long nonce;
    std::string hash;
};