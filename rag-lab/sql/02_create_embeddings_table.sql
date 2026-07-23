-- Lesson 4: table for chunks + 768-dim Vertex embeddings (text-embedding-005)
CREATE TABLE IF NOT EXISTS `cursor-rag-lab-sam.rag_lab.doc_chunks` (
  id STRING NOT NULL,
  doc_id STRING NOT NULL,
  content STRING NOT NULL,
  embedding ARRAY<FLOAT64> NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
