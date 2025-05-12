#include <iostream>
#include <string>
#include <cstring>
#include <sstream>
#include <algorithm>
#include <cctype>
#include <fstream>
#include <regex>
#include <cmath>
#include <cstdlib>
#include <typeinfo>
#include <stdlib.h>
#include <curl/curl.h>
#include <nlohmann/json.hpp>

// Imported files
#include "../../sqlite3.h"
#include "Filter.h"

using namespace std;

void FilterSystem::loadDatabaseData() {
    // Add all the words & URL from the database into the vector
    sqlite3_stmt *stmt{};
    sqlite3* DB{};

    const char* statement = "SELECT d.URL AS DocumentURL, p.Text AS Paragraph "
                      "FROM Association AS a "
                      "INNER JOIN Paragraph AS p ON a.ParagraphID = p.ParagraphID "
                      "INNER JOIN Document AS d ON a.DocumentID = d.DocumentID "
                      "ORDER BY d.URL;";

    // Open the database
    if (sqlite3_open("/home/vithursh/Coding/EazApply/backend/File Data/website_data.db", &DB) != SQLITE_OK) {
        std::cerr << "Error opening database: " << sqlite3_errmsg(DB) << std::endl;
    }

    cout << "Test to see where the code frezzes #1" << endl;
    int rc = sqlite3_prepare_v2(DB, statement, -1, &stmt, nullptr);

    // Prepare the SQL statement
    if (sqlite3_prepare_v2(DB, statement, -1, &stmt, nullptr) != SQLITE_OK) {
        std::cerr << "Error preparing SQL statement: " << sqlite3_errmsg(DB) << std::endl;
        sqlite3_close(DB);
        throw "Code was stopped!!!";
    }
    
    int count = 0;

    string usersSummary{};

    string env_variable = std::getenv("GEMINI_API_KEY");

    // Loop through the results, a row at a time.
    while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
        cout << "This code was run: " << ++count << " number of times." << endl;
        // cout << "The number of documents is: " << getNumOfDocuments() << endl;
        // rowsFetched++;
        FilterSystem tempInstance{};
        auto url = sqlite3_column_text(stmt, 0);
        std::string urlStr = reinterpret_cast<const char*>(url);
        tempInstance.setWebsiteURL(urlStr);
        auto paragraph = sqlite3_column_text(stmt, 1);
        std::string paragraphStr = reinterpret_cast<const char*>(paragraph);
        tempInstance.setParagraph(paragraphStr);
        // tempInstance.setRank(cosine_similarity(embedText(env_variable, paragraphStr), embedText(env_variable, usersSummary)));
        auto emb = embedText(env_variable, paragraphStr);
        for (const auto& val : emb) {
            std::cout << val << " ";
        }
        m_dataBaseData.push_back(tempInstance);
    }

    cout << endl << "The data inside the 'm_dataBaseData' vector is:" << endl;
    cout << "The max size a vector can hold is: " << m_dataBaseData.max_size() << endl;
    for (auto& data : m_dataBaseData) {
        // if (data.getParagraph() == "work") {
            std::cout << "Paragraph: " << data.getParagraph() << ", URL: " << data.getWebsiteURL() << std::endl;
            cout << "There are '" << m_dataBaseData.size() << " many words in the 'm_dataBaseData' vector." << endl;
            // break;
        // }
    }

    // Free the statement when done.
    sqlite3_reset(stmt);
    sqlite3_finalize(stmt);
    sqlite3_close(DB);

    cout << endl;
}

// Callback to collect response data into a std::string
size_t FilterSystem::WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    size_t total = size * nmemb;
    static_cast<std::string*>(userp)->append(static_cast<char*>(contents), total);
    return total;
}

