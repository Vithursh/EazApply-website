#include "Index.h"
#include <iostream>
#include <unordered_map>
#include <vector>
#include <string>
#include <sstream>
#include <fstream>
#include <cstdlib>
#include "sqlite/sqlite3.h"

using namespace std;

void Index::indexDocument(string websiteLink) {

    sqlite3* DB;
    int exit = sqlite3_open("/home/vithursh/Coding/EazApply/backend/File Data/website_data.db", &DB);

    if (exit) {
        std::cerr << "Error open DB " << sqlite3_errmsg(DB) << std::endl;
        return;
    } else {
        std::cout << "Opened Database Successfully!" << std::endl;
    }

    executeSQLFile(DB, exit);

	string paragraph;
	ifstream inputFile("/home/vithursh/Coding/EazApply/backend/File Data/website_content.txt"); 

    // Check if the file is successfully opened 
    if (!inputFile.is_open()) {
        cerr << "Error opening the file!" << endl; 
        return; 
    } 

    // std::vector<std::string> words{};
    std::string line{}, content{};

    while (std::getline(inputFile, line)) {
        size_t start = 0;
        while ((start = line.find('[', start)) != std::string::npos) {
            size_t end = line.find(']', start);
            if (end != std::string::npos) {
                content = line.substr(start + 1, end - start - 1);
                std::cout << "The text is: "<< content << std::endl;
                start = end + 1;
            } else {
                break; // No matching closing bracket
            }
        }
    }

    // int position{};
    paragraph = content;
    int DocumentID = rand();
    // cout << "File Content: " << endl;
    // while (!words.empty()) {
        // Get first word before removing
        // string currentWord = words.front();
        // words.erase(words.begin());  // Remove first element
        if (!paragraph.empty()) {
            int Paragraphid = rand();
            insertData(DB, exit, Paragraphid, utilities.trimSpace(paragraph), DocumentID, websiteLink);
            cout << endl << Paragraphid << endl;
        }
    // }
	
    // Close the file 
    inputFile.close();

	// ofstream myfile; // Create an ofstream object
    // myfile.open("/home/vithursh/Coding/EazApply/backend/File Data/test.txt"); // Open a file named "example.txt"

    // if (myfile.is_open()) { // Check if the file is open
    //     myfile << "The C++ indexDocument was called!!!\n"; // Write to the file
    //     myfile.close(); // Close the file
    //     cout << "File written successfully!" << endl;
    // } else {
    //     cout << "Unable to open file" << endl;
    // }

    sqlite3_close(DB);
}

void Index::executeSQLFile(sqlite3* DB, int rc) {
    const std::string filePath = "/home/vithursh/Coding/EazApply/backend/Search Engine/Indexer/website_data database.sql";
    std::ifstream file(filePath);
    if (!file.is_open()) {
        std::cerr << "Error opening the file!" << std::endl;
        sqlite3_close(DB);
        return;
    }

    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string sql = buffer.str();

    char *errMsg = 0;
    rc = sqlite3_exec(DB, sql.c_str(), 0, 0, &errMsg);
    if (rc != SQLITE_OK) {
        std::cerr << "SQL error: " << errMsg << std::endl;
        sqlite3_free(errMsg);
    } else {
        std::cout << "SQL file executed successfully!" << std::endl;
    }
}

void Index::insertData(sqlite3* DB, int rc, int ParagraphID, string paragraph, int DocumentID, string URL) {
    sqlite3_stmt *stmt;
    bool docStatus = false, wordStatus = false;

    // Check if ParagraphID exists
    const char *checkParagraph = "SELECT 1 FROM Paragraph WHERE ParagraphID = ?;";
    rc = sqlite3_prepare_v2(DB, checkParagraph, -1, &stmt, 0);
    if (rc != SQLITE_OK) {
        std::cerr << "SQL error in check paragraph: " << sqlite3_errmsg(DB) << std::endl;
        return;
    }
    sqlite3_bind_int(stmt, 1, ParagraphID);
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        // Generate new ParagraphID if exists
        ParagraphID = rand();
        sqlite3_reset(stmt);
        sqlite3_bind_int(stmt, 1, ParagraphID);
    }
    sqlite3_finalize(stmt);

    // Check if DocumentID exists
    const char *checkDoc = "SELECT 1 FROM Document WHERE DocumentID = ?;";
    rc = sqlite3_prepare_v2(DB, checkDoc, -1, &stmt, 0);
    if (rc != SQLITE_OK) {
        std::cerr << "SQL error in check document: " << sqlite3_errmsg(DB) << std::endl;
        return;
    }
    sqlite3_bind_int(stmt, 1, DocumentID);
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        // Generate new DocumentID if exists
        DocumentID = rand();
        sqlite3_reset(stmt);
        sqlite3_bind_int(stmt, 1, DocumentID);
    }
    sqlite3_finalize(stmt);

    // Insert into Paragraph table
    if (!paragraph.empty()) {
        const char *sql = "INSERT INTO Paragraph (ParagraphID, Text) VALUES (?, LOWER(?));";
        rc = sqlite3_prepare_v2(DB, sql, -1, &stmt, 0);
        if (rc != SQLITE_OK) {
            std::cerr << "SQL error in paragraph insert: " << sqlite3_errmsg(DB) << std::endl;
            return;
        }
        
        sqlite3_bind_int(stmt, 1, ParagraphID);
        sqlite3_bind_text(stmt, 2, paragraph.c_str(), -1, SQLITE_STATIC);
        
        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            std::cerr << "Execution failed: " << sqlite3_errmsg(DB) << std::endl;
            wordStatus = false;
        } else {
            std::cout << "Record inserted successfully for the paragraph table" << std::endl;
            wordStatus = true;
        }
        sqlite3_finalize(stmt);
    }

    // Insert into Document table
    const char *sql2 = "INSERT INTO Document (DocumentID, URL) VALUES (?, ?);";
    rc = sqlite3_prepare_v2(DB, sql2, -1, &stmt, 0);
    if (rc != SQLITE_OK) {
        std::cerr << "SQL error in document insert: " << sqlite3_errmsg(DB) << std::endl;
        return;
    }

    sqlite3_bind_int(stmt, 1, DocumentID);
    sqlite3_bind_text(stmt, 2, URL.c_str(), -1, SQLITE_STATIC);

    rc = sqlite3_step(stmt);
    if (rc != SQLITE_DONE) {
        std::cerr << "Execution failed: " << sqlite3_errmsg(DB) << std::endl;
        docStatus = false;
    } else {
        std::cout << "Record inserted successfully for the document table" << std::endl;
        docStatus = true;
    }
    sqlite3_finalize(stmt);

    // Write to CSV if both inserts failed
    if (wordStatus == false && docStatus == false) {
        utilities.writeToCSV(ParagraphID, DocumentID, paragraph);
    }

    // Insert into Association table
    if (!paragraph.empty()) {
        const char *sql3 = "INSERT INTO Association (ParagraphID, DocumentID) VALUES (?, ?);";
        rc = sqlite3_prepare_v2(DB, sql3, -1, &stmt, 0);
        if (rc != SQLITE_OK) {
            std::cerr << "SQL error in association insert: " << sqlite3_errmsg(DB) << std::endl;
            return;
        }

        sqlite3_bind_int(stmt, 1, ParagraphID);
        sqlite3_bind_int(stmt, 2, DocumentID);

        std::cout << "Inserting into Association: ParagraphID=" << ParagraphID 
                  << ", DocumentID=" << DocumentID << std::endl;

        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            std::cerr << "Association insertion failed: " << sqlite3_errmsg(DB) << std::endl;
        } else {
            std::cout << "Record inserted successfully for the Association table" << std::endl;
        }
        sqlite3_finalize(stmt);
    }
}

int Index::checkWordExists(sqlite3* DB, int rc, string word) {
    sqlite3_stmt *stmt;
    int wordId{};

    const char *sql = "SELECT WordID FROM Word WHERE word = ?;";
    rc = sqlite3_prepare_v2(DB, sql, -1, &stmt, 0);
    if (rc != SQLITE_OK) {
        std::cerr << "SQL error: " << sqlite3_errmsg(DB) << std::endl;
        return 0;
    }

    sqlite3_bind_text(stmt, 1, word.c_str(), -1, SQLITE_STATIC);

    rc = sqlite3_step(stmt);
    if (rc == SQLITE_ROW) {
        wordId = sqlite3_column_int(stmt, 0);
        std::cout << "Word found with ID: " << wordId << std::endl;
    } else if (rc != SQLITE_DONE) {
        std::cerr << "Query failed: " << sqlite3_errmsg(DB) << std::endl;
    }

    sqlite3_finalize(stmt);
    return wordId;
}

// int Index::getTermFrequency(sqlite3* DB, int rc, string word) {
//     sqlite3_stmt *stmt;

//     // Selecting data from the Word table
//     const char *sql = "SELECT termFrequency FROM Word WHERE word = ?;";

//     rc = sqlite3_prepare_v2(DB, sql, -1, &stmt, 0);
//     if (rc != SQLITE_OK) {
//         std::cerr << "SQL error: " << sqlite3_errmsg(DB) << std::endl;
//         sqlite3_close(DB);
//         return -1;
//     }

//     sqlite3_bind_text(stmt, 1, word.c_str(), -1, SQLITE_STATIC);

//     int result = 0;
//     rc = sqlite3_step(stmt);
//     if (rc == SQLITE_ROW) {
//         result = sqlite3_column_int(stmt, 0);
//         std::cout << "Data retrieved successfully: " << result << std::endl;
//     } else if (rc != SQLITE_DONE) {
//         std::cerr << "Execution failed: " << sqlite3_errmsg(DB) << std::endl;
//         sqlite3_finalize(stmt);
//         return -1;
//     }

//     // Reset the statement to reuse it
//     sqlite3_reset(stmt);

//     sqlite3_finalize(stmt);

//     return result;
// }

// void Index::update(sqlite3* DB, int rc, const string& word, int termOccurrence) {
//     sqlite3_stmt *stmt;

//     // SQL update statement
//     const char *sql = "UPDATE Word SET OccurrenceCount = ? WHERE word = ?;";

//     rc = sqlite3_prepare_v2(DB, sql, -1, &stmt, 0);
//     if (rc != SQLITE_OK) {
//         std::cerr << "SQL error: " << sqlite3_errmsg(DB) << std::endl;
//         sqlite3_close(DB);
//         return;
//     }

//     // Bind values to the placeholders
//     sqlite3_bind_int(stmt, 1, termOccurrence);
//     sqlite3_bind_text(stmt, 2, word.c_str(), -1, SQLITE_STATIC);

//     // Execute the statement
//     rc = sqlite3_step(stmt);
//     if (rc == SQLITE_DONE) {
//         std::cout << "Data updated successfully." << std::endl;
//     } else {
//         std::cerr << "Execution failed: " << sqlite3_errmsg(DB) << std::endl;
//     }

//     // Finalize the statement
//     sqlite3_finalize(stmt);
// }

// void Index::termFrequency() {}

const vector<pair<int, int>>& Index::search(const string& term) const {
	static const vector<pair<int, int>> empty;
	auto it = index.find(term);
	return it != index.end() ? it->second : empty;
}

extern "C" {

	Index indexInstance;

	void indexDocument(const char* websiteLink) {
		cout << "The data recived from c++ is: " << websiteLink << endl;
		string websiteLinkString = websiteLink;
		indexInstance.indexDocument(websiteLinkString);
	}
}