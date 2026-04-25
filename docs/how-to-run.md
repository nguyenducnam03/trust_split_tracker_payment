# How to Run

## Prerequisites
- Node.js >= 18
- npm >= 9

## Frontend (Vue 3 + Vite)

```bash
cd frontend
npm install
npm run dev
```

Runs at `http://localhost:7777`

## Project Structure

```
trust_split_track_payment/
├── frontend/        # Vue 3 + Vite frontend
│   ├── src/
│   │   ├── components/
│   │   │   └── CreateSession.vue
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── docs/            # Documentation
```

## Notes
- Backend (FastAPI) not yet implemented
- Current demo: frontend only (CreateSession UI)