std::vector<float> FilterSystem::embedText(const std::string& apiKey, const std::string& text) {
    // 1) Correct URL
    std::string url =
      "https://generativelanguage.googleapis.com/v1beta/models/"
      "text-embedding-004:embedContent?key=" + apiKey;

    // 2) Build the proper JSON body
    nlohmann::json reqBody = {
      {"content", {
         {"parts", nlohmann::json::array({
            {{"text", text}}
         })}
      }}
    };
    std::string reqStr = reqBody.dump();

    // 3) Send the POST via libcurl
    std::string response;
    CURL* curl = curl_easy_init();
    struct curl_slist* hdrs = nullptr;
    hdrs = curl_slist_append(hdrs, "Content-Type: application/json");

    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, hdrs);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, reqStr.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);

    CURLcode res = curl_easy_perform(curl);
    curl_slist_free_all(hdrs);
    curl_easy_cleanup(curl);
    if (res != CURLE_OK) {
      throw std::runtime_error("cURL error: " + std::string(curl_easy_strerror(res)));
    }

    // 4) Parse out the embedding values
    auto j = nlohmann::json::parse(response);
    if (!j.contains("embedding") || !j["embedding"].contains("values")) {
      throw std::runtime_error("Unexpected response format: " + response);
    }
    auto& vals = j["embedding"]["values"];
    std::vector<float> embedding;
    embedding.reserve(vals.size());
    for (auto& v : vals) embedding.push_back(v.get<float>());

    return embedding;
}

float FilterSystem::cosine_similarity(const std::vector<float>& a, const std::vector<float>& b) {
    if (a.size() != b.size()) {
        throw std::invalid_argument("Vectors must be the same length");
    }

    float dot = 0.0f;
    float normA = 0.0f;
    float normB = 0.0f;
    for (size_t i = 0; i < a.size(); ++i) {
        dot   += a[i] * b[i];
        normA += a[i] * a[i];
        normB += b[i] * b[i];
    }

    if (normA == 0.0f || normB == 0.0f) {
        // One of the vectors is zero-length; cosine similarity is undefined.
        // Here we choose to return 0.0f, but you could also throw or return NaN.
        return 0.0f;
    }

    return dot / (std::sqrt(normA) * std::sqrt(normB));
}

void FilterSystem::setParagraph(std::string paragraph) {
    m_paragraph = paragraph;
}

string FilterSystem::getParagraph() {
    return m_paragraph;
}

void FilterSystem::setWebsiteURL(std::string url) {
    m_url = url;
}

string FilterSystem::getWebsiteURL() {
    return m_url;
}

void FilterSystem::setRank(float rank) {
    m_rank = rank;
}

float FilterSystem::getRank() {
    return m_rank;
}

bool FilterSystem::extractWordsFromString(const char* str) {
    bool containsSpaces = false;
    string strValue(str);
    string word{};
    // making a string stream
    stringstream iss(str);
    // Check if the string conatins atleast one space
    size_t pos = strValue.find(' ');
    if (pos != string::npos) {
        containsSpaces = true;    
        // Read and print each word.
        while (iss >> word) {
            FilterSystem item{};
            // Check if the word contains any unwanted characters
            auto it = std::find_if(unwantedChars.begin(), unwantedChars.end(), [word](const std::string &c) {
                return c == std::string(1, word[0]);
            });

            // If the word does not contain any unwanted characters, add it to the vector
            if (it == unwantedChars.end()) {
                item.setParagraph(word);
                m_surveyQuestionAnwsers.push_back(item);  // Add each match to the vector 
            }
        }
    } else {
        FilterSystem item{};
        item.setParagraph(strValue);
        m_surveyQuestionAnwsers.push_back(item);
    }

    return containsSpaces;
}

extern "C" {
    void receiveData(const char** companysize, int companysizeNum, const char** industriesexcitedin, int industriesexcitedinNum, const char** levelofexperience, int levelofexperienceNum, const char** liketowork, int liketoworkNum, const char** minimumexpectedsalary, int minimumexpectedsalaryNum, const char** rolesinterestedin, int rolesinterestedinNum, const char** skillsenjoyworkingwith, int skillsenjoyworkingwithNum, const char** valueinrole, int valueinroleNum) {
        cout << endl << "The clean data in the tables after sending it to C++:" << endl;
        
        FilterSystem instance;

        // Load data
        instance.loadDatabaseData();
    }
}