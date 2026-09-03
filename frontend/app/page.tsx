"use client";

import { FormEvent, useEffect, useRef, useState } from "react";

interface Source {
  source: string;
  page_start: number;
  page_end: number;
}

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
  retrieval_score?: number | null;
  answered?: boolean;
}

function groupSources(sources: Source[]) {
  const grouped = new Map<string, string[]>();

  sources.forEach((source) => {
    const pageRange =
      source.page_start === source.page_end
        ? `${source.page_start}`
        : `${source.page_start}-${source.page_end}`;

    const existingPages = grouped.get(source.source) || [];

    if (!existingPages.includes(pageRange)) {
      existingPages.push(pageRange);
    }

    grouped.set(source.source, existingPages);
  });

  return Array.from(grouped.entries()).map(([source, pages]) => ({
    source,
    pages,
  }));
}

function getConfidenceLabel(
  score: number | null | undefined,
  hasSources: boolean,
  answered?: boolean,
) {
  if (answered === true) {
    return {
      label: "Grounded answer",
      className: "confidence-high",
    };
  }

  if (!hasSources || score === null || score === undefined) {
    return {
      label: "Not enough information",
      className: "confidence-low",
    };
  }

  return {
    label: "Grounded answer",
    className: "confidence-high",
  };
}

export default function Home() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const [uploadedDocument, setUploadedDocument] = useState<string | null>(null);

  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  const uploadPDF = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];

    if (!file) return;

    if (!file.name.toLowerCase().endsWith(".pdf")) {
      alert("Please select a PDF file.");
      return;
    }

    setUploading(true);

    try {
      const formData = new FormData();

      formData.append("file", file);

      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to upload the PDF.");
      }

      setUploadedDocument(data.source);

      setMessages([]);
    } catch (error) {
      alert(
        error instanceof Error
          ? error.message
          : "Something went wrong while uploading.",
      );
    } finally {
      setUploading(false);

      event.target.value = "";
    }
  };

  const askMainTopic = async () => {
    if (!uploadedDocument || loading) return;

    const topicQuestion = "What is the main topic of this document?";

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: topicQuestion,
      },
    ]);

    setLoading(true);

    try {
      const response = await fetch("/api/ask-uploaded", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: topicQuestion,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to answer the question.");
      }

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources,
          retrieval_score: data.retrieval_score,
          answered: data.answered,
        },
      ]);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            error instanceof Error
              ? error.message
              : "Sorry, something went wrong.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const summarizeDocument = async () => {
    if (!uploadedDocument || loading) return;

    const summaryRequest = "Can you summarize this document?";

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: summaryRequest,
      },
    ]);

    setLoading(true);

    try {
      const response = await fetch("/api/summarize-uploaded", {
        method: "POST",
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to summarize the document.");
      }

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources,
          retrieval_score: data.retrieval_score,
          answered: data.answered,
        },
      ]);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            error instanceof Error
              ? error.message
              : "Sorry, something went wrong while summarizing.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const askQuestion = async (event: FormEvent) => {
    event.preventDefault();

    if (!question.trim() || loading) return;

    const userQuestion = question.trim();

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: userQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const endpoint = uploadedDocument ? "/api/ask-uploaded" : "/api/ask";

      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: userQuestion,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || data.error || "Something went wrong");
      }

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources,
          retrieval_score: data.retrieval_score,
          answered: data.answered,
        },
      ]);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            error instanceof Error
              ? error.message
              : "Sorry, something went wrong. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const copyAnswer = async (content: string, index: number) => {
    try {
      await navigator.clipboard.writeText(content);

      setCopiedIndex(index);

      setTimeout(() => {
        setCopiedIndex(null);
      }, 2000);
    } catch {
      alert("Unable to copy the answer.");
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <main className="app">
      <header className="header">
        <div>
          <h1>AI Knowledge Assistant</h1>

          {uploadedDocument ? (
            <div className="document-status">
              <div className="document-status-icon">📄</div>

              <div className="document-status-info">
                <span className="document-status-label">ACTIVE DOCUMENT</span>

                <span className="document-status-name">{uploadedDocument}</span>
              </div>

              <div className="document-status-dot" />
            </div>
          ) : (
            <p>Upload a PDF and ask questions about it</p>
          )}

          <label className="upload-card">
            <div className="upload-icon">{uploading ? "⏳" : "📄"}</div>

            <div className="upload-content">
              <span className="upload-title">
                {uploading
                  ? "Processing your document..."
                  : uploadedDocument
                    ? "Upload another PDF"
                    : "Upload a PDF"}
              </span>

              <span className="upload-subtitle">
                {uploading
                  ? "Preparing your document for AI search"
                  : "Add a document to your knowledge base"}
              </span>
            </div>

            <div className="upload-action">
              {uploading ? "Processing" : "Browse"}
            </div>

            <input
              type="file"
              accept=".pdf,application/pdf"
              onChange={uploadPDF}
              disabled={uploading}
              hidden
            />
          </label>
        </div>

        {messages.length > 0 && (
          <button className="clear-button" onClick={clearChat}>
            Clear Chat
          </button>
        )}
      </header>

      <section className="chat-container">
        {messages.length === 0 ? (
          <div className="welcome">
            <div className="welcome-icon">🤖</div>

            <h2>How can I help you?</h2>

            <p>Ask me anything based on the documents in my knowledge base.</p>

            <div className="suggestions">
              <button
                onClick={askMainTopic}
                disabled={!uploadedDocument || loading}
              >
                What is the main topic?
              </button>

              <button
                onClick={summarizeDocument}
                disabled={!uploadedDocument || loading}
              >
                Summarize this document
              </button>
            </div>
          </div>
        ) : (
          <div className="messages">
            {messages.map((message, index) => (
              <div key={index} className={`message ${message.role}`}>
                <div className="message-label">
                  {message.role === "user" ? "You" : "AI Assistant"}
                </div>

                {message.role === "assistant" &&
                  (() => {
                    const confidence = getConfidenceLabel(
                      message.retrieval_score,
                      Boolean(message.sources?.length),
                      message.answered,
                    );

                    return (
                      <div
                        className={`confidence-badge ${confidence.className}`}
                      >
                        {confidence.className === "confidence-high"
                          ? "🟢"
                          : "🔴"}{" "}
                        {confidence.label}
                      </div>
                    );
                  })()}

                <div className="message-content">{message.content}</div>

                {message.role === "assistant" && (
                  <button
                    className="copy-button"
                    onClick={() => copyAnswer(message.content, index)}
                  >
                    {copiedIndex === index ? "✅ Copied!" : "📋 Copy"}
                  </button>
                )}

                {message.role === "assistant" &&
                  message.sources &&
                  message.sources.length > 0 && (
                    <div className="sources">
                      <h4>📚 Sources</h4>

                      {groupSources(message.sources).map((source) => (
                        <div className="source" key={source.source}>
                          <div>📄 {source.source}</div>

                          <div className="source-pages">
                            Pages: {source.pages.join(", ")}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
              </div>
            ))}

            {loading && (
              <div className="message assistant">
                <div className="message-label">AI Assistant</div>

                <div className="typing">
                  Thinking<span>.</span>
                  <span>.</span>
                  <span>.</span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        )}
      </section>

      <form className="input-area" onSubmit={askQuestion}>
        <input
          type="text"
          placeholder="Ask a question about your knowledge base..."
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          disabled={loading}
        />

        <button type="submit" disabled={loading || !question.trim()}>
          {loading ? "Thinking..." : "Send"}
        </button>
      </form>
    </main>
  );
}
