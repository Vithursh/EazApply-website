#ifndef INDEX_H
#define INDEX_H

#include <iostream>
#include <unordered_map>
#include <vector>
#include <string>

using namespace std;

class Index {

public:
    void indexDocument(int docID, string websiteLink);
    const std::vector<std::pair<int, int>>& search(const std::string& term) const;

private:
    std::unordered_map<std::string, std::vector<std::pair<int, int>>> index;
};

// Functions pyhton can access
extern "C" {
    void indexDocument(int docID, const char* websiteLink);
}

#endif // INDEXER_H