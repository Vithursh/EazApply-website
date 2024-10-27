#ifndef UTILITIES_H
#define UTILITIES_H

#include <iostream>
#include <unordered_map>
#include <vector>
#include <string>
#include <cctype> 
#include "sqlite/sqlite3.h"

using namespace std;

class Utilities {
    public:
    string toLowerCase(string description);
};
#endif