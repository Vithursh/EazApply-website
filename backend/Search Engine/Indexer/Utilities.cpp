#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <cstdlib>
#include "sqlite/sqlite3.h"
#include "Utilities.h"

using namespace std;

string Utilities::toLowerCase(string description) {
    std::string finalDesc{};
    
    for (size_t i = 0; i < description.length(); i++) {  // Use size() instead of strlen()
        if (description[i] == ' ') {
            // if (i + 1 < description.size()) {  // Check if there's a next character
                char temp = tolower(description[i + 1]);
                finalDesc += ' ';  // Keep the space
                finalDesc += temp; // Add the uppercase next character
                i++; // Skip the next character since it's already processed
            // }
        } else if (description[i] == description[0]) {
            char temp = tolower(description[0]);
            finalDesc += temp;
        } else {
            finalDesc += description[i];  // Add non-space characters as is
        }
    }
    
    return removeStopWords(&finalDesc);
}

string Utilities::removeStopWords(string* word) {
    // Adjust the array size as needed to fit all stop words
    string* stopWords = new string[96];

    // Allocate each word to an index
    stopWords[0] = "a";
    stopWords[1] = "an";
    stopWords[2] = "the";
    stopWords[3] = "and";
    stopWords[4] = "but";
    stopWords[5] = "or";
    stopWords[6] = "nor";
    stopWords[7] = "for";
    stopWords[8] = "so";
    stopWords[9] = "yet";
    stopWords[10] = "in";
    stopWords[11] = "on";
    stopWords[12] = "at";
    stopWords[13] = "by";
    stopWords[14] = "with";
    stopWords[15] = "about";
    stopWords[16] = "against";
    stopWords[17] = "between";
    stopWords[18] = "into";
    stopWords[19] = "through";
    stopWords[20] = "during";
    stopWords[21] = "before";
    stopWords[22] = "after";
    stopWords[23] = "above";
    stopWords[24] = "below";
    stopWords[25] = "to";
    stopWords[26] = "from";
    stopWords[27] = "up";
    stopWords[28] = "down";
    stopWords[29] = "out";
    stopWords[30] = "over";
    stopWords[31] = "under";
    stopWords[32] = "again";
    stopWords[33] = "further";
    stopWords[34] = "then";
    stopWords[35] = "once";
    stopWords[36] = "i";
    stopWords[37] = "me";
    stopWords[38] = "my";
    stopWords[39] = "myself";
    stopWords[40] = "we";
    stopWords[41] = "our";
    stopWords[42] = "ours";
    stopWords[43] = "ourselves";
    stopWords[44] = "you";
    stopWords[45] = "your";
    stopWords[46] = "yours";
    stopWords[47] = "yourself";
    stopWords[48] = "yourselves";
    stopWords[49] = "he";
    stopWords[50] = "him";
    stopWords[51] = "his";
    stopWords[52] = "himself";
    stopWords[53] = "she";
    stopWords[54] = "her";
    stopWords[55] = "hers";
    stopWords[56] = "herself";
    stopWords[57] = "it";
    stopWords[58] = "its";
    stopWords[59] = "itself";
    stopWords[60] = "they";
    stopWords[61] = "them";
    stopWords[62] = "their";
    stopWords[63] = "theirs";
    stopWords[64] = "themselves";
    stopWords[65] = "am";
    stopWords[66] = "is";
    stopWords[67] = "are";
    stopWords[68] = "was";
    stopWords[69] = "were";
    stopWords[70] = "be";
    stopWords[71] = "been";
    stopWords[72] = "being";
    stopWords[73] = "have";
    stopWords[74] = "has";
    stopWords[75] = "had";
    stopWords[76] = "having";
    stopWords[77] = "do";
    stopWords[78] = "does";
    stopWords[79] = "did";
    stopWords[80] = "doing";
    stopWords[81] = "very";
    stopWords[82] = "too";
    stopWords[83] = "just";
    stopWords[84] = "now";
    stopWords[85] = "then";
    stopWords[86] = "once";
    stopWords[87] = "here";
    stopWords[88] = "there";
    stopWords[89] = "when";
    stopWords[90] = "where";
    stopWords[91] = "why";
    stopWords[92] = "how";
    stopWords[93] = "all";
    stopWords[94] = "some";
    stopWords[95] = "any";

    // Example logic: check if the word is a stop word
    for (int i = 0; i < 96; i++) {
        if (*word == stopWords[i]) {
            cout << "'" << *word << "'" << " is a stop word!!!" << endl;
            return ""; // Return empty string if it's a stop word
        }
    }

    // If not a stop word, return the original word
    return *word;
}