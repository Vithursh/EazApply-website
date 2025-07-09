-- website_data database in SQLite

-- DELETE FROM Paragraph;
-- DELETE FROM Document;
-- DELETE FROM Association;
-- DROP TABLE IF EXISTS Association;
-- DROP TABLE IF EXISTS Document;
-- DROP TABLE IF EXISTS Paragraph;

-- 1) Paragraphs (each summary paragraph, unlinked for now)
CREATE TABLE IF NOT EXISTS Paragraph (
    ParagraphID  INT NOT NULL UNIQUE,
    Text         TEXT    NOT NULL
--   Score        REAL    NOT NULL DEFAULT 0
);

-- 2) Documents (each URL)
CREATE TABLE IF NOT EXISTS Document (
    DocumentID   INT NOT NULL UNIQUE,
    URL          VARCHAR(255) NOT NULL,
    Title          VARCHAR(255) NOT NULL
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

-- Check for duplicates on all columns in all tables(debbuging purposes):
-- SELECT *, COUNT(*)
-- FROM Association
-- GROUP BY ParagraphID, DocumentID
-- HAVING COUNT(*) > 1;

-- DELETE FROM Association 
-- WHERE rowid IN (
--     SELECT rowid FROM Association 
--     ORDER BY rowid ASC 
--     LIMIT 100000
-- );

SELECT d.URL AS DocumentURL, p.Text, d.Title
FROM Association AS a
INNER JOIN Paragraph AS p ON a.ParagraphID = p.ParagraphID
INNER JOIN Document AS d ON a.DocumentID = d.DocumentID
ORDER BY d.URL;