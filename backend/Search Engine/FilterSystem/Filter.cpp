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
#include <thread>
#include <chrono>
#include <curl/curl.h>
#include <nlohmann/json.hpp>
#include <pybind11/embed.h>
#include <pybind11/stl.h>  // Enable conversion for STL containers
#include <Python.h>

// Imported files
#include "../../sqlite3.h"
#include "Filter.h"

using namespace std;

void FilterSystem::loadDatabaseData(string userId) {
    // Add all the words & URL from the database into the vector
    sqlite3_stmt *stmt{};
    sqlite3* DB{};

    const char* statement = "SELECT d.URL AS DocumentURL, p.Text AS Paragraph, d.Title "
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

    string env_variable = std::getenv("GEMINI_API_KEY");
    string userSummary = getUserSummary(userId);

    // Loop through the results, a row at a time.
    while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
        cout << "This code was run: " << ++count << " number of times." << endl;
        // rowsFetched++;
        FilterSystem tempInstance{};
        auto url = sqlite3_column_text(stmt, 0);
        std::string urlStr = reinterpret_cast<const char*>(url);
        tempInstance.setWebsiteURL(urlStr);
        auto paragraph = sqlite3_column_text(stmt, 1);
        std::string paragraphStr = reinterpret_cast<const char*>(paragraph);
        tempInstance.setParagraph(paragraphStr);
        auto title = sqlite3_column_text(stmt, 2);
        std::string titleStr = reinterpret_cast<const char*>(title);
        tempInstance.setWebsiteTitle(titleStr);
        if (count % 5 == 0 && count != 0) {
            std::cout << "Sleeping for 1 minute..." << std::endl;
            std::this_thread::sleep_for(std::chrono::seconds(20));
            if (userSummary.empty()) {
                cout << "The user summary is: [" << userSummary << "]" << endl;
                throw std::runtime_error("User summary is empty. Cannot compute cosine similarity.");
            } else if (paragraphStr.empty()) {
                throw std::runtime_error("Paragraph is empty. Cannot compute cosine similarity.");
            } else {
                std::cout << "Computing cosine similarity..." << std::endl;
                tempInstance.setRank(cosine_similarity(embedText(env_variable, userSummary), embedText(env_variable, paragraphStr)));
            }
            std::cout << "Awake now!" << std::endl;
        }
        // auto emb = embedText(env_variable, paragraphStr);
        // for (const auto& val : emb) {
            // std::cout << val << " ";
        // }
        // std::cout << "The user summary is: " << getUserSummary("Someone123@gmail.com") << std::endl;
        m_dataBaseData.push_back(tempInstance);
    }

    // namespace py = pybind11;
    // py::gil_scoped_acquire gil;
    // py::scoped_interpreter guard{};
    // if (!Py_IsInitialized()) {
        // py::initialize_interpreter();
    // }
    // std::vector<std::vector<std::string>> dataSent{};

    // cout << endl << "The data inside the 'm_dataBaseData' vector is:" << endl;
    // cout << "The max size a vector can hold is: " << m_dataBaseData.max_size() << endl;
    // for (auto& data : m_dataBaseData) {
        // std::cout << "Paragraph: " << data.getParagraph() << ", URL: " << data.getWebsiteURL() << ", Rank: " << data.getRank() << std::endl << std::endl << std::endl;
        // cout << "There are '" << m_dataBaseData.size() << " many words in the 'm_dataBaseData' vector." << endl;
        // std::vector <std::string> rowData{};
        // rowData.push_back(data.getWebsiteURL());
        // rowData.push_back(data.getParagraph());
        // // rowData.push_back(data.getRank());
        // dataSent.push_back(rowData);
    // }

    // Sort data based on rank in descending order
    std::sort(m_dataBaseData.begin(), m_dataBaseData.end(), [](FilterSystem& a, FilterSystem& b) {
        return a.getRank() > b.getRank();
    });

    // Write data to csv file
    std::ofstream outputFile;
    outputFile.open("/home/vithursh/Coding/EazApply/backend/File Data/job_data.csv", std::ios::out); // Open for writing, overwrite if exists

    if (outputFile.is_open()) {
        // Write header if it's a new file or you want to ensure it's there
        outputFile << "Rank" << "," << "URL" << "," << "Paragraph" << "," << "Title" << std::endl;

        // Write some data
        for (auto& data : m_dataBaseData) {
            if (data.getRank() > 0.0)
                outputFile << data.getRank() << "|" << data.getWebsiteURL() << "|" << data.getParagraph() << "|" << data.getWebsiteTitle() << std::endl;
        }
        
        outputFile.close();
        std::cout << "Data successfully written to my_data.csv" << std::endl;
    } else {
        std::cerr << "Error opening file!" << std::endl;
    }

    // py::module_ sys = py::module_::import("sys");
    // // std::cout << "Python executable: " << std::string(py::str(sys.attr("executable"))) << std::endl;
    // sys.attr("path").attr("insert")(0, "/home/vithursh/Coding/EazApply/backend");

    // py::module_ builtins = py::module_::import("clean");
    // // std::string name = "Vithursh";
    // py::object receive_job_data_function = builtins.attr("receiveJobData");
    // // builtins.attr("receiveJobData");

    // receive_job_data_function();

    // Free the statement when done.
    sqlite3_reset(stmt);
    sqlite3_finalize(stmt);
    sqlite3_close(DB);

    cout << endl;
}

