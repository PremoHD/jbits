#pragma once
#include "Block.h"
#include <string>

inline std::string multiHash(const Block& b, int salt = 0) {
    return std::to_string(std::hash<std::string>{}(b.hash + std::to_string(salt)));
}