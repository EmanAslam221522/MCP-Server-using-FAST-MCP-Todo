'use client';

import { useState, useEffect } from 'react';

export default function Home() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      // Use backend service name from docker-compose
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001';
      const response = await fetch(`${apiUrl}/api/message`);

      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }

      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Next.js Frontend</h1>

      <div style={{
        marginTop: '2rem',
        padding: '1rem',
        border: '1px solid #ddd',
        borderRadius: '8px',
        backgroundColor: '#f5f5f5'
      }}>
        <h2>API Response:</h2>

        {loading && <p>Loading...</p>}

        {error && (
          <p style={{ color: 'red' }}>Error: {error}</p>
        )}

        {data && (
          <div>
            <p><strong>Message:</strong> {data.message}</p>
            <p><strong>Timestamp:</strong> {data.timestamp}</p>
            <p><strong>Status:</strong> {data.status}</p>
          </div>
        )}

        <button
          onClick={fetchData}
          style={{
            marginTop: '1rem',
            padding: '0.5rem 1rem',
            backgroundColor: '#0070f3',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Refresh Data
        </button>
      </div>
    </main>
  );
}