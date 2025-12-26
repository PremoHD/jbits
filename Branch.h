#pragma once
#include <vector>
#include "Block.h"

struct Branch {
    std::string id;
    std::vector<Block> blocks;
};