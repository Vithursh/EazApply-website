#include <iostream>
#include <string>
#include <cstring>
#include <sstream>
#include <fstream>
#include <regex>
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
    const char* statement = "SELECT Word.word, Document.URL FROM Association "
                      "INNER JOIN Word ON Association.termID = Word.WordID "
                      "INNER JOIN Document ON Association.docID = Document.DocumentID;";
    int rc = sqlite3_prepare_v2(DB, statement, -1, &stmt, nullptr);

    // Open the database
    if (sqlite3_open("/home/vithursh/Coding/EazApply/backend/File Data/website_data.db", &DB) != SQLITE_OK) {
        std::cerr << "Error opening database: " << sqlite3_errmsg(DB) << std::endl;
    }

    // Prepare the SQL statement
    if (sqlite3_prepare_v2(DB, statement, -1, &stmt, nullptr) != SQLITE_OK) {
        std::cerr << "Error preparing SQL statement: " << sqlite3_errmsg(DB) << std::endl;
        sqlite3_close(DB);
        throw "Code was stopped!!!";
    }

    // Loop through the results, a row at a time.
    while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
        FilterSystem tempInstance{};
        auto word = sqlite3_column_text(stmt, 0);
        std::string wordStr = reinterpret_cast<const char*>(word);
        tempInstance.setName(wordStr);
        auto url = sqlite3_column_text(stmt, 1);
        std::string urlStr = reinterpret_cast<const char*>(url);
        tempInstance.setWebsiteURL(urlStr);

        // Add it to 'm_dataBaseData'
        m_dataBaseData.push_back(tempInstance);
    }
    
    cout << "The data inside the 'm_dataBaseData' vector is:" << endl;
    for (auto& data : m_dataBaseData)
        std::cout << "Word: " << data.getName() << ", URL: " << data.getWebsiteURL() << std::endl;

    // Free the statement when done.
    sqlite3_reset(stmt);
    sqlite3_finalize(stmt);
    sqlite3_close(DB);

    cout << endl;
}

void FilterSystem::setName(std::string name) {
    m_name = name;
}

string FilterSystem::getName() {
    return m_name;
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
            auto it = std::find_if(unwantedChars.begin(), unwantedChars.end(), [word](const std::string &c) {
                return c == std::string(1, word[0]);
            });

            if (it == unwantedChars.end()) {
                item.setName(word);
                m_surveyQuestionAnwsers.push_back(item);  // Add each match to the vector 
            }
        }
    } else {
        FilterSystem item{};
        item.setName(strValue);
        m_surveyQuestionAnwsers.push_back(item);
    }

    cout << "Extracted words/phrases:" << endl;
    for (auto& items : m_surveyQuestionAnwsers) {
        cout << "Words in 'm_surveyQuestionAnwsers' is: " << items.getName() << endl;
    }

    return containsSpaces;
}

extern "C" {
    void receiveData(const char** companysize, int companysizeNum, const char** industriesexcitedin, int industriesexcitedinNum, const char** levelofexperience, int levelofexperienceNum, const char** liketowork, int liketoworkNum, const char** minimumexpectedsalary, int minimumexpectedsalaryNum, const char** rolesinterestedin, int rolesinterestedinNum, const char** skillsenjoyworkingwith, int skillsenjoyworkingwithNum, const char** valueinrole, int valueinroleNum) {
        cout << endl << "The clean data in the tables after sending it to C++:" << endl;
        
        FilterSystem instance;

        // Load data
        instance.loadDatabaseData();

        // Print companysize (1 element)
        cout << "The 'companysize' table" << endl;
        for (int i = 1; i < companysizeNum; i++) {
            if (strcmp(companysize[i], "NULL") != 0) {
                if (instance.extractWordsFromString(companysize[i])) {
                    cout << "There were spaces in the string" << endl;
                } else {
                    cout << "There were no spaces in the string" << endl;
                }
                cout << "companysize[" << i << "]: " << companysize[i] << endl;
            }
        }
        cout << endl;

        // Print industriesexcitedin (5 elements)
        cout << "The 'industriesexcitedin' table" << endl;
        for (int i = 1; i < industriesexcitedinNum; i++) {
            if (strcmp(industriesexcitedin[i], "NULL") != 0) {
                if (instance.extractWordsFromString(industriesexcitedin[i])) {
                    cout << "There were spaces in the string" << endl;
                } else {
                    cout << "There were no spaces in the string" << endl;
                }
                cout << "industriesexcitedin[" << i << "]: " << industriesexcitedin[i] << endl;
            }
        }
        cout << endl;

        // Print levelofexperience (2 elements)
        cout << "The 'levelofexperience' table" << endl;
        for (int i = 1; i < levelofexperienceNum; i++) {
            if (strcmp(levelofexperience[i], "NULL") != 0) {
                if (instance.extractWordsFromString(levelofexperience[i])) {
                    cout << "There were spaces in the string" << endl;
                } else {
                    cout << "There were no spaces in the string" << endl;
                }
                cout << "levelofexperience[" << i << "]: " << levelofexperience[i] << endl;
            }
        }
        cout << endl;

        // Print liketowork (2 elements)
        cout << "The 'liketowork' table" << endl;
        for (int i = 1; i < liketoworkNum; i++) {
            if (strcmp(liketowork[i], "NULL") != 0) {
                if (instance.extractWordsFromString(liketowork[i])) {
                    cout << "There were spaces in the string" << endl;
                } else {
                    cout << "There were no spaces in the string" << endl;
                }
                cout << "liketowork[" << i << "]: " << liketowork[i] << endl;
            }
        }
        cout << endl;

        // Print minimumexpectedsalary (1 element)
        cout << "The 'minimumexpectedsalary' table" << endl;
        for (int i = 1; i < minimumexpectedsalaryNum; i++) {
            if (strcmp(minimumexpectedsalary[i], "NULL") != 0) {
                if (instance.extractWordsFromString(minimumexpectedsalary[i])) {
                    cout << "There were spaces in the string" << endl;
                } else {
                    cout << "There were no spaces in the string" << endl;
                }
                cout << "minimumexpectedsalary[" << i << "]: " << minimumexpectedsalary[i] << endl;
            }
        }
        cout << endl;

        // Print rolesinterestedin (5 elements)
        cout << "The 'rolesinterestedin' table" << endl;
        for (int i = 1; i < rolesinterestedinNum; i++) {
            if (strcmp(rolesinterestedin[i], "NULL") != 0) {
                if (instance.extractWordsFromString(rolesinterestedin[i])) {
                    cout << "There were spaces in the string" << endl;
                } else {
                    cout << "There were no spaces in the string" << endl;
                }
                cout << "rolesinterestedin[" << i << "]: " << rolesinterestedin[i] << endl;
            }
        }
        cout << endl;

        // Print skillsenjoyworkingwith (15 elements)
        cout << "The 'skillsenjoyworkingwith' table" << endl;
        for (int i = 1; i < skillsenjoyworkingwithNum; i++) {
            if (strcmp(skillsenjoyworkingwith[i], "NULL") != 0) {
                if (instance.extractWordsFromString(skillsenjoyworkingwith[i])) {
                    cout << "There were spaces in the string" << endl;
                } else {
                    cout << "There were no spaces in the string" << endl;
                }
                cout << "skillsenjoyworkingwith[" << i << "]: " << skillsenjoyworkingwith[i] << endl;
            }
        }
        cout << endl;

        // Print valueinrole (3 elements)
        cout << "The 'valueinrole' table" << endl;
        for (int i = 1; i < valueinroleNum; i++) {
            if (strcmp(valueinrole[i], "NULL") != 0) {
                if (instance.extractWordsFromString(valueinrole[i])) {
                    cout << "There were spaces in the string" << endl;
                } else {
                    cout << "There were no spaces in the string" << endl;
                }
                cout << "valueinrole[" << i << "]: " << valueinrole[i] << endl;
            }
        }
    }
}