#pragma once
#include <vector>
#include <map>
#include "Block.h"
#include "Branch.h"

enum class NodeType { FULL, LIGHT, VALIDATOR };

struct Node {
    NodeType type;
    std::vector<Block> ledger;
    std::map<std::string, Branch> branches;
};