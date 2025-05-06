-- website_data database in SQLite

-- DELETE FROM Paragraph;
-- DELETE FROM Document;
-- DELETE FROM Association;
-- DROP TABLE IF EXISTS Association;

-- 1) Paragraphs (each summary paragraph, unlinked for now)
CREATE TABLE IF NOT EXISTS Paragraph (
    ParagraphID  INT NOT NULL UNIQUE,
    Text         TEXT    NOT NULL
--   Score        REAL    NOT NULL DEFAULT 0
);

-- 2) Documents (each URL)
CREATE TABLE IF NOT EXISTS Document (
    DocumentID   INT NOT NULL UNIQUE,
    URL          VARCHAR(255) NOT NULL
);

-- 3) Association (connects each paragraph to its document)
CREATE TABLE IF NOT EXISTS Association (
    ParagraphID  INT NOT NULL,
    DocumentID   INT NOT NULL,
    -- PRIMARY KEY (ParagraphID, DocumentID),
    FOREIGN KEY (ParagraphID) REFERENCES Paragraph(ParagraphID),
    FOREIGN KEY (DocumentID)  REFERENCES Document(DocumentID)
);

-- SELECT * FROM Association;

-- SELECT * FROM Paragraph;

-- SELECT * FROM Document;

-- Check for invalid WordID in Association table(debbuging purposes):

-- -- Check for invalid docID in Association table
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

-- DELETE FROM Association 
-- WHERE rowid IN (
--     SELECT rowid FROM Association 
--     ORDER BY rowid ASC 
--     LIMIT 100000
-- );

-- SELECT COUNT(*) FROM Association;

-- SELECT d.URL AS DocumentURL, p.Text AS Paragraph
-- FROM Association AS a
-- INNER JOIN Paragraph AS p ON a.ParagraphID = p.ParagraphID
-- INNER JOIN Document AS d ON a.DocumentID = d.DocumentID
-- ORDER BY d.URL;

-- SELECT * FROM Word WHERE word = 'work';