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

    /*
    const char* statement = "SELECT Word.word, Document.URL FROM Association "
                        "INNER JOIN Word ON Association.termID = Word.WordID "
                        "INNER JOIN Document ON Association.docID = Document.DocumentID "
                        "LIMIT ? OFFSET ?;";
    */

    const char* statement = "SELECT Word.word, Document.URL FROM Association "
                      "INNER JOIN Word ON Association.termID = Word.WordID "
                      "INNER JOIN Document ON Association.docID = Document.DocumentID;";

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

    // Set the number of documents
    setNumOfDocuments();

    // int batchSize = 10000;
    // int offset = 0;
    
    int count = 0;
    // bool isStopped = false;
    
    // while (isStopped == false) {
    //     cout << "Test to see where the code frezzes #2" << endl;
    //     sqlite3_prepare_v2(DB, statement, -1, &stmt, nullptr);
    //     sqlite3_bind_int(stmt, 1, batchSize);
    //     sqlite3_bind_int(stmt, 2, offset);

        // int rowsFetched = 0;
        // Loop through the results, a row at a time.
        while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
            cout << "This code was run: " << ++count << " number of times." << endl;
            // cout << "The number of documents is: " << getNumOfDocuments() << endl;
            // rowsFetched++;
            FilterSystem tempInstance{};
            auto word = sqlite3_column_text(stmt, 0);
            std::string wordStr = reinterpret_cast<const char*>(word);
            tempInstance.setName(wordStr);
            auto url = sqlite3_column_text(stmt, 1);
            std::string urlStr = reinterpret_cast<const char*>(url);
            tempInstance.setWebsiteURL(urlStr);

            // CREATE A NEW SETTERS AND GETTERS FOR CALCULATING THE NUMBER OF DUPLICATE WORDS IN A DOCUMENT THEN GET THE TF 
            // Calculates the term frequency
            if (!m_dataBaseData.empty()) {
                bool found = false;
                // Find and update existing instance(term frequency)
                for (auto& entry : m_dataBaseData) {
                    // Update the term frequency for words that occur mutiple times in a document
                    if (entry.getName() == tempInstance.getName() && entry.getWebsiteURL() == tempInstance.getWebsiteURL()) {
                        // cout << "The TF before adding more onto it: " << entry.getTermFrequency() << endl;
                        entry.setDuplicateWordCount(entry.getDuplicateWordCount() + 1);
                        found = true;
                        // cout << "Updating TF for existing word: " << entry.getTermFrequency() << endl;
                        break;
                    }
                }

                // If word not found, add new instance
                if (!found) {
                    tempInstance.setDuplicateWordCount(1);
                    m_dataBaseData.push_back(tempInstance);
                    // cout << "Adding new word with TF=1" << endl;
                }

            } else {
                // First entry
                tempInstance.setDuplicateWordCount(1);
                m_dataBaseData.push_back(tempInstance);
                // cout << "First entry with TF=1" << endl;
            }

            // cout << "TF for '" << tempInstance.getName() 
            // << "' in '" << tempInstance.getWebsiteURL() 
            // << "' is: " << tempInstance.getTermFrequency() << endl;

            // cout << "The word count for '" << tempInstance.getName() << "' is: " << tempInstance.getDuplicateWordCount() << endl;
        }

        // cout << "Processing batch: Offset = " << offset << ", Batch size = " << batchSize << endl;
        // sqlite3_finalize(stmt);
        // if (rowsFetched < batchSize) {
        //     offset += batchSize;
        //     isStopped = true;
        //     // break;
        // }
    // }

    int numOfDocumentsContainingWord{};
    std::string lastDocument{};

    // Count the number of different documents
    for (int i = 0; i < m_dataBaseData.size(); i++) {
        // Ex. Website1, Website2, Website1, Website3, Website2
        // numOfDocuments = 2
        // if (m_dataBaseData[i].getWebsiteURL() != m_dataBaseData[i+1].getWebsiteURL()) {
        //     // cout << "The different documents is: " << m_dataBaseData[i].getWebsiteURL() << endl;
        //     numOfDocuments++;
        //     i++;
        // }

        // Get the term frequency using the 'DuplicateWordCount' getters and setters
        // for (size_t j = 0; j <= i && j < m_dataBaseData.size(); j++) {  // Changed to <= to include current word
            // if (m_dataBaseData[i].getName() == m_dataBaseData[j].getName() && m_dataBaseData[i].getWebsiteURL() == m_dataBaseData[j].getWebsiteURL()) {
                // cout << "The TF before adding more onto it: " << entry.getTermFrequency() << endl;
                m_dataBaseData[i].setTermFrequency(m_dataBaseData[i].getDuplicateWordCount());
                cout << "TF for '" << m_dataBaseData[i].getName() 
                << "' in '" << m_dataBaseData[i].getWebsiteURL() 
                << "' is: " << m_dataBaseData[i].getTermFrequency() << endl;
                // found = true;
                // cout << "Updating TF for existing word: " << entry.getTermFrequency() << endl;
                // break;
            // }
        // }

        // Count the number of documents containing the word
        // lastDocument = "";
        for (size_t j = 0; j < i && j < m_dataBaseData.size(); j++) {
            if (m_dataBaseData[j].getName() == m_dataBaseData[i].getName() && lastDocument != m_dataBaseData[j].getWebsiteURL()) {
                lastDocument = m_dataBaseData[j].getWebsiteURL();
                m_dataBaseData[i].setDocumentCountContainingWord(m_dataBaseData[i].getDocumentCountContainingWord() + 1);
                cout << "Word '" << m_dataBaseData[i].getName() << "' found in document: " << m_dataBaseData[i].getWebsiteURL() << " (count: " << m_dataBaseData[i].getDocumentCountContainingWord() << ")" << endl;
            } else {
                // If the word is not found in any document (default value is 1)
                if (m_dataBaseData[i].getDocumentCountContainingWord() == 0) {
                    m_dataBaseData[i].setDocumentCountContainingWord(m_dataBaseData[i].getDocumentCountContainingWord() + 1);
                }
            }
        }
    }

    // All instances of the same word get the document count
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
        double idf = 1 + log(getNumOfDocuments() / docCount);
        entry.setInverseDocumentFrequency(idf);
        
        // Calculate the TF * IDF
        entry.setTFMultiplyIDF(entry.getTermFrequency() * idf);
    }

    cout << endl << "The data inside the 'm_dataBaseData' vector is:" << endl;
    for (auto& data : m_dataBaseData) {
        // if (data.getName() == "work") {
            std::cout << "Word: " << data.getName() << ", URL: " << data.getWebsiteURL() << ", Term Frequency: " << data.getTermFrequency() << ", Inverse Document Frequency: " << data.getInverseDocumentFrequency() << ", TF * IDF: " << data.getTFMultiplyIDF() << std::endl;
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

    cout << "The TF before calculating is: " << termFrequency << endl;
    cout << "The number of words in the document " << m_url << " is: " << numOfWordInDocument << endl;
    m_termFrequency = termFrequency / numOfWordInDocument;
}