std::string FilterSystem::getUserSummary(const std::string& userId) {
    CURL* curl = curl_easy_init();
    std::string response;

    const std::string& supabaseUrl = std::getenv("VITE_SUPABASE_URL");
    const std::string& supabaseKey = std::getenv("VITE_SUPABASE_ANON_KEY");

    cout << "Supabase URL: " << supabaseUrl << endl;
    cout << "Supabase Key: " << supabaseKey << endl;
    
    if (!curl) {
        throw std::runtime_error("Failed to initialize CURL");
    }

    try {
        // Construct the API URL to only get the summary field
        std::string url = supabaseUrl + "/rest/v1/users?select=summary&user_id=eq." + userId;
        
        // Set up Supabase headers
        struct curl_slist* headers = nullptr;
        headers = curl_slist_append(headers, ("apikey: " + supabaseKey).c_str());
        headers = curl_slist_append(headers, ("Authorization: Bearer " + supabaseKey).c_str());
        
        // Configure CURL
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);
        
        // Perform request
        CURLcode res = curl_easy_perform(curl);
        
        // Clean up
        // curl_slist_free_all(headers);
        // curl_easy_cleanup(curl);
        
        if (res != CURLE_OK) {
            throw std::runtime_error("CURL request failed: " + std::string(curl_easy_strerror(res)));
        }
        
        // Parse JSON response to get just the summary field
        auto jsonResponse = nlohmann::json::parse(response);

        if (jsonResponse.is_object()) {
            if (jsonResponse.contains("summary")) {
                cout << "Summary found in JSON object." << endl;
                return jsonResponse["summary"].get<std::string>();
            } else {
                // This is where your code was likely falling through!
                cout << "It's an object, but 'summary' key is missing." << endl;
                cout << "Keys found: " << jsonResponse.dump() << endl; 
            }
        } 
        else if (jsonResponse.is_array() && !jsonResponse.empty()) {
            if (jsonResponse[0].contains("summary")) {
                cout << "Summary found in JSON array." << endl;
                
                // Check if the value is actually null in the database
                if (jsonResponse[0]["summary"].is_null()) {
                    cout << "The summary field exists but it is NULL in the database." << endl;
                    return "";
                }

                auto summaryValue = jsonResponse[0]["summary"].get<std::string>();
                
                // ADD THIS LINE:
                cout << "Summary content: [" << summaryValue << "]" << endl;
                
                return jsonResponse[0]["summary"].get<std::string>();
            }
        }
        else if (jsonResponse.is_string()) {
            // Maybe the API returned the summary directly as a raw string?
            cout << "Summary found as a raw string." << endl;
            return jsonResponse.get<std::string>();
        }
        
        // Log the actual type to find the culprit
        cerr << "Error: Received unexpected JSON type: " << jsonResponse.type_name() << endl;
        return ""; // or throw an exception
        
    } catch (const std::exception& e) {
        if (curl) curl_easy_cleanup(curl);
        throw std::runtime_error("Error fetching user summary: " + std::string(e.what()));
    }
}

// Callback to collect response data into a std::string
size_t FilterSystem::WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    size_t total = size * nmemb;
    static_cast<std::string*>(userp)->append(static_cast<char*>(contents), total);
    return total;
}

std::vector<float> FilterSystem::embedText(const std::string& apiKey, const std::string& text) {
    // 1) Correct URL
    std::string url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key=" + apiKey;

    // std::string url =
    // "https://generativelanguage.googleapis.com/v1beta/models/"
    // "gemini-embedding-exp-03-07:embedContent?key=" + apiKey;

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

void FilterSystem::setWebsiteTitle(std::string title) {
    m_title = title;
}

string FilterSystem::getWebsiteTitle() {
    return m_title;
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

	FilterSystem filterInstance;

	void loadDatabaseData(const char* userId) {
		cout << "The data recived from c++ is: " << userId << endl;
		string userIdString = userId;
		filterInstance.loadDatabaseData(userIdString);
	}
}