export type DocumentResponse = {
  id: number;
  filename: string;
  content_type: string;
  chunk_count: number;
  created_at: string;
};


export type RAGSearchHit = {
  document_id: number;
  filename: string;
  chunk_index: number;
  content: string;
  similarity: number;
};


export type RAGSearchResponse = {
  query: string;
  results: RAGSearchHit[];
};


export type RAGAskRequest = {
  question: string;
  top_k?: number;
};


export type RAGAskResponse = {
  answer: string;
  sources: RAGSearchHit[];
  provider: string;
};