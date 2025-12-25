#include "ledger.h"
#include "crypto.h"
#include <iostream>

int main() {
    std::cout << "Starting JBits agent...\n";

    std::string private_key = random256();
    std::cout << "Wallet private key: " << private_key << "\n";

    Ledger ledger;

    while (true) {
        ledger.mine();   // autonomous mining
    }
}