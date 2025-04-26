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
    int numOfDocuments{};
    double m_termFrequency{};
    double m_queryTermFrequency{};
    double m_inverseDocumentFrequency{};
    double m_TFMultiplyIDF{};
    int m_documentCountContainingWord{};
    int m_duplicateWordCount{};
    std::vector<std::string> unwantedChars = {
    " ", "\t", "\n",  // Whitespace characters
    "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "{", "}", "[", "]", "|", "\\", ":", ";", "\"", "'", "<", ">", ",", ".", "?", "/",
    "\0", "\b", "\r"  // Control characters
    };
    FilterSystem() {};
    void loadDatabaseData();
    bool extractWordsFromString(const char* str);
    void computeSurveyQuestionsTFIDF();

    // Getters
    std::string getName();
    std::string getWebsiteURL();
    double getTermFrequency();
    double getQueryTermFrequency();
    double getInverseDocumentFrequency();
    int getDocumentCountContainingWord();
    double getTFMultiplyIDF();
    int getNumOfDocuments();
    int getDuplicateWordCount();

    // Setters
    void setName(std::string name);
    void setWebsiteURL(std::string url);
    void setTermFrequency(double termFrequency);
    void setQueryTermFrequency(double queryTermFrequency);
    void setInverseDocumentFrequency(double inverseDocumentFrequency);
    void setDocumentCountContainingWord(int numOfDocumentsContainingWord);
    void setTFMultiplyIDF(double TFMultiplyIDF);
    void setNumOfDocuments();
    void setDuplicateWordCount(int duplicateWordCount);

    // Vectors
    std::vector<FilterSystem> m_dataBaseData{};
    std::vector<FilterSystem> m_surveyQuestionAnwsers{};

    ~FilterSystem() {};
};
#endif