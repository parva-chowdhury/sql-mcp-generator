import React, { useState } from 'react';
import { generateSQL, sendFeedback, executeSQL } from './api';
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
  const [executing, setExecuting] = useState(false);
  const [executionResult, setExecutionResult] = useState(null);
  const [error, setError] = useState('');

  const handleFeedback = async (rating) => {
    if (!sqlResult) return;
    await sendFeedback(query, sqlResult, rating);
    alert(`Thanks for your feedback! (${rating})`);
  };

  const handleExecute = async () => {
    if (!sqlResult) return;
    setExecuting(true);
    setExecutionResult(null);
    try {
      const result = await executeSQL(sqlResult);
      setExecutionResult(result);
    } catch (err) {
      console.error("Execution error:", err);
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to execute SQL.';
      setError(`Execution Failed: ${errorMessage}`);
    } finally {
      setExecuting(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSqlResult('');
    setExecutionResult(null);

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
    setExecutionResult(null);
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

              <button
                className="execute-btn"
                onClick={handleExecute}
                disabled={executing}
              >
                {executing ? 'Executing...' : '▶ Run Query'}
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

        {executionResult && (
          <div className="execution-result">
            <h2>Query Results</h2>
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    {executionResult.columns.map((col, index) => (
                      <th key={index}>{col}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {executionResult.rows.map((row, rowIndex) => (
                    <tr key={rowIndex}>
                      {executionResult.columns.map((col, colIndex) => (
                        <td key={colIndex}>{row[col]}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <p className="result-meta">
              Status: {executionResult.status} | Query ID: {executionResult.query_id}
            </p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
