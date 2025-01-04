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

CREATE TABLE IF NOT EXISTS Association (
    termID INT NOT NULL,
    docID INT NOT NULL,
    position INT NOT NULL,
    FOREIGN KEY (termID) REFERENCES Word(WordID),
    FOREIGN KEY (docID) REFERENCES Document(DocumentID)
);

-- SELECT * FROM Association;

-- SELECT * FROM Word;

-- SELECT * FROM Document;

-- Check for invalid WordID in Association table(debbuging purposes):

-- Check for invalid docID in Association table
-- SELECT DISTINCT docID FROM Association
-- WHERE docID NOT IN (SELECT DocumentID FROM Document);

-- -- Check for invalid termID in Association table
-- SELECT DISTINCT termID FROM Association
-- WHERE termID NOT IN (SELECT WordID FROM Word);

-- -- Check for duplicate rows in Association table
-- SELECT termID, docID, position, COUNT(*)
-- FROM Association
-- GROUP BY termID, docID, position
-- HAVING COUNT(*) > 1;

-- SELECT Word.word, Document.URL FROM Association
-- INNER JOIN Word ON Association.termID = Word.WordID
-- INNER JOIN Document ON Association.docID = Document.DocumentID;

-- SELECT * FROM Word WHERE word = 'work';