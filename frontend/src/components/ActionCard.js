import React from 'react';

export default function ActionCard({ actionCard, riskLevel }) {
  if (!actionCard) return null;

  const riskColors = {
    high: '#e53e3e',
    medium: '#dd6b20',
    low: '#38a169',
    unknown: '#718096'
  };

  const riskBg = {
    high: '#fff5f5',
    medium: '#fffaf0',
    low: '#f0fff4',
    unknown: '#f7fafc'
  };

  return (
    <div style={{
      border: `3px solid ${riskColors[riskLevel]}`,
      padding: '24px',
      marginTop: '24px',
      backgroundColor: riskBg[riskLevel],
      borderRadius: '12px',
      boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
    }}>
      <h3 style={{
        color: riskColors[riskLevel],
        marginTop: 0,
        fontSize: '20px',
        fontWeight: '700',
        marginBottom: '16px'
      }}>
        ⚠️ Action Required - Risk: {riskLevel.toUpperCase()}
      </h3>

      <div style={{
        padding: '16px 20px',
        backgroundColor: 'white',
        borderLeft: `5px solid ${riskColors[riskLevel]}`,
        marginBottom: '20px',
        borderRadius: '8px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.05)'
      }}>
        <strong style={{ fontSize: '16px', color: '#2d3748' }}>
          {actionCard.immediate_action}
        </strong>
      </div>

      <h4 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '12px', color: '#2d3748' }}>
        📋 Next Steps:
      </h4>
      <ol style={{ marginLeft: '20px', lineHeight: '1.8' }}>
        {actionCard.next_steps.map((step, i) => (
          <li key={i} style={{
            marginBottom: '10px',
            color: '#4a5568',
            fontSize: '15px'
          }}>{step}</li>
        ))}
      </ol>

      <div style={{
        marginTop: '20px',
        padding: '14px 18px',
        backgroundColor: 'white',
        borderRadius: '8px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.05)'
      }}>
        <a
          href={actionCard.official_source}
          target="_blank"
          rel="noopener noreferrer"
          style={{
            color: '#667eea',
            fontWeight: '600',
            textDecoration: 'none',
            fontSize: '15px'
          }}
        >
          📄 View Official Source →
        </a>
      </div>
    </div>
  );
}
