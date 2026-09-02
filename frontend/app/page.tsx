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
}

export default function Home() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

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

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <main className="app">
      <header className="header">
        <div>
          <h1>AI Knowledge Assistant</h1>

          <p>
            {uploadedDocument
              ? `Currently using: ${uploadedDocument}`
              : "Upload a PDF and ask questions about it"}
          </p>

          <label className="upload-button">
            {uploading ? "Processing PDF..." : "📄 Upload PDF"}

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
                onClick={() =>
                  setQuestion("Explain Euclid's algorithm for finding GCD.")
                }
              >
                Explain Euclid&apos;s algorithm
              </button>

              <button
                onClick={() =>
                  setQuestion("What is the efficiency of Euclid's algorithm?")
                }
              >
                Explain algorithm efficiency
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

                <div className="message-content">{message.content}</div>

                {message.role === "assistant" &&
                  message.sources &&
                  message.sources.length > 0 && (
                    <div className="sources">
                      <h4>📚 Sources</h4>

                      {message.sources.map((source, sourceIndex) => (
                        <div className="source" key={sourceIndex}>
                          📄 {source.source} — Page{" "}
                          {source.page_start === source.page_end
                            ? source.page_start
                            : `${source.page_start}-${source.page_end}`}
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
