-- website_data database in SQLite

-- DELETE FROM Word;
-- DELETE FROM Document;
-- DELETE FROM Association;

CREATE TABLE IF NOT EXISTS Word(
    WordID INT NOT NULL UNIQUE,
    word VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Document(
    DocumentID INT NOT NULL UNIQUE,
    URL VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Association(
    termID INT,
    docID INT,
    position INT,
    FOREIGN KEY (termID) REFERENCES Word(WordID),
    FOREIGN KEY (docID) REFERENCES Document(DocumentID)
);

-- SELECT * FROM Association;

-- SELECT * FROM Word;

-- SELECT * FROM Document;