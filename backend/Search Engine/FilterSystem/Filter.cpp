#include <iostream>
#include <string>
#include <cstring>
#include <sstream>
#include <fstream>
#include <regex>
#include <cstdlib>
#include <typeinfo>
#include "../../sqlite3.h"
#include "Filter.h"

using namespace std;

void FilterSystem::setName(std::string name) {
    m_name = name;
}

std::string FilterSystem::getName() {
    return m_name;
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
                filterSystem.push_back(item);  // Add each match to the vector 
            }
        }
    } else {
        FilterSystem item{};
        item.setName(strValue);
        filterSystem.push_back(item);
    }

    cout << "Extracted words/phrases:" << endl;
    for (auto& items : filterSystem) {
        cout << "Words in 'filterSystem' is: " << items.getName() << endl;
    }

    return containsSpaces;
}

extern "C" {
    void receiveData(const char** companysize, int companysizeNum, const char** industriesexcitedin, int industriesexcitedinNum, const char** levelofexperience, int levelofexperienceNum, const char** liketowork, int liketoworkNum, const char** minimumexpectedsalary, int minimumexpectedsalaryNum, const char** rolesinterestedin, int rolesinterestedinNum, const char** skillsenjoyworkingwith, int skillsenjoyworkingwithNum, const char** valueinrole, int valueinroleNum) {
        cout << endl << "The clean data in the tables after sending it to C++:" << endl;
        
        FilterSystem filterSystem;

        // Print companysize (1 element)
        cout << "The 'companysize' table" << endl;
        for (int i = 1; i < companysizeNum; i++) {
            if (strcmp(companysize[i], "NULL") != 0) {
                if (filterSystem.extractWordsFromString(companysize[i])) {
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
                if (filterSystem.extractWordsFromString(industriesexcitedin[i])) {
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
                if (filterSystem.extractWordsFromString(levelofexperience[i])) {
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
                if (filterSystem.extractWordsFromString(liketowork[i])) {
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
                if (filterSystem.extractWordsFromString(minimumexpectedsalary[i])) {
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
                if (filterSystem.extractWordsFromString(rolesinterestedin[i])) {
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
                if (filterSystem.extractWordsFromString(skillsenjoyworkingwith[i])) {
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
                if (filterSystem.extractWordsFromString(valueinrole[i])) {
                    cout << "There were spaces in the string" << endl;
                } else {
                    cout << "There were no spaces in the string" << endl;
                }
                cout << "valueinrole[" << i << "]: " << valueinrole[i] << endl;
            }
        }
    }
}