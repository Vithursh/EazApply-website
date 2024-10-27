#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <cstdlib>
#include "sqlite/sqlite3.h"
#include "Utilities.h"

using namespace std;

string Utilities::toLowerCase(string description) {
    std::string finalDesc{};
    
    for (size_t i = 0; i < description.length(); i++) {  // Use size() instead of strlen()
        if (description[i] == ' ') {
            // if (i + 1 < description.size()) {  // Check if there's a next character
                char temp = tolower(description[i + 1]);
                finalDesc += ' ';  // Keep the space
                finalDesc += temp; // Add the uppercase next character
                i++; // Skip the next character since it's already processed
            // }
        } else if (description[i] == description[0]) {
            char temp = tolower(description[0]);
            finalDesc += temp;
        } else {
            finalDesc += description[i];  // Add non-space characters as is
        }
    }
    
    return finalDesc;
}