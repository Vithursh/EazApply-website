#ifndef FILTER_H
#define FILTER_H

#include <iostream>
#include <unordered_map>
#include <vector>
#include <string>
#include "../../sqlite3.h"

using namespace std;

extern "C" {
    void receiveData(const char** companysize, int companysizeNum, const char** industriesexcitedin, int industriesexcitedinNum, const char** levelofexperience, int levelofexperienceNum, const char** liketowork, int liketoworkNum, const char** minimumexpectedsalary, int minimumexpectedsalaryNum, const char** rolesinterestedin, int rolesinterestedinNum, const char** skillsenjoyworkingwith, int skillsenjoyworkingwithNum, const char** valueinrole, int valueinroleNum);
}

class FilterSystem {
    public:
    std::string m_name{};
    // int m_termFrequency{};
    // int m_inverseDocumentFrequency{};
    // int m_TFMultiplyIDF{}
    std::vector<std::string> unwantedChars = {
    " ", "\t", "\n",  // Whitespace characters
    "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "{", "}", "[", "]", "|", "\\", ":", ";", "\"", "'", "<", ">", ",", ".", "?", "/",
    "\0", "\b", "\r"  // Control characters
    };
    FilterSystem() {};
    bool extractWordsFromString(const char* str);

    // Getters
    std::string getName();
    int getTermFrequency();
    int getInverseDocumentFrequency();
    // int TFMultiplyIDF();

    // Setters
    void setName(std::string name);
    void setTermFrequency(std::string);
    void setInverseDocumentFrequency(std::string);
    // void TFMultiplyIDF();

    // Vectors
    std::vector<FilterSystem> filterSystem{};

    ~FilterSystem() {};
};
#endif