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
    std::string m_paragraph{};
    std::string m_url{};
    float m_rank{};
    std::vector<std::string> unwantedChars = {
    " ", "\t", "\n",  // Whitespace characters
    "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "{", "}", "[", "]", "|", "\\", ":", ";", "\"", "'", "<", ">", ",", ".", "?", "/",
    "\0", "\b", "\r"  // Control characters
    };
    FilterSystem() {};
    void loadDatabaseData();
    std::string getUserSummary(const std::string& userEmail);
    bool extractWordsFromString(const char* str);

    // Getters
    std::string getParagraph();
    std::string getWebsiteURL();
    float getRank();

    // Setters
    void setParagraph(std::string paragraph);
    void setWebsiteURL(std::string url);
    void setRank(float rank);

    // Vectors
    std::vector<FilterSystem> m_dataBaseData{};
    std::vector<FilterSystem> m_surveyQuestionAnwsers{};

    std::vector<float> embedText(const std::string& apiKey, const std::string& text);
    static size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp);
    float cosine_similarity(const std::vector<float>& a, const std::vector<float>& b);

    ~FilterSystem() {};
};
#endif