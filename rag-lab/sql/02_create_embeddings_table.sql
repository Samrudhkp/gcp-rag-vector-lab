-- Lesson 4: table for chunks + 768-dim Vertex embeddings (text-embedding-005)
-- Note: BigQuery disallows NOT NULL on ARRAY columns (empty array is the null stand-in).
CREATE TABLE IF NOT EXISTS `cursor-rag-lab-sam.rag_lab.doc_chunks` (
  id STRING NOT NULL,
  doc_id STRING NOT NULL,
  content STRING NOT NULL,
  embedding ARRAY<FLOAT64>,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
