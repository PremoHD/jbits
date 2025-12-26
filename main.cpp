#include <iostream>
#include "Block.h"
#include "Branch.h"
#include "NodeCore.h"
#include "MultiHash.h"

int main() {
    // Create a block
    Block b1{0, "0", "Genesis Block", "hash0"};
    
    // Create a branch and add block
    Branch mainBranch{"main"};
    mainBranch.blocks.push_back(b1);
    
    // Create a node
    Node node{NodeType::FULL};
    node.ledger.push_back(b1);
    node.branches["main"] = mainBranch;

    // Compute multi-hash
    std::string proof = multiHash(b1, 123);

    std::cout << "Block index: " << b1.index << "\n";
    std::cout << "Branch ID: " << mainBranch.id << "\n";
    std::cout << "Node ledger size: " << node.ledger.size() << "\n";
    std::cout << "Multi-hash: " << proof << "\n";

    return 0;
}