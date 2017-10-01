DROP TABLE IF EXISTS `weld_docs`;

CREATE TABLE `weld_docs` (
  doc_number VARCHAR(15)
  , s3_key VARCHAR(50)
  , PRIMARY KEY (`doc_number`)
);
