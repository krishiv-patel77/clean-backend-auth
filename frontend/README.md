# QuickReach Frontend

A lightweight React + Vite interface that mirrors the MVP experience for QuickReach.
It is intentionally simple and readable so it can evolve alongside the scraper and
tracking APIs.

## What’s Included
- Clean landing layout for discovery + tracking.
- Highlighted detection stats and pipeline cards.
- Minimal styling in a single CSS file for quick iteration.

## Getting Started

```bash
cd frontend
npm install
npm run dev
```

Then open `http://localhost:5173`.

## Scripts
- `npm run dev` — start the local dev server.
- `npm run build` — create a production build.
- `npm run preview` — preview the production build.
- `npm run lint` — run ESLint.

## Next Steps
- Wire the stats and job list to real API responses.
- Replace sample pipeline data with live application states.
- Add authentication once backend endpoints are ready.
