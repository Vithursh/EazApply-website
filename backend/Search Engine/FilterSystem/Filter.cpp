#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <cstdlib>
#include "../../sqlite3.h"
#include "Filter.h"

using namespace std;

extern "C" {
    void receiveData(const char** companysize, int companysizeNum, const char** industriesexcitedin, int industriesexcitedinNum, const char** levelofexperience, int levelofexperienceNum, const char** liketowork, int liketoworkNum, const char** minimumexpectedsalary, int minimumexpectedsalaryNum, const char** rolesinterestedin, int rolesinterestedinNum, const char** skillsenjoyworkingwith, int skillsenjoyworkingwithNum, const char** valueinrole, int valueinroleNum) {
        // Print companysize (1 element)
        cout << endl << "The data in the tables after sending it to C++:" << endl;
        for (int i = 0; i < companysizeNum; i++) {
            cout << "companysize[" << i << "]: " << companysize[i] << endl;
        }
        cout << endl;

        // Print industriesexcitedin (5 elements)
        for (int i = 0; i < industriesexcitedinNum; i++) {
            cout << "industriesexcitedin[" << i << "]: " << industriesexcitedin[i] << endl;
        }
        cout << endl;

        // Print levelofexperience (2 elements)
        for (int i = 0; i < levelofexperienceNum; i++) {
            cout << "levelofexperience[" << i << "]: " << levelofexperience[i] << endl;
        }
        cout << endl;

        // Print liketowork (2 elements)
        for (int i = 0; i < liketoworkNum; i++) {
            cout << "liketowork[" << i << "]: " << liketowork[i] << endl;
        }
        cout << endl;

        // Print minimumexpectedsalary (1 element)
        for (int i = 0; i < minimumexpectedsalaryNum; i++) {
            cout << "minimumexpectedsalary[" << i << "]: " << minimumexpectedsalary[i] << endl;
        }
        cout << endl;

        // Print rolesinterestedin (5 elements)
        for (int i = 0; i < rolesinterestedinNum; i++) {
            cout << "rolesinterestedin[" << i << "]: " << rolesinterestedin[i] << endl;
        }
        cout << endl;

        // Print skillsenjoyworkingwith (15 elements)
        for (int i = 0; i < skillsenjoyworkingwithNum; i++) {
            cout << "skillsenjoyworkingwith[" << i << "]: " << skillsenjoyworkingwith[i] << endl;
        }
        cout << endl;

        // Print valueinrole (3 elements)
        for (int i = 0; i < valueinroleNum; i++) {
            cout << "valueinrole[" << i << "]: " << valueinrole[i] << endl;
        }
    }
}