export function CustomTooltip({ active, payload, label }) {
  if (active && payload && payload.length) {
    return (
      <div 
        style={{
          backgroundColor: '#0f172a',
          border: '1px solid #334155',
          borderRadius: '8px',
          padding: '12px',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.3)',
          color: '#fff',
        }}
      >
        <p 
          style={{ 
            color: '#cbd5e1', 
            marginBottom: '8px',
            fontWeight: '600',
            fontSize: '14px',
          }}
        >
          {label}
        </p>
        {payload.map((entry, index) => (
          <p 
            key={index} 
            style={{ 
              color: '#fff',
              fontSize: '13px',
              margin: '4px 0',
            }}
          >
            {entry.name || 'count'} : {entry.value}
          </p>
        ))}
      </div>
    );
  }
  return null;
}

