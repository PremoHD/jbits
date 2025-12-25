#include "ledger.h"
#include "crypto.h"
#include <ctime>
#include <iostream>

Ledger::Ledger() {
    Block genesis;
    genesis.index = 0;
    genesis.prev_hash = "0";
    genesis.timestamp = time(nullptr);
    genesis.nonce = 0;
    genesis.hash = sha256("genesis");
    chain.push_back(genesis);
}

void Ledger::mine() {
    Block b;
    b.index = chain.size();
    b.prev_hash = chain.back().hash;
    b.timestamp = time(nullptr);
    b.nonce = 0;

    while (true) {
        b.hash = sha256(
            std::to_string(b.index) +
            b.prev_hash +
            std::to_string(b.timestamp) +
            std::to_string(b.nonce)
        );
        if (b.hash.substr(0, 4) == "0000")
            break;
        b.nonce++;
    }

    chain.push_back(b);
    std::cout << "Mined block " << b.index
              << " hash=" << b.hash << std::endl;
}