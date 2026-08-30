"use client";

import { FormEvent, useState } from "react";

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
      const response = await fetch("/api/ask", {
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
        throw new Error(data.error || "Something went wrong");
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
            "Sorry, I couldn't connect to the AI Knowledge Assistant. Please try again.",
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
          <p>Ask questions about your uploaded knowledge base</p>
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
            <p>
              Ask me anything based on the documents in my knowledge base.
            </p>

            <div className="suggestions">
              <button
                onClick={() =>
                  setQuestion("Explain Euclid's algorithm for finding GCD.")
                }
              >
                Explain Euclid's algorithm
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
              <div
                key={index}
                className={`message ${message.role}`}
              >
                <div className="message-label">
                  {message.role === "user" ? "You" : "AI Assistant"}
                </div>

                <div className="message-content">
                  {message.content}
                </div>

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
                  Thinking<span>.</span><span>.</span><span>.</span>
                </div>
              </div>
            )}
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