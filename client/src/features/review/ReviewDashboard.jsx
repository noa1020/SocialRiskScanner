import { useEffect, useMemo, useState } from 'react';
import { fetchReviewItems } from './reviewApi';
import './reviewDashboard.css';

export function ReviewDashboard() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;

    async function loadItems() {
      try {
        const data = await fetchReviewItems();
        if (active) setItems(data);
      } catch (err) {
        if (active) setError(err.message || 'Unable to connect to the server.');
      } finally {
        if (active) setLoading(false);
      }
    }

    loadItems();

    return () => {
      active = false;
    };
  }, []);

  const summary = useMemo(() => {
    const flaggedCount = items.filter(
      (item) => item.suicide_rate.risk_level  === 'high'
    ).length;

    return {
      total: items.length,
      flaggedCount,
    };
  }, [items]);

  const getTone = (riskLevel) => {
    if (riskLevel === 'high') return 'critical';
    if (riskLevel === 'medium') return 'high';
    return 'low';
  };

  const getLabel = (riskLevel) => {
    if (riskLevel === 'high') return 'High risk';
    if (riskLevel === 'medium') return 'Medium risk';
    return 'Low signal';
  };

  return (
    <div className="app-shell">
      <header className="hero-card">
        <div>
          <p className="eyebrow">Social Risk Scanner</p>
          <h1>Provisional social risk review</h1>
          <p className="hero-copy">
            This dashboard displays generic screening signals from short social text.
            It is not a diagnosis.
          </p>
        </div>

        <div className="summary-panel">
          <div>
            <strong>{summary.total}</strong>
            <span>items reviewed</span>
          </div>
          <div>
            <strong>{summary.flaggedCount}</strong>
            <span>flagged items</span>
          </div>
        </div>
      </header>

      {loading && <div className="status-card">Loading review items…</div>}
      {error && <div className="status-card error">{error}</div>}

      {!loading && !error && items.length === 0 && (
        <div className="status-card">No review items were stored.</div>
      )}

      <div className="posts-container">
        {items.map((item) => {
          const rate = item.suicide_rate || {};

          const tone = getTone(rate.risk_level);
          const label = getLabel(rate.risk_level);

          return (
            <article key={item.id} className={`post-card ${tone}`}>
              <div className="card-topline">
                <span className="risk-badge">{label}</span>
                <span className="timestamp">
                  {item.created_at || 'Unknown time'}
                </span>
              </div>

              <h2>{item.username || 'Unknown user'}</h2>

              <p className="post-content">
                {item.content || 'No content available.'}
              </p>

            </article>
          );
        })}
      </div>
    </div>
  );
}