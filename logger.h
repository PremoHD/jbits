#pragma once
#include <string>

void log_event(
    const std::string& type,
    const std::string& key,
    int height,
    const std::string& hash,
    long nonce,
    long reward
);