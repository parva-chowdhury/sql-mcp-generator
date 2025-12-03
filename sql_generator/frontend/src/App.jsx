import React, { useState } from 'react';
import { generateSQL, sendFeedback } from './api';
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter';
import sql from 'react-syntax-highlighter/dist/esm/languages/hljs/sql';
import { docco } from 'react-syntax-highlighter/dist/esm/styles/hljs';
import './App.css';

SyntaxHighlighter.registerLanguage('sql', sql);

function App() {
  const [query, setQuery] = useState('');
  const [sqlResult, setSqlResult] = useState('');
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFeedback = async (rating) => {
    if (!sqlResult) return;
    await sendFeedback(query, sqlResult, rating);
    alert(`Thanks for your feedback! (${rating})`);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSqlResult('');

    try {
      // Send current history + new query
      const result = await generateSQL(query, history);
      setSqlResult(result);

      // Update history with new interaction
      setHistory(prev => [
        ...prev,
        { role: 'user', content: query },
        { role: 'assistant', content: result }
      ]);
    } catch (err) {
      setError('Failed to generate SQL. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const clearHistory = () => {
    setHistory([]);
    setSqlResult('');
    setQuery('');
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>AI SQL Generator</h1>
        <p>Ask questions about your data in plain English</p>
      </header>

      <main className="main-content">
        <form onSubmit={handleSubmit} className="query-form">
          <div className="input-group">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., Show me active devices by region"
              disabled={loading}
            />
            <button type="submit" disabled={loading || !query.trim()}>
              {loading ? 'Generating...' : 'Generate SQL'}
            </button>
          </div>
        </form>

        {error && <div className="error-message">{error}</div>}

        {sqlResult && (
          <div className="result-container">
            <h2>Generated SQL</h2>
            <div className="code-block">
              <SyntaxHighlighter language="sql" style={docco}>
                {sqlResult}
              </SyntaxHighlighter>
            </div>

            <div className="action-buttons">
              <button
                className="copy-btn"
                onClick={() => navigator.clipboard.writeText(sqlResult)}
              >
                Copy to Clipboard
              </button>

              <div className="feedback-buttons">
                <button
                  onClick={() => handleFeedback('Good')}
                  className="feedback-btn good"
                  title="Good Response"
                >
                  👍
                </button>
                <button
                  onClick={() => handleFeedback('Bad')}
                  className="feedback-btn bad"
                  title="Bad Response"
                >
                  👎
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
