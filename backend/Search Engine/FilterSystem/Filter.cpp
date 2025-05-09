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
        m_dataBaseData.push_back(tempInstance);
    }

    cout << endl << "The data inside the 'm_dataBaseData' vector is:" << endl;
    for (auto& data : m_dataBaseData) {
        // if (data.getParagraph() == "work") {
            std::cout << "Paragraph: " << data.getParagraph() << ", URL: " << data.getWebsiteURL() << std::endl;
            cout << "There are '" << m_dataBaseData.size() << " many words in the 'm_dataBaseData' vector." << endl;
            cout << "The max size a vector can hold is: " << m_dataBaseData.max_size() << endl;
            // break;
        // }
    }

    // Free the statement when done.
    sqlite3_reset(stmt);
    sqlite3_finalize(stmt);
    sqlite3_close(DB);

    cout << endl;
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