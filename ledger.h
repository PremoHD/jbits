#pragma once
#include "block.h"
#include <vector>

class Ledger {
public:
    Ledger();
    void mine();
private:
    std::vector<Block> chain;
};