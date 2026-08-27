#include "crypto.h"
#include <openssl/sha.h>
#include <sstream>
#include <iomanip>
#include <random>

std::string sha256(const std::string& input) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256((unsigned char*)input.c_str(), input.size(), hash);

    std::stringstream ss;
    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++)
        ss << std::hex << std::setw(2) << std::setfill('0') << (int)hash[i];

    return ss.str();
}

std::string random256() {
    std::random_device rd;
    std::stringstream ss;
    for (int i = 0; i < 32; i++)
        ss << std::hex << (rd() & 0xff);
    return ss.str();
}