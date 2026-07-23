-- Lesson 6: example VECTOR_SEARCH (query embedding must be supplied as a parameter from Python)
-- See src/retrieve.py for the runnable version.
SELECT
  base.id,
  base.doc_id,
  base.content,
  distance
FROM VECTOR_SEARCH(
  TABLE `cursor-rag-lab-sam.rag_lab.doc_chunks`,
  'embedding',
  (
    SELECT embedding
    FROM `cursor-rag-lab-sam.rag_lab.doc_chunks`
    WHERE id = 'REPLACE_WITH_AN_EXISTING_ID'
  ),
  top_k => 3,
  distance_type => 'COSINE'
);
