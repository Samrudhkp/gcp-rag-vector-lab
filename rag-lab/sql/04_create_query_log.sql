-- Lesson 8: log every RAG question/answer for demos and debugging
CREATE TABLE IF NOT EXISTS `cursor-rag-lab-sam.rag_lab.query_log` (
  query_id STRING NOT NULL,
  question STRING NOT NULL,
  answer STRING,
  retrieved_ids ARRAY<STRING>,
  distances ARRAY<FLOAT64>,
  embedding_model STRING,
  gemini_model STRING,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
