import { useEffect, useMemo, useState } from 'react';
import { fetchReviewItems } from './reviewApi';
import './reviewDashboard.css';

const getRiskDetails = (score) => {
  if (score >= 90) {
    return { label: 'Provisional high', tone: 'critical' };
  }
  if (score >= 70) {
    return { label: 'Provisional medium', tone: 'high' };
  }
  return { label: 'Low signal', tone: 'low' };
};

export function ReviewDashboard() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;

    async function loadItems() {
      try {
        const data = await fetchReviewItems();
        if (active) {
          setItems(data);
        }
      } catch (err) {
        if (active) {
          setError(err.message || 'Unable to connect to the server.');
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    loadItems();

    return () => {
      active = false;
    };
  }, []);

  const summary = useMemo(() => {
    const flaggedCount = items.filter((item) => item.suicide_rate?.is_high_risk).length;
    return {
      total: items.length,
      flaggedCount,
    };
  }, [items]);

  return (
    <div className="app-shell">
      <header className="hero-card">
        <div>
          <p className="eyebrow">Shield Akaton</p>
          <h1>Provisional social risk review</h1>
          <p className="hero-copy">
            This dashboard displays generic screening signals from short social text. It is not a diagnosis and should only be used as a review aid.
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

      {!loading && !error && items.length === 0 && <div className="status-card">No review items were stored.</div>}

      <div className="posts-container">
        {items.map((item) => {
          const score = item.suicide_rate?.score_percentage ?? 0;
          const risk = getRiskDetails(score);
          return (
            <article key={item.id} className={`post-card ${risk.tone}`}>
              <div className="card-topline">
                <span className="risk-badge">{risk.label}</span>
                <span className="timestamp">{item.created_at || 'Unknown time'}</span>
              </div>
              <h2>{item.username || 'Unknown user'}</h2>
              <p className="post-content">{item.content || 'No content available.'}</p>
              <div className="metrics">
                <div>
                  <span className="metric-label">Model score</span>
                  <strong>{score.toFixed(2)}%</strong>
                </div>
                <div>
                  <span className="metric-label">Note</span>
                  <strong>{item.suicide_rate?.note || 'Provisional signal'}</strong>
                </div>
              </div>
            </article>
          );
        })}
      </div>
    </div>
  );
}
