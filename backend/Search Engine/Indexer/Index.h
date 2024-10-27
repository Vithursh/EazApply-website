#ifndef INDEX_H
#define INDEX_H

#include <iostream>
#include <unordered_map>
#include <vector>
#include <string>
#include "Utilities.h"
#include "sqlite/sqlite3.h"

using namespace std;

class Index {

public:
    void indexDocument(string websiteLink);
    const std::vector<std::pair<int, int>>& search(const std::string& term) const;

    void executeSQLFile(sqlite3* DB, int rc);
    
    void insertData(sqlite3* DB, int rc, int WordID, string word, int DocumentID, string URL, int termID, int docID, int position);

    bool checkWordExists(sqlite3* DB, int rc, string word);

    int getWordId(sqlite3* DB, int rc, string word);
    Utilities utilities{};

private:
    std::unordered_map<std::string, std::vector<std::pair<int, int>>> index;
};

// Functions pyhton can access
extern "C" {
    void indexDocument(const char* websiteLink);
}

#endif // INDEXER_H