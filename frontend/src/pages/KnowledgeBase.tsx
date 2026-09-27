import {
  useEffect,
  useState,
} from "react";

import {
  askDocumentation,
  deleteDocument,
  getDocuments,
  uploadDocument,
} from "../services/rag";

import type {
  DocumentResponse,
  RAGAskResponse,
} from "../types/rag";


function KnowledgeBase() {
  const [documents, setDocuments] =
    useState<DocumentResponse[]>([]);

  const [selectedFile, setSelectedFile] =
    useState<File | null>(null);

  const [question, setQuestion] =
    useState("");

  const [answer, setAnswer] =
    useState<RAGAskResponse | null>(
      null,
    );

  const [
    documentsLoading,
    setDocumentsLoading,
  ] = useState(true);

  const [
    uploading,
    setUploading,
  ] = useState(false);

  const [
    asking,
    setAsking,
  ] = useState(false);

  const [error, setError] =
    useState<string | null>(null);


  useEffect(() => {
    let cancelled = false;


    async function loadInitialDocuments() {
      try {
        const result =
          await getDocuments();

        if (!cancelled) {
          setDocuments(result);
        }

      } catch {
        if (!cancelled) {
          setError(
            "Unable to load documents.",
          );
        }

      } finally {
        if (!cancelled) {
          setDocumentsLoading(false);
        }
      }
    }


    void loadInitialDocuments();


    return () => {
      cancelled = true;
    };
  }, []);


  async function refreshDocuments() {
    try {
      const result =
        await getDocuments();

      setDocuments(result);

    } catch {
      setError(
        "Unable to refresh documents.",
      );
    }
  }


  async function handleUpload(
    event:
      React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    if (!selectedFile) {
      setError(
        "Please choose a document first.",
      );

      return;
    }


    setUploading(true);
    setError(null);


    try {
      await uploadDocument(
        selectedFile,
      );

      setSelectedFile(null);

      await refreshDocuments();

    } catch (uploadError) {

      setError(
        uploadError instanceof Error
          ? uploadError.message
          : "Document upload failed.",
      );

    } finally {
      setUploading(false);
    }
  }


  async function handleDelete(
    documentId: number,
  ) {
    setError(null);


    try {
      await deleteDocument(
        documentId,
      );

      await refreshDocuments();

    } catch {
      setError(
        "Unable to delete document.",
      );
    }
  }


  async function handleAsk(
    event:
      React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    if (!question.trim()) {
      return;
    }


    setAsking(true);
    setError(null);
    setAnswer(null);


    try {
      const result =
        await askDocumentation({
          question:
            question.trim(),

          top_k: 5,
        });

      setAnswer(result);

    } catch (askError) {

      setError(
        askError instanceof Error
          ? askError.message
          : "Unable to answer question.",
      );

    } finally {
      setAsking(false);
    }
  }


  return (
    <main>

      <h1>
        Knowledge Base
      </h1>

      <p>
        Upload architecture documents,
        runbooks, deployment files and
        technical documentation for
        grounded GreenOps AI answers.
      </p>


      {error && (
        <div className="error-message">
          {error}
        </div>
      )}


      <section className="knowledge-section">

        <h2>
          Upload Document
        </h2>


        <form
          className="document-upload-form"
          onSubmit={handleUpload}
        >

          <input
            type="file"
            accept={
              ".txt,.md,.yaml,.yml,"
              + ".json,.pdf"
            }
            onChange={(event) => {
              const file =
                event.target.files?.[0]
                ?? null;

              setSelectedFile(file);
            }}
          />


          {selectedFile && (
            <p>
              Selected:{" "}
              <strong>
                {selectedFile.name}
              </strong>
            </p>
          )}


          <button
            type="submit"
            disabled={
              uploading
              || !selectedFile
            }
          >
            {uploading
              ? "Uploading..."
              : "Upload Document"}
          </button>

        </form>

      </section>


      <section className="knowledge-section">

        <div className="section-heading">

          <h2>
            Documents
          </h2>


          <button
            onClick={
              refreshDocuments
            }
          >
            Refresh
          </button>

        </div>


        {documentsLoading ? (
          <p>
            Loading documents...
          </p>

        ) : documents.length === 0 ? (
          <p>
            No documents uploaded yet.
          </p>

        ) : (
          <div className="document-list">

            {documents.map(
              (document) => (

                <article
                  key={document.id}
                  className="document-card"
                >

                  <div>

                    <strong>
                      {document.filename}
                    </strong>

                    <p>
                      {
                        document
                          .chunk_count
                      }{" "}
                      chunks
                    </p>

                    <small>
                      {
                        document
                          .content_type
                      }
                    </small>

                  </div>


                  <button
                    onClick={() =>
                      handleDelete(
                        document.id,
                      )
                    }
                  >
                    Delete
                  </button>

                </article>
              ),
            )}

          </div>
        )}

      </section>


      <section className="knowledge-section">

        <h2>
          Ask Documentation
        </h2>


        <form
          className="knowledge-question-form"
          onSubmit={handleAsk}
        >

          <textarea
            rows={5}
            required
            placeholder={
              "Example: What is the "
              + "minimum replica count "
              + "for the payment service?"
            }
            value={question}
            onChange={(event) =>
              setQuestion(
                event.target.value,
              )
            }
          />


          <button
            type="submit"
            disabled={asking}
          >
            {asking
              ? "Searching..."
              : "Ask GreenOps"}
          </button>

        </form>


        {answer && (
          <div className="rag-answer">

            <h3>
              GreenOps Answer
            </h3>


            <div className="ai-response">
              {answer.answer}
            </div>


            <p>
              AI Provider:{" "}
              <strong>
                {answer.provider}
              </strong>
            </p>


            <h3>
              Sources
            </h3>


            {answer.sources.length === 0 ? (
              <p>
                No relevant sources found.
              </p>

            ) : (
              <div className="source-list">

                {answer.sources.map(
                  (
                    source,
                    index,
                  ) => (

                    <article
                      className="source-card"
                      key={
                        `${source.document_id}`
                        + `-${source.chunk_index}`
                        + `-${index}`
                      }
                    >

                      <strong>
                        {
                          source
                            .filename
                        }
                      </strong>


                      <p>
                        Chunk:{" "}
                        {
                          source
                            .chunk_index
                        }
                      </p>


                      <p>
                        Similarity:{" "}
                        {(
                          source.similarity
                          * 100
                        ).toFixed(1)}
                        %
                      </p>


                      <details>

                        <summary>
                          View retrieved text
                        </summary>

                        <p>
                          {
                            source
                              .content
                          }
                        </p>

                      </details>

                    </article>
                  ),
                )}

              </div>
            )}

          </div>
        )}

      </section>

    </main>
  );
}


export default KnowledgeBase;