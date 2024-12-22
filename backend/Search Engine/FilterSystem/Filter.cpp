#include <iostream>
#include <string>
#include <cstring>
#include <sstream>
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

        // Calculates the term frequency
        if (!m_dataBaseData.empty()) {
            bool found = false;
            // Find and update existing instance
            for (auto& entry : m_dataBaseData) {
                if (entry.getName() == tempInstance.getName() && entry.getWebsiteURL() == tempInstance.getWebsiteURL()) {
                    entry.setTermFrequency(entry.getTermFrequency() + 1);
                    found = true;
                    break;
                }
            }

            // If word not found, add new instance
            if (!found) {
                tempInstance.setTermFrequency(1);
                m_dataBaseData.push_back(tempInstance);
            }

        } else {
            // First entry
            tempInstance.setTermFrequency(1);
            m_dataBaseData.push_back(tempInstance);
        }
    }

    int numOfDocuments{}, numOfDocumentsContainingWord{};
    std::string document{};
    for (int i = 0; i < m_dataBaseData.size(); i++) {
        if (m_dataBaseData[i].getWebsiteURL() != m_dataBaseData[i+1].getWebsiteURL()) {
            // cout << "The different documents is: " << m_dataBaseData[i].getWebsiteURL() << endl;
            numOfDocuments++;
            i++;
        }
        
        // Count the number of documents containing the word
        for (size_t j = 0; j < i && j < m_dataBaseData.size(); j++) {
            document = "";
            if (m_dataBaseData[j].getName() == m_dataBaseData[i].getName() && document != m_dataBaseData[j].getWebsiteURL()) {
                document = m_dataBaseData[j].getWebsiteURL();
                m_dataBaseData[i].setDocumentCountContainingWord(m_dataBaseData[i].getDocumentCountContainingWord() + 1);
                cout << "Word '" << m_dataBaseData[i].getName() << "' found in document: " << m_dataBaseData[i].getWebsiteURL() << " (count: " << m_dataBaseData[i].getDocumentCountContainingWord() << ")" << endl;
            } else {
                // If the word is not found in any document (default value is 0)
                if (m_dataBaseData[i].getDocumentCountContainingWord() == 0) {
                    m_dataBaseData[i].setDocumentCountContainingWord(m_dataBaseData[i].getDocumentCountContainingWord() + 1);
                }
            }
        }
    }

    // Find the maximum number of documents containing the word
    for (size_t i = 0; i < m_dataBaseData.size(); i++) {
        for (size_t j = 0; j < i && j < m_dataBaseData.size(); j++) {
            if (m_dataBaseData[j].getName() == m_dataBaseData[i].getName()) {
                if (m_dataBaseData[j].getName() == m_dataBaseData[i].getName() && m_dataBaseData[j].getDocumentCountContainingWord() > m_dataBaseData[i].getDocumentCountContainingWord()) {
                    m_dataBaseData[i].setDocumentCountContainingWord(m_dataBaseData[j].getDocumentCountContainingWord());
                } else {
                    m_dataBaseData[j].setDocumentCountContainingWord(m_dataBaseData[i].getDocumentCountContainingWord());
                }
            }
        }
    }

    // cout << "The size is: " << numOfDocuments << endl;

    // Calculate the inverse document frequency and TF * IDF
    for (auto& entry : m_dataBaseData) {
        // Prevent division by zero
        double docCount = entry.getDocumentCountContainingWord();
        
        if (docCount <= 0) {
            // Safety: minimum value of 1 as default
            docCount = 1;
        }

        cout << "The document count for '" << entry.getName() << "' is: " << docCount << endl;

        // Calculate the inverse document frequency
        double idf = 1 + log(numOfDocuments / docCount);
        entry.setInverseDocumentFrequency(idf);
        
        // Calculate the TF * IDF
        entry.setTFMultiplyIDF(entry.getTermFrequency() * idf);
    }
    
    cout << endl << "The data inside the 'm_dataBaseData' vector is:" << endl;
    for (auto& data : m_dataBaseData) {
        std::cout << "Word: " << data.getName() << ", URL: " << data.getWebsiteURL() << ", Term Frequency: " << data.getTermFrequency() << ", Inverse Document Frequency: " << data.getInverseDocumentFrequency() << ", TF * IDF: " << data.getTFMultiplyIDF() << std::endl;
    }

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

void FilterSystem::setTermFrequency(double termFrequency) {
    int numOfWordInDocument{};
    sqlite3_stmt *stmt{};
    sqlite3* DB{};
    const char* statement = "SELECT COUNT(Document.URL), Document.URL FROM Association "
                        "INNER JOIN Document ON Association.docID = Document.DocumentID "
                        "WHERE Document.URL = ?;";
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

    if (sqlite3_bind_text(stmt, 1, m_url.c_str(), -1, SQLITE_STATIC) != SQLITE_OK) {
        std::cerr << "Error binding value: " << sqlite3_errmsg(DB) << std::endl;
        sqlite3_finalize(stmt);
        sqlite3_close(DB);
        throw "Code was stopped!!!";
    }

    // Loop through the results, a row at a time.
    while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
        numOfWordInDocument = sqlite3_column_int(stmt, 0);
        // std::cout << "Number of occurrences: " << numOfWordInDocument << std::endl;
    }

    // Free the statement when done.
    sqlite3_reset(stmt);
    sqlite3_finalize(stmt);
    sqlite3_close(DB);

    // for (auto& entry : m_dataBaseData) {
    //     if (entry.getWebsiteURL() == m_url) {
    //         numOfWordInDocument++;
    //     }
    // }

    // cout << "The number of words in the document " << m_url << " is: " << numOfWordInDocument << endl;
    m_termFrequency = termFrequency / numOfWordInDocument;
}

double FilterSystem::getTermFrequency() {
    return m_termFrequency;
}

void FilterSystem::setInverseDocumentFrequency(double inverseDocumentFrequency) {
    m_inverseDocumentFrequency = inverseDocumentFrequency;
}

double FilterSystem::getInverseDocumentFrequency() {
    return m_inverseDocumentFrequency;
}

void FilterSystem::setTFMultiplyIDF(double TFMultiplyIDF) {
    m_TFMultiplyIDF = TFMultiplyIDF;
}

void FilterSystem::setDocumentCountContainingWord(int numOfDocumentsContainingWord) {
    m_documentCountContainingWord = numOfDocumentsContainingWord;
}

int FilterSystem::getDocumentCountContainingWord() {
    return m_documentCountContainingWord;
}

double FilterSystem::getTFMultiplyIDF() {
    return m_TFMultiplyIDF;
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