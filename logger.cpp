#include "logger.h"
#include <fstream>
#include <ctime>

void log_event(
    const std::string& type,
    const std::string& key,
    int height,
    const std::string& hash,
    long nonce,
    long reward
) {
    std::ofstream file("jbits_log.csv", std::ios::app);

    std::time_t now = std::time(nullptr);

    file
        << now << ","
        << type << ","
        << key << ","
        << height << ","
        << hash << ","
        << nonce << ","
        << reward
        << "\n";

    file.close();
}