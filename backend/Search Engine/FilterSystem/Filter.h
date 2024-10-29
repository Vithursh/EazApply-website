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
    FilterSystem();
    ~FilterSystem();
};
#endif