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

	string word;
	ifstream inputFile("/home/vithursh/Coding/EazApply/backend/File Data/website_content.txt"); 
	
    // Check if the file is successfully opened 
    if (!inputFile.is_open()) {
        cerr << "Error opening the file!" << endl; 
        return; 
    } 
	
    // Read each line of the file and print it to the 
    // standard output stream 
    cout << "File Content: " << endl;
    while (getline(inputFile, word, ',')) {
        cout << word << endl; // Print the current line
		// index[word].emplace_back(docID, position++);
        int id = rand();
        insertData(DB, exit, id, utilities.toLowerCase(word), id, websiteLink, id, id, id);
		cout << endl << id << endl;
    }
	
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

void Index::insertData(sqlite3* DB, int rc, int WordID, string word, int DocumentID, string URL, int termID, int docID, int position) {
    sqlite3_stmt *stmt;

    // Check if word exists in database
    // if (checkWordExists(DB, rc, word)) {
        // Get the word id
        // DocumentID = getWordId(DB, rc, word);
        // cout << "'" << word << "'" <<" already exists in the database" << endl;
    // } else {
        // Inserting data into the Word table
        const char *sql = "INSERT INTO Word (WordID, word) VALUES (?, ?);";

        rc = sqlite3_prepare_v2(DB, sql, -1, &stmt, 0);
        if (rc != SQLITE_OK) {
            std::cerr << "SQL error: " << sqlite3_errmsg(DB) << std::endl;
            sqlite3_close(DB);
            return;
        }

        sqlite3_bind_int(stmt, 1, WordID);
        sqlite3_bind_text(stmt, 2, word.c_str(), -1, SQLITE_STATIC);

        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            std::cerr << "Execution failed: " << sqlite3_errmsg(DB) << std::endl;
        } else {
            std::cout << "Record inserted successfully for the word table" << std::endl;
        }

        // Reset the statement to reuse it
        sqlite3_reset(stmt);

        sqlite3_finalize(stmt);
    // }

    // Inserting data into the Document table
    const char *sql2 = "INSERT INTO Document (DocumentID, URL) VALUES (?, ?);";

    rc = sqlite3_prepare_v2(DB, sql2, -1, &stmt, 0);
    if (rc != SQLITE_OK) {
        std::cerr << "SQL error: " << sqlite3_errmsg(DB) << std::endl;
        sqlite3_close(DB);
        return;
    }

    sqlite3_bind_int(stmt, 1, DocumentID);
    sqlite3_bind_text(stmt, 2, URL.c_str(), -1, SQLITE_STATIC);

    rc = sqlite3_step(stmt);
    if (rc != SQLITE_DONE) {
        std::cerr << "Execution failed: " << sqlite3_errmsg(DB) << std::endl;
    } else {
        std::cout << "Record inserted successfully for the document table" << std::endl;
    }

    // Reset the statement to reuse it
    sqlite3_reset(stmt);

    sqlite3_finalize(stmt);

    // Inserting data into the Association table
    const char *sql3 = "INSERT INTO Association (termID, docID, position) VALUES (?, ?, ?);";

    rc = sqlite3_prepare_v2(DB, sql3, -1, &stmt, 0);
    if (rc != SQLITE_OK) {
        std::cerr << "SQL error: " << sqlite3_errmsg(DB) << std::endl;
        sqlite3_close(DB);
        return;
    }

    sqlite3_bind_int(stmt, 1, termID);
    sqlite3_bind_int(stmt, 2, docID);
    sqlite3_bind_int(stmt, 3, position);

    rc = sqlite3_step(stmt);
    if (rc != SQLITE_DONE) {
        std::cerr << "Execution failed: " << sqlite3_errmsg(DB) << std::endl;
    } else {
        std::cout << "Record inserted successfully for the Association table" << std::endl;
    }

    // Reset the statement to reuse it
    sqlite3_reset(stmt);

    sqlite3_finalize(stmt);
}

bool Index::checkWordExists(sqlite3* DB, int rc, string word) {
    sqlite3_stmt *stmt;

    // Prepare the SQL statement
    const char *sql = "SELECT word FROM Word WHERE word = ?;";
    rc = sqlite3_prepare_v2(DB, sql, -1, &stmt, 0);
    if (rc != SQLITE_OK) {
        std::cerr << "SQL error: " << sqlite3_errmsg(DB) << std::endl;
        return false;
    }

    // Convert the first letter to uppercase
    string upperCase = word;
    upperCase[0] = toupper(upperCase[0]);

    // Bind the word with the first letter in uppercase
    sqlite3_bind_text(stmt, 1, upperCase.c_str(), -1, SQLITE_STATIC);

    // Execute the query and check the result
    bool wordFound = false;
    rc = sqlite3_step(stmt);
    if (rc == SQLITE_ROW) {
        wordFound = true;
        std::cout << "Record queried successfully for the word table" << std::endl;
    } else if (rc != SQLITE_DONE) {
        std::cerr << "Execution failed: " << sqlite3_errmsg(DB) << std::endl;
    }

    // Reset the statement to reuse it
    sqlite3_reset(stmt);

    // Convert the first letter to lowercase
    string lowerCase = word;
    lowerCase[0] = tolower(lowerCase[0]);

    // Bind the word with the first letter in lowercase
    sqlite3_bind_text(stmt, 1, lowerCase.c_str(), -1, SQLITE_STATIC);

    // Execute the query and check the result
    rc = sqlite3_step(stmt);
    if (rc == SQLITE_ROW) {
        wordFound = true;
        std::cout << "Record queried successfully for the word table" << std::endl;
    } else if (rc != SQLITE_DONE) {
        std::cerr << "Execution failed: " << sqlite3_errmsg(DB) << std::endl;
    }

    // Finalize the statement
    sqlite3_finalize(stmt);

    return wordFound;
}

int Index::getWordId(sqlite3* DB, int rc, string word) {
    sqlite3_stmt *stmt;

    // Selecting data from the Word table
    const char *sql = "SELECT WordID FROM Word WHERE word = ?;";

    rc = sqlite3_prepare_v2(DB, sql, -1, &stmt, 0);
    if (rc != SQLITE_OK) {
        std::cerr << "SQL error: " << sqlite3_errmsg(DB) << std::endl;
        sqlite3_close(DB);
        return -1;
    }

    sqlite3_bind_text(stmt, 1, word.c_str(), -1, SQLITE_STATIC);

    int result = 0;
    rc = sqlite3_step(stmt);
    if (rc == SQLITE_ROW) {
        result = sqlite3_column_int(stmt, 0);
        std::cout << "Data retrieved successfully: " << result << std::endl;
    } else if (rc != SQLITE_DONE) {
        std::cerr << "Execution failed: " << sqlite3_errmsg(DB) << std::endl;
        sqlite3_finalize(stmt);
        return -1;
    }

    // Reset the statement to reuse it
    sqlite3_reset(stmt);

    sqlite3_finalize(stmt);

    return result;
}

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