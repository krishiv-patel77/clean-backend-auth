const stats = [
  { label: "Sources monitored", value: "12" },
  { label: "New roles today", value: "48" },
  { label: "Average detection", value: "90s" }
];

const stages = ["Saved", "Applied", "Interview", "Offer / Rejected"];

const sampleRoles = [
  {
    title: "Quant Research Intern",
    company: "Helios Capital",
    location: "New York, NY",
    freshness: "Posted 6 minutes ago"
  },
  {
    title: "Software Engineering Intern",
    company: "Signal Robotics",
    location: "San Francisco, CA",
    freshness: "Posted 14 minutes ago"
  },
  {
    title: "Investment Banking Summer Analyst",
    company: "Arcadia Partners",
    location: "Chicago, IL",
    freshness: "Posted 28 minutes ago"
  }
];

const pipeline = [
  {
    stage: "Saved",
    count: 8,
    detail: "Shortlist high-signal roles to review today."
  },
  {
    stage: "Applied",
    count: 14,
    detail: "Track outreach dates and recruiter follow-ups."
  },
  {
    stage: "Interview",
    count: 3,
    detail: "Prep kits and calendars stay linked here."
  },
  {
    stage: "Offer / Rejected",
    count: 2,
    detail: "Archive outcomes to keep focus on next steps."
  }
];

export default function App() {
  return (
    <div className="app">
      <header className="hero">
        <div>
          <p className="eyebrow">QuickReach MVP</p>
          <h1>Discover new roles first. Track everything effortlessly.</h1>
          <p className="hero-copy">
            QuickReach monitors high-signal job sources, surfaces fresh postings
            within minutes, and keeps your application pipeline clean.
          </p>
          <div className="hero-actions">
            <button className="primary">Start tracking roles</button>
            <button className="secondary">View live feed</button>
          </div>
        </div>
        <div className="hero-card">
          <h2>Live detection engine</h2>
          <p>
            Most polls exit early. We alert only when a net-new role appears — no
            noise, no duplicates.
          </p>
          <div className="stats">
            {stats.map((stat) => (
              <div key={stat.label} className="stat">
                <span>{stat.value}</span>
                <p>{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </header>

      <section className="section">
        <div className="section-header">
          <div>
            <h2>Fresh postings</h2>
            <p>See what the scraper detects first so you can apply faster.</p>
          </div>
          <span className="tag">Updated just now</span>
        </div>
        <div className="grid three">
          {sampleRoles.map((role) => (
            <article key={role.title} className="card">
              <h3>{role.title}</h3>
              <p className="muted">{role.company}</p>
              <p>{role.location}</p>
              <div className="badge">{role.freshness}</div>
            </article>
          ))}
        </div>
      </section>

      <section className="section">
        <div className="section-header">
          <div>
            <h2>Application pipeline</h2>
            <p>Minimal states keep your focus on applying, not organizing.</p>
          </div>
          <div className="stage-list">
            {stages.map((stage) => (
              <span key={stage}>{stage}</span>
            ))}
          </div>
        </div>
        <div className="grid four">
          {pipeline.map((item) => (
            <article key={item.stage} className="card">
              <div className="card-top">
                <h3>{item.stage}</h3>
                <span className="count">{item.count}</span>
              </div>
              <p className="muted">{item.detail}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section light">
        <div className="section-header">
          <div>
            <h2>Engine design</h2>
            <p>
              Every source uses the same change-detection loop for fast scaling.
            </p>
          </div>
        </div>
        <div className="grid two">
          <div className="card">
            <h3>Stateful polling</h3>
            <ul>
              <li>Conditional fetch with ETag / Last-Modified</li>
              <li>Fingerprint check to avoid false positives</li>
              <li>Delta detection on stable job IDs</li>
            </ul>
          </div>
          <div className="card">
            <h3>Notification ready</h3>
            <ul>
              <li>Events emitted only on net-new roles</li>
              <li>Email + iOS alert pipeline ready</li>
              <li>Clean tracking states synced in-app</li>
            </ul>
          </div>
        </div>
      </section>
    </div>
  );
}
