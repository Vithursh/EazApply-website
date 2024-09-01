#include "Index.h"
#include <iostream>
#include <unordered_map>
#include <vector>
#include <string>
#include <sstream>
#include <fstream>

using namespace std;

void Index::indexDocument(int docID, string websiteLink) {
	string word;
	int position = 0;
    
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
		index[word].emplace_back(docID, position++);
		cout << endl << position << endl;
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
}

const vector<pair<int, int>>& Index::search(const string& term) const {
	static const vector<pair<int, int>> empty;
	auto it = index.find(term);
	return it != index.end() ? it->second : empty;
}

extern "C" {

	Index indexInstance;

	void indexDocument(int docID, const char* websiteLink) {
		cout << "The data recived from c++ is: " << websiteLink << endl;
		string websiteLinkString = websiteLink;
		indexInstance.indexDocument(docID, websiteLinkString);
	}
}

// unordered_map<string, vector<pair<int, int>>> index;