#ifndef FILTER_H
#define FILTER_H

#include <iostream>
#include <unordered_map>
#include <vector>
#include <string>
#include "../../sqlite3.h"

using namespace std;

class FilterSystem {
    public:
    std::string m_paragraph{};
    std::string m_url{};
    std::string m_title{};
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
    std::string getWebsiteTitle();
    float getRank();

    // Setters
    void setParagraph(std::string paragraph);
    void setWebsiteURL(std::string url);
    void setWebsiteTitle(std::string title);
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