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
    
    void insertData(sqlite3* DB, int rc, int ParagraphID, string paragraph, int DocumentID, string URL);

    int checkWordExists(sqlite3* DB, int rc, string word);

    // int Index::getTermFrequency(sqlite3* DB, int rc, string word);
    // void termFrequency();
    // int count{};
    // int termOccurrence{};
    // void update(sqlite3* DB, int rc, const string& word, int termOccurrence);
    Utilities utilities{};

private:
    std::unordered_map<std::string, std::vector<std::pair<int, int>>> index;
};

// Functions pyhton can access
extern "C" {
    void indexDocument(const char* websiteLink);
}

#endif // INDEXER_H