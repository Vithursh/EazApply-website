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
    std::string m_url{};
    // int m_termFrequency{};
    // int m_inverseDocumentFrequency{};
    // int m_TFMultiplyIDF{}
    std::vector<std::string> unwantedChars = {
    " ", "\t", "\n",  // Whitespace characters
    "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "{", "}", "[", "]", "|", "\\", ":", ";", "\"", "'", "<", ">", ",", ".", "?", "/",
    "\0", "\b", "\r"  // Control characters
    };
    FilterSystem() {};
    void loadDatabaseData();
    bool extractWordsFromString(const char* str);

    // Getters
    std::string getName();
    std::string getWebsiteURL();
    int getTermFrequency();
    int getInverseDocumentFrequency();
    // int TFMultiplyIDF();

    // Setters
    void setName(std::string name);
    void setWebsiteURL(std::string url);
    void setTermFrequency(std::string);
    void setInverseDocumentFrequency(std::string);
    // void TFMultiplyIDF();

    // Vectors
    std::vector<FilterSystem> m_dataBaseData{};
    std::vector<FilterSystem> m_surveyQuestionAnwsers{};

    ~FilterSystem() {};
};
#endif