double FilterSystem::getTermFrequency() {
    return m_termFrequency;
}

void FilterSystem::setQueryTermFrequency(double queryTermFrequency) {
    m_queryTermFrequency = queryTermFrequency;
}

double FilterSystem::getQueryTermFrequency() {
    return m_queryTermFrequency;
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

double FilterSystem::getTFMultiplyIDF() {
    return m_TFMultiplyIDF;
}

void FilterSystem::setDocumentCountContainingWord(int numOfDocumentsContainingWord) {
    m_documentCountContainingWord = numOfDocumentsContainingWord;
}

int FilterSystem::getDocumentCountContainingWord() {
    return m_documentCountContainingWord;
}

int FilterSystem::getNumOfDocuments() {
    return numOfDocuments;
}

void FilterSystem::setNumOfDocuments() {
    sqlite3_stmt *stmt{};
    sqlite3* DB{};
    const char* statement = "SELECT COUNT(URL) FROM Document;";
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
        numOfDocuments = sqlite3_column_int(stmt, 0);
    }

    // Free the statement when done.
    sqlite3_reset(stmt);
    sqlite3_finalize(stmt);
    sqlite3_close(DB);
}

int FilterSystem::getDuplicateWordCount() {
    return m_duplicateWordCount;
}

void FilterSystem::setDuplicateWordCount(int duplicateWordCount) {
    m_duplicateWordCount = duplicateWordCount;
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
                item.setName(word);
                m_surveyQuestionAnwsers.push_back(item);  // Add each match to the vector 
            }
        }
    } else {
        FilterSystem item{};
        item.setName(strValue);
        m_surveyQuestionAnwsers.push_back(item);
    }

    return containsSpaces;
}

void FilterSystem::computeSurveyQuestionsTFIDF() {
    // Calculate the survey questions term frequency
    for (size_t i = 0; i < m_surveyQuestionAnwsers.size(); i++) {
        double numOfDuplicateWords = 0.0;
        
        for (size_t j = 0; j <= i && j < m_surveyQuestionAnwsers.size(); j++) {  // Changed to <= to include current word
            if (m_surveyQuestionAnwsers[j].getName() == m_surveyQuestionAnwsers[i].getName()) {
                numOfDuplicateWords++;
            }
        }
        m_surveyQuestionAnwsers[i].setQueryTermFrequency(numOfDuplicateWords / m_surveyQuestionAnwsers.size());
    }

    int numOfDocumentsContainingWord{};
    std::string lastDocument{};

    // Count the number of documents containing the word
    for (int i = 0; i < m_surveyQuestionAnwsers.size(); i++) {
        for (size_t j = 0; j < i && j < m_dataBaseData.size(); j++) {
            // lastDocument = "";
            if (m_dataBaseData[j].getName() == m_surveyQuestionAnwsers[i].getName() && lastDocument != m_dataBaseData[j].getWebsiteURL()) {
                lastDocument = m_dataBaseData[j].getWebsiteURL();
                m_surveyQuestionAnwsers[i].setDocumentCountContainingWord(m_surveyQuestionAnwsers[i].getDocumentCountContainingWord() + 1);
                cout << "Word '" << m_surveyQuestionAnwsers[i].getName() << "' found in document: " << m_dataBaseData[i].getWebsiteURL() << " (count: " << m_surveyQuestionAnwsers[i].getDocumentCountContainingWord() << ")" << endl;
            } else {
                // If the word is not found in any document (default value is 0)
                if (m_surveyQuestionAnwsers[i].getDocumentCountContainingWord() == 0) {
                    m_surveyQuestionAnwsers[i].setDocumentCountContainingWord(m_surveyQuestionAnwsers[i].getDocumentCountContainingWord() + 1);
                }
            }
        }
    }

    for (auto& entry : m_surveyQuestionAnwsers) {
        // Prevent division by zero
        double docCount = entry.getDocumentCountContainingWord();
        
        if (docCount <= 0) {
            // Safety: minimum value of 1 as default
            docCount = 1;
        }

        cout << "The document count for '" << entry.getName() << "' is: " << docCount << endl;

        // Calculate the inverse document frequency
        double idf = 1 + log(getNumOfDocuments() / docCount);
        entry.setInverseDocumentFrequency(idf);
        
        // Calculate the TF * IDF
        entry.setTFMultiplyIDF(entry.getQueryTermFrequency() * idf);
    }

    cout << "Extracted words/phrases:" << endl;
    for (auto& data : m_surveyQuestionAnwsers) {
        std::cout << "Word: " << data.getName() << ", Term Frequency: " << data.getQueryTermFrequency() << ", Inverse Document Frequency: " << data.getInverseDocumentFrequency() << ", TF * IDF: " << data.getTFMultiplyIDF() << std::endl;
    }
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
                std::string lowerCaseStr(companysize[i]);
                std::transform(lowerCaseStr.begin(), lowerCaseStr.end(), lowerCaseStr.begin(),
                   [](unsigned char c) { return std::tolower(c); });
                if (instance.extractWordsFromString(lowerCaseStr.c_str())) {
                    cout << "There were spaces in the string" << endl;
                } else {
                    cout << "There were no spaces in the string" << endl;
                }
                // cout << "companysize[" << i << "]: " << companysize[i] << endl;
            }
        }
        cout << endl;

        // Print industriesexcitedin (5 elements)
        cout << "The 'industriesexcitedin' table" << endl;
        for (int i = 1; i < industriesexcitedinNum; i++) {
            if (strcmp(industriesexcitedin[i], "NULL") != 0) {
                std::string lowerCaseStr(industriesexcitedin[i]);
                std::transform(lowerCaseStr.begin(), lowerCaseStr.end(), lowerCaseStr.begin(),
                   [](unsigned char c) { return std::tolower(c); });
                if (instance.extractWordsFromString(lowerCaseStr.c_str())) {
                    cout << "There were spaces in the string" << endl;
                } else {
                    cout << "There were no spaces in the string" << endl;
                }
                // cout << "industriesexcitedin[" << i << "]: " << industriesexcitedin[i] << endl;
            }
        }
        cout << endl;

        // Print levelofexperience (2 elements)
        cout << "The 'levelofexperience' table" << endl;
        for (int i = 1; i < levelofexperienceNum; i++) {
            if (strcmp(levelofexperience[i], "NULL") != 0) {
                std::string lowerCaseStr(levelofexperience[i]);
                std::transform(lowerCaseStr.begin(), lowerCaseStr.end(), lowerCaseStr.begin(),
                   [](unsigned char c) { return std::tolower(c); });
                if (instance.extractWordsFromString(lowerCaseStr.c_str())) {
                    cout << "There were spaces in the string" << endl;
                } else {
                    cout << "There were no spaces in the string" << endl;
                }
                // cout << "levelofexperience[" << i << "]: " << levelofexperience[i] << endl;
            }
        }
        cout << endl;

        // Print liketowork (2 elements)
        cout << "The 'liketowork' table" << endl;
        for (int i = 1; i < liketoworkNum; i++) {
            if (strcmp(liketowork[i], "NULL") != 0) {
                std::string lowerCaseStr(liketowork[i]);
                std::transform(lowerCaseStr.begin(), lowerCaseStr.end(), lowerCaseStr.begin(),
                   [](unsigned char c) { return std::tolower(c); });
                if (instance.extractWordsFromString(lowerCaseStr.c_str())) {
                    cout << "There were spaces in the string" << endl;
                } else {
                    cout << "There were no spaces in the string" << endl;
                }
                // cout << "liketowork[" << i << "]: " << liketowork[i] << endl;
            }
        }
        cout << endl;

        // Print minimumexpectedsalary (1 element)
        cout << "The 'minimumexpectedsalary' table" << endl;
        for (int i = 1; i < minimumexpectedsalaryNum; i++) {
            if (strcmp(minimumexpectedsalary[i], "NULL") != 0) {
                std::string lowerCaseStr(minimumexpectedsalary[i]);
                std::transform(lowerCaseStr.begin(), lowerCaseStr.end(), lowerCaseStr.begin(),
                   [](unsigned char c) { return std::tolower(c); });
                if (instance.extractWordsFromString(lowerCaseStr.c_str())) {
                    cout << "There were spaces in the string" << endl;
                } else {
                    cout << "There were no spaces in the string" << endl;
                }
                // cout << "minimumexpectedsalary[" << i << "]: " << minimumexpectedsalary[i] << endl;
            }
        }
        cout << endl;

        // Print rolesinterestedin (5 elements)
        cout << "The 'rolesinterestedin' table" << endl;
        for (int i = 1; i < rolesinterestedinNum; i++) {
            if (strcmp(rolesinterestedin[i], "NULL") != 0) {
                std::string lowerCaseStr(rolesinterestedin[i]);
                std::transform(lowerCaseStr.begin(), lowerCaseStr.end(), lowerCaseStr.begin(),
                   [](unsigned char c) { return std::tolower(c); });
                if (instance.extractWordsFromString(lowerCaseStr.c_str())) {
                    cout << "There were spaces in the string" << endl;
                } else {
                    cout << "There were no spaces in the string" << endl;
                }
                // cout << "rolesinterestedin[" << i << "]: " << rolesinterestedin[i] << endl;
            }
        }
        cout << endl;

        // Print skillsenjoyworkingwith (15 elements)
        cout << "The 'skillsenjoyworkingwith' table" << endl;
        for (int i = 1; i < skillsenjoyworkingwithNum; i++) {
            if (strcmp(skillsenjoyworkingwith[i], "NULL") != 0) {
                std::string lowerCaseStr(skillsenjoyworkingwith[i]);
                std::transform(lowerCaseStr.begin(), lowerCaseStr.end(), lowerCaseStr.begin(),
                   [](unsigned char c) { return std::tolower(c); });
                if (instance.extractWordsFromString(lowerCaseStr.c_str())) {
                    cout << "There were spaces in the string" << endl;
                } else {
                    cout << "There were no spaces in the string" << endl;
                }
                // cout << "skillsenjoyworkingwith[" << i << "]: " << skillsenjoyworkingwith[i] << endl;
            }
        }
        cout << endl;

        // Print valueinrole (3 elements)
        cout << "The 'valueinrole' table" << endl;
        for (int i = 1; i < valueinroleNum; i++) {
            if (strcmp(valueinrole[i], "NULL") != 0) {
                std::string lowerCaseStr(valueinrole[i]);
                std::transform(lowerCaseStr.begin(), lowerCaseStr.end(), lowerCaseStr.begin(),
                   [](unsigned char c) { return std::tolower(c); });
                if (instance.extractWordsFromString(lowerCaseStr.c_str())) {
                    cout << "There were spaces in the string" << endl;
                } else {
                    cout << "There were no spaces in the string" << endl;
                }
                // cout << "valueinrole[" << i << "]: " << valueinrole[i] << endl;
            }
        }

        instance.computeSurveyQuestionsTFIDF();
    }
}