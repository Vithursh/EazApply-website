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

string FilterSystem::getWordBeforeAmpersand(const char* str) {
    regex befPattern(R"((\w+)\s*&)");  // Match a word before '&'
    string strValue(str);
    size_t pos = strValue.find('&');
    smatch match;
    if (pos != string::npos) {
        if (regex_search(strValue, match, befPattern)) {
            cout << "Word before '&': " << match[1] << endl;
            return match[1];
        }
    }
    return "";
}

string FilterSystem::getWordAfterAmpersand(const char* str) {
    regex aftPattern(R"(&\s*(\w+))");  // Match a word after '&'
    string strValue(str);
    size_t pos = strValue.find('&');
    smatch match;
    if (pos != string::npos) {
        if (regex_search(strValue, match, aftPattern)) {
            cout << "Word after '&': " << match[1] << endl;
            return match[1];
        }
    }
    return "";
}

extern "C" {
    void receiveData(const char** companysize, int companysizeNum, const char** industriesexcitedin, int industriesexcitedinNum, const char** levelofexperience, int levelofexperienceNum, const char** liketowork, int liketoworkNum, const char** minimumexpectedsalary, int minimumexpectedsalaryNum, const char** rolesinterestedin, int rolesinterestedinNum, const char** skillsenjoyworkingwith, int skillsenjoyworkingwithNum, const char** valueinrole, int valueinroleNum) {
        cout << endl << "The clean data in the tables after sending it to C++:" << endl;
        
        FilterSystem filterSystem;

        // Print companysize (1 element)
        cout << "The 'companysize' table" << endl;
        for (int i = 1; i < companysizeNum; i++) {
            if (strcmp(companysize[i], "NULL") != 0) {
                if (filterSystem.getWordBeforeAmpersand(companysize[i]) != "" && filterSystem.getWordAfterAmpersand(companysize[i]) != "") {
                    cout << "There was an '&' in the string" << endl;
                } else {
                    cout << "There was no '&' in the string" << endl;
                }
                cout << "companysize[" << i << "]: " << companysize[i] << endl;
            }
        }
        cout << endl;

        // Print industriesexcitedin (5 elements)
        cout << "The 'industriesexcitedin' table" << endl;
        for (int i = 1; i < industriesexcitedinNum; i++) {
            if (strcmp(industriesexcitedin[i], "NULL") != 0) {
                if (filterSystem.getWordBeforeAmpersand(industriesexcitedin[i]) != "" && filterSystem.getWordAfterAmpersand(industriesexcitedin[i]) != "") {
                    cout << "There was an '&' in the string" << endl;
                } else {
                    cout << "There was no '&' in the string" << endl;
                }
                cout << "industriesexcitedin[" << i << "]: " << industriesexcitedin[i] << endl;
            }
        }
        cout << endl;

        // Print levelofexperience (2 elements)
        cout << "The 'levelofexperience' table" << endl;
        for (int i = 1; i < levelofexperienceNum; i++) {
            if (strcmp(levelofexperience[i], "NULL") != 0) {
                if (filterSystem.getWordBeforeAmpersand(levelofexperience[i]) != "" && filterSystem.getWordAfterAmpersand(levelofexperience[i]) != "") {
                    cout << "There was an '&' in the string" << endl;
                } else {
                    cout << "There was no '&' in the string" << endl;
                }
                cout << "levelofexperience[" << i << "]: " << levelofexperience[i] << endl;
            }
        }
        cout << endl;

        // Print liketowork (2 elements)
        cout << "The 'liketowork' table" << endl;
        for (int i = 1; i < liketoworkNum; i++) {
            if (strcmp(liketowork[i], "NULL") != 0) {
                if (filterSystem.getWordBeforeAmpersand(liketowork[i]) != "" && filterSystem.getWordAfterAmpersand(liketowork[i]) != "") {
                    cout << "There was an '&' in the string" << endl;
                } else {
                    cout << "There was no '&' in the string" << endl;
                }
                cout << "liketowork[" << i << "]: " << liketowork[i] << endl;
            }
        }
        cout << endl;

        // Print minimumexpectedsalary (1 element)
        cout << "The 'minimumexpectedsalary' table" << endl;
        for (int i = 1; i < minimumexpectedsalaryNum; i++) {
            if (strcmp(minimumexpectedsalary[i], "NULL") != 0) {
                if (filterSystem.getWordBeforeAmpersand(minimumexpectedsalary[i]) != "" && filterSystem.getWordAfterAmpersand(minimumexpectedsalary[i]) != "") {
                    cout << "There was an '&' in the string" << endl;
                } else {
                    cout << "There was no '&' in the string" << endl;
                }
                cout << "minimumexpectedsalary[" << i << "]: " << minimumexpectedsalary[i] << endl;
            }
        }
        cout << endl;

        // Print rolesinterestedin (5 elements)
        cout << "The 'rolesinterestedin' table" << endl;
        for (int i = 1; i < rolesinterestedinNum; i++) {
            if (strcmp(rolesinterestedin[i], "NULL") != 0) {
                if (filterSystem.getWordBeforeAmpersand(rolesinterestedin[i]) != "" && filterSystem.getWordAfterAmpersand(rolesinterestedin[i]) != "") {
                    cout << "There was an '&' in the string" << endl;
                } else {
                    cout << "There was no '&' in the string" << endl;
                }
                cout << "rolesinterestedin[" << i << "]: " << rolesinterestedin[i] << endl;
            }
        }
        cout << endl;

        // Print skillsenjoyworkingwith (15 elements)
        cout << "The 'skillsenjoyworkingwith' table" << endl;
        for (int i = 1; i < skillsenjoyworkingwithNum; i++) {
            if (strcmp(skillsenjoyworkingwith[i], "NULL") != 0) {
                if (filterSystem.getWordBeforeAmpersand(skillsenjoyworkingwith[i]) != "" && filterSystem.getWordAfterAmpersand(skillsenjoyworkingwith[i]) != "") {
                    cout << "There was an '&' in the string" << endl;
                } else {
                    cout << "There was no '&' in the string" << endl;
                }
                cout << "skillsenjoyworkingwith[" << i << "]: " << skillsenjoyworkingwith[i] << endl;
            }
        }
        cout << endl;

        // Print valueinrole (3 elements)
        cout << "The 'valueinrole' table" << endl;
        for (int i = 1; i < valueinroleNum; i++) {
            if (strcmp(valueinrole[i], "NULL") != 0) {
                if (filterSystem.getWordBeforeAmpersand(valueinrole[i]) != "" && filterSystem.getWordAfterAmpersand(valueinrole[i]) != "") {
                    cout << "There was an '&' in the string" << endl;
                } else {
                    cout << "There was no '&' in the string" << endl;
                }
                cout << "valueinrole[" << i << "]: " << valueinrole[i] << endl;
            }
        }
    }
}