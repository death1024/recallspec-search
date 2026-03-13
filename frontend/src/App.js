import React, { useState } from 'react';
import axios from 'axios';
import IdentitySpec from './components/IdentitySpec';
import ActionCard from './components/ActionCard';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/v1/search', {
        query: query
      });
      setResult(response.data);
    } catch (error) {
      console.error('Search failed:', error);
    }
    setLoading(false);
  };

  const handleImageSearch = async () => {
    if (!image) return;
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('image', image);
      if (query) formData.append('query', query);

      const response = await axios.post('http://localhost:8000/api/v1/search/image', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(response.data);
    } catch (error) {
      console.error('Image search failed:', error);
    }
    setLoading(false);
  };

  return (
    <div className="app-container">
      <div className="header">
        <h1>🔍 RecallSpec Search</h1>
        <p>Verify product safety with official recall data</p>
      </div>

      <div className="search-card">
        <input
          type="text"
          className="search-input"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter VIN, UPC, brand, or product description..."
        />

        <div className="file-upload">
          <div className="file-input-wrapper">
            <input
              type="file"
              id="file-input"
              accept="image/*"
              onChange={(e) => setImage(e.target.files[0])}
            />
            <label htmlFor="file-input" className="file-input-label">
              📷 {image ? image.name : 'Upload Product Image'}
            </label>
          </div>
        </div>

        <div className="button-group">
          <button
            className="btn btn-primary"
            onClick={handleSearch}
            disabled={loading}
          >
            {loading ? '⏳ Searching...' : '🔎 Search Text'}
          </button>

          <button
            className="btn btn-secondary"
            onClick={handleImageSearch}
            disabled={loading || !image}
          >
            {loading ? '⏳ Processing...' : '📸 Search Image'}
          </button>
        </div>
      </div>

      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <p>Analyzing product and checking recall databases...</p>
        </div>
      )}

      {result && !loading && (
        <div className="results-container">
          <IdentitySpec spec={result.identity_spec} />

          <div className="result-card">
            <h2 style={{ marginBottom: '20px', color: '#2d3748' }}>Match Result</h2>
            <div style={{
              padding: '20px',
              background: result.resolution_spec.match_status === 'exact_match' ? '#fed7d7' : '#f7fafc',
              border: `2px solid ${result.resolution_spec.match_status === 'exact_match' ? '#fc8181' : '#e2e8f0'}`,
              borderRadius: '12px'
            }}>
              <p style={{ fontSize: '18px', fontWeight: '600', marginBottom: '12px' }}>
                Status: {result.resolution_spec.match_status.replace('_', ' ').toUpperCase()}
              </p>

              {result.resolution_spec.uncertainties && result.resolution_spec.uncertainties.length > 0 && (
                <div style={{
                  marginTop: '16px',
                  padding: '16px',
                  backgroundColor: '#fef5e7',
                  borderLeft: '4px solid #f39c12',
                  borderRadius: '8px'
                }}>
                  <strong style={{ color: '#d68910' }}>⚠️ Uncertainties:</strong>
                  <ul style={{ marginTop: '8px', marginLeft: '20px' }}>
                    {result.resolution_spec.uncertainties.map((u, i) => (
                      <li key={i} style={{ marginBottom: '4px' }}>{u}</li>
                    ))}
                  </ul>
                </div>
              )}

              <ActionCard
                actionCard={result.resolution_spec.action_card}
                riskLevel={result.resolution_spec.risk_level}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
