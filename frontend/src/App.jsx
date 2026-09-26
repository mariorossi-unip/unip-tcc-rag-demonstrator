import { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [selectedMessageId, setSelectedMessageId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function askQuestion(event) {
    event?.preventDefault();

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || loading) {
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: trimmedQuestion,
          n_results: 5,
        }),
      });

      if (!response.ok) {
        const body = await response.text();

        throw new Error(
          body || `Request failed with status ${response.status}`
        );
      }

      const data = await response.json();

      const newMessage = {
        id: crypto.randomUUID(),
        question: data.question,
        answer: data.answer,
        results: data.results,
        context: data.context,
      };

      setMessages((previousMessages) => [
        ...previousMessages,
        newMessage,
      ]);

      setSelectedMessageId(newMessage.id);
      setQuestion("");
    } catch (err) {
      console.error(err);
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      askQuestion();
    }
  }

  function selectMessage(messageId) {
    setSelectedMessageId(messageId);
  }

  function clearConversation() {
    setMessages([]);
    setSelectedMessageId(null);
    setError("");
  }

  const selectedMessage =
    messages.find((message) => message.id === selectedMessageId) ||
    messages[messages.length - 1] ||
    null;

  return (
    <div className="app">
      <header className="topbar">
        <div>
          <p className="eyebrow">TCC - Mario Rossi Bracco da Costa [ 2301193, Ciência da Computação ]</p>
          <h1>RAG Demonstrator</h1>
        </div>

        <div className="topbar-actions">
          {messages.length > 0 && (
            <button
              className="clear-button"
              onClick={clearConversation}
            >
              Clear session
            </button>
          )}

          <div className="status">
            <span className="status-dot" />
            API connected
          </div>
        </div>
      </header>

      <main className="workspace">
        <section className="chat-panel">
          <div className="panel-header">
            <div>
              <span className="panel-number">01</span>
              <h2>Conversation</h2>
            </div>

            <p>
              Ask questions and inspect the RAG execution associated with
              each response.
            </p>
          </div>

          <div className="conversation">
            {messages.length === 0 &&
              !loading &&
              !error && (
                <div className="empty-state">
                  <div className="empty-icon">RAG</div>

                  <h3>Ask the knowledge base</h3>

                  <p>
                    The system will retrieve relevant document excerpts,
                    build a context and use it to generate an answer.
                  </p>
                </div>
              )}

            {messages.map((message) => (
              <ConversationMessage
                key={message.id}
                message={message}
                selected={message.id === selectedMessageId}
                onSelect={() => selectMessage(message.id)}
              />
            ))}

            {loading && (
              <div className="message assistant-message loading-message">
                <div className="message-header">
                  <span className="avatar assistant-avatar">AI</span>
                  <span>Assistant</span>
                </div>

                <div className="thinking">
                  <span />
                  <span />
                  <span />
                  Retrieving documents and generating response
                </div>
              </div>
            )}

            {error && (
              <div className="error-box">
                <strong>Request failed</strong>
                <p>{error}</p>
              </div>
            )}
          </div>

          <form className="question-form" onSubmit={askQuestion}>
            <textarea
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask something about the knowledge base..."
              rows={3}
            />

            <div className="question-actions">
              <span>
                Enter to send · Shift + Enter for a new line
              </span>

              <button
                type="submit"
                disabled={loading || !question.trim()}
              >
                {loading ? "Processing..." : "Ask"}
              </button>
            </div>
          </form>
        </section>

        <section className="inspector-panel">
          <div className="panel-header inspector-header">
            <div>
              <span className="panel-number">02</span>
              <h2>RAG Inspector</h2>
            </div>

            <p>
              Inspect the information retrieved and passed to the language
              model for the selected response.
            </p>
          </div>

          {!selectedMessage ? (
            <div className="inspector-empty">
              <span>No RAG execution yet</span>

              <p>
                Submit a question to visualize the retrieval and generation
                pipeline.
              </p>
            </div>
          ) : (
            <RagInspector message={selectedMessage} />
          )}
        </section>
      </main>
    </div>
  );
}

function ConversationMessage({ message, selected, onSelect }) {
  return (
    <div
      className={`conversation-entry ${
        selected ? "conversation-entry-selected" : ""
      }`}
      onClick={onSelect}
    >
      <div className="message user-message">
        <div className="message-header">
          <span className="avatar user-avatar">U</span>
          <span>You</span>
        </div>

        <div className="message-content">
          {message.question}
        </div>
      </div>

      <div className="message assistant-message">
        <div className="message-header">
          <span className="avatar assistant-avatar">AI</span>
          <span>Assistant</span>
        </div>

        <div className="message-content">
          {message.answer}
        </div>
      </div>

      <div className="message-inspector-hint">
        <span>↗</span>
        Inspect RAG execution for this response
      </div>
    </div>
  );
}

function RagInspector({ message }) {
  return (
    <div className="inspector-content">
      <Pipeline />

      <section className="inspector-section">
        <SectionTitle
          number="1"
          title="User query"
          description="Original question submitted to the system."
        />

        <div className="query-box">
          {message.question}
        </div>
      </section>

      <section className="inspector-section">
        <SectionTitle
          number="2"
          title="Retrieved documents"
          description={`${message.results?.length ?? 0} chunks selected from the vector database.`}
        />

        <div className="retrieval-list">
          {message.results?.map((result, index) => (
            <RetrievedChunk
              key={result.id || index}
              result={result}
              index={index}
            />
          ))}
        </div>
      </section>

      <section className="inspector-section">
        <SectionTitle
          number="3"
          title="Constructed context"
          description="Content assembled by the backend before generation."
        />

        <details className="context-details">
          <summary>
            View complete context sent to the LLM
          </summary>

          <pre className="context-box">
            {message.context}
          </pre>
        </details>
      </section>

      <section className="inspector-section">
        <SectionTitle
          number="4"
          title="Generated answer"
          description="Final response produced using the retrieved context."
        />

        <div className="generated-answer">
          {message.answer}
        </div>
      </section>
    </div>
  );
}

function Pipeline() {
  return (
    <div className="pipeline">
      <PipelineStep number="1" label="Query" />
      <span className="pipeline-arrow">→</span>

      <PipelineStep number="2" label="Retrieval" />
      <span className="pipeline-arrow">→</span>

      <PipelineStep number="3" label="Context" />
      <span className="pipeline-arrow">→</span>

      <PipelineStep number="4" label="Generation" />
    </div>
  );
}

function PipelineStep({ number, label }) {
  return (
    <div className="pipeline-step">
      <span>{number}</span>
      <strong>{label}</strong>
    </div>
  );
}

function SectionTitle({ number, title, description }) {
  return (
    <div className="section-title">
      <span>{number}</span>

      <div>
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

function RetrievedChunk({ result, index }) {
  const metadata = result.metadata || {};

  const source =
    metadata.source ||
    metadata.filename ||
    metadata.paper ||
    "Unknown document";

  const page = metadata.page ?? "N/A";
  const chunkIndex = metadata.chunk_index ?? "N/A";

  const distance =
    typeof result.distance === "number"
      ? result.distance.toFixed(4)
      : "N/A";

  return (
    <details className="retrieved-chunk">
      <summary>
        <div className="chunk-summary">
          <div className="chunk-rank">
            {index + 1}
          </div>

          <div className="chunk-source">
            <strong>{source}</strong>

            <span>
              Page {page} · Chunk {chunkIndex}
            </span>
          </div>

          <div className="distance">
            <span>Distance</span>
            <strong>{distance}</strong>
          </div>
        </div>
      </summary>

      <div className="chunk-content">
        <div className="chunk-metadata">
          <div>
            <span>Source</span>
            <strong>{source}</strong>
          </div>

          <div>
            <span>Page</span>
            <strong>{page}</strong>
          </div>

          <div>
            <span>Chunk</span>
            <strong>{chunkIndex}</strong>
          </div>

          <div>
            <span>Vector distance</span>
            <strong>{distance}</strong>
          </div>
        </div>

        <div className="chunk-text">
          {result.text}
        </div>
      </div>
    </details>
  );
}

export default App;