#pragma once
#include <string>

struct Block {
    int index;
    std::string prevHash;
    std::string data;
    std::string hash;
};