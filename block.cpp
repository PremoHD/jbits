#include "block.h"
#include "crypto.h"

std::string calculate_hash(const Block& b) {
    return sha256(
        std::to_string(b.index) +
        b.prev_hash +
        std::to_string(b.timestamp) +
        std::to_string(b.nonce)
    );
}