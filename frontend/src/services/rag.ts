import {
  API_BASE_URL,
} from "../config/api";

import type {
  DocumentResponse,
  RAGAskRequest,
  RAGAskResponse,
  RAGSearchResponse,
} from "../types/rag";


export async function uploadDocument(
  file: File,
): Promise<DocumentResponse> {

  const formData = new FormData();

  formData.append(
    "file",
    file,
  );


  const response = await fetch(
    `${API_BASE_URL}/rag/documents`,
    {
      method: "POST",
      body: formData,
    },
  );


  if (!response.ok) {
    const message =
      await readErrorMessage(
        response,
      );

    throw new Error(message);
  }


  return response.json();
}


export async function getDocuments():
  Promise<DocumentResponse[]> {

  const response = await fetch(
    `${API_BASE_URL}/rag/documents`,
  );


  if (!response.ok) {
    throw new Error(
      "Unable to load documents.",
    );
  }


  return response.json();
}


export async function deleteDocument(
  documentId: number,
): Promise<void> {

  const response = await fetch(
    `${API_BASE_URL}/rag/documents/${documentId}`,
    {
      method: "DELETE",
    },
  );


  if (!response.ok) {
    throw new Error(
      "Unable to delete document.",
    );
  }
}


export async function searchDocuments(
  query: string,
  topK = 5,
): Promise<RAGSearchResponse> {

  const response = await fetch(
    `${API_BASE_URL}/rag/search`,
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json",
      },

      body: JSON.stringify({
        query,
        top_k: topK,
      }),
    },
  );


  if (!response.ok) {
    throw new Error(
      "Unable to search documentation.",
    );
  }


  return response.json();
}


export async function askDocumentation(
  request: RAGAskRequest,
): Promise<RAGAskResponse> {

  const response = await fetch(
    `${API_BASE_URL}/rag/ask`,
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json",
      },

      body: JSON.stringify(
        request,
      ),
    },
  );


  if (!response.ok) {
    const message =
      await readErrorMessage(
        response,
      );

    throw new Error(message);
  }


  return response.json();
}


async function readErrorMessage(
  response: Response,
): Promise<string> {

  try {
    const data = await response.json();

    if (
      typeof data.detail
      === "string"
    ) {
      return data.detail;
    }

  } catch {
    // Ignore malformed JSON.
  }


  return (
    "The GreenOps knowledge "
    + "service is unavailable."
  );
}