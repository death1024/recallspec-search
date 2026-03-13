import React from 'react';

export default function IdentitySpec({ spec }) {
  if (!spec) return null;

  const statusColors = {
    complete: '#48bb78',
    partial: '#ed8936',
    minimal: '#f56565'
  };

  return (
    <div style={{
      background: 'white',
      borderRadius: '16px',
      padding: '24px',
      marginBottom: '24px',
      boxShadow: '0 10px 40px rgba(0,0,0,0.1)',
      border: '1px solid #e2e8f0'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '20px' }}>
        <h3 style={{ margin: 0, fontSize: '20px', fontWeight: '600', color: '#2d3748' }}>
          Product Identity
        </h3>
        <span style={{
          marginLeft: '12px',
          padding: '6px 12px',
          backgroundColor: statusColors[spec.status],
          color: 'white',
          fontSize: '13px',
          fontWeight: '600',
          borderRadius: '20px',
          textTransform: 'uppercase'
        }}>
          {spec.status}
        </span>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '16px'
      }}>
        {spec.brand && (
          <div style={{ padding: '12px', background: '#f7fafc', borderRadius: '8px' }}>
            <div style={{ fontSize: '12px', color: '#718096', marginBottom: '4px' }}>Brand</div>
            <div style={{ fontSize: '16px', fontWeight: '600', color: '#2d3748' }}>{spec.brand}</div>
          </div>
        )}
        {spec.model && (
          <div style={{ padding: '12px', background: '#f7fafc', borderRadius: '8px' }}>
            <div style={{ fontSize: '12px', color: '#718096', marginBottom: '4px' }}>Model</div>
            <div style={{ fontSize: '16px', fontWeight: '600', color: '#2d3748' }}>{spec.model}</div>
          </div>
        )}
        {spec.vin && (
          <div style={{ padding: '12px', background: '#f7fafc', borderRadius: '8px' }}>
            <div style={{ fontSize: '12px', color: '#718096', marginBottom: '4px' }}>VIN</div>
            <div style={{ fontSize: '14px', fontWeight: '600', color: '#2d3748', fontFamily: 'monospace' }}>{spec.vin}</div>
          </div>
        )}
        {spec.upc && (
          <div style={{ padding: '12px', background: '#f7fafc', borderRadius: '8px' }}>
            <div style={{ fontSize: '12px', color: '#718096', marginBottom: '4px' }}>UPC</div>
            <div style={{ fontSize: '14px', fontWeight: '600', color: '#2d3748', fontFamily: 'monospace' }}>{spec.upc}</div>
          </div>
        )}
        {spec.category && (
          <div style={{ padding: '12px', background: '#f7fafc', borderRadius: '8px' }}>
            <div style={{ fontSize: '12px', color: '#718096', marginBottom: '4px' }}>Category</div>
            <div style={{ fontSize: '16px', fontWeight: '600', color: '#2d3748', textTransform: 'capitalize' }}>
              {spec.category.replace('_', ' ')}
            </div>
          </div>
        )}
      </div>

      {spec.missing_fields && spec.missing_fields.length > 0 && (
        <div style={{
          marginTop: '16px',
          padding: '12px 16px',
          background: '#fef5e7',
          borderLeft: '4px solid #f39c12',
          borderRadius: '8px'
        }}>
          <strong style={{ color: '#d68910', fontSize: '14px' }}>⚠️ Missing:</strong>
          <span style={{ marginLeft: '8px', color: '#7d6608' }}>
            {spec.missing_fields.join(', ')}
          </span>
        </div>
      )}
    </div>
  );
}
