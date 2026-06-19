# RAG Query Builder - Frontend

This is the Next.js frontend application for the RAG Query Builder. It provides a simple chat interface that allows users to converse with their database.

## Features

- **Natural Language Chat**: Send prompts to the FastAPI backend.
- **Dynamic Charts**: Renders ECharts (Bar, Line) based on the JSON response from the backend.
- **KPI Cards**: Renders styled metric cards for summary intents.
- **Data Tables**: Renders raw data rows natively.
- **Developer Previews**: Collapsible JSON and SQL views to verify the backend's query plan.

## Stack

- Next.js (App Router)
- React
- TypeScript
- Tailwind CSS
- Apache ECharts (`echarts-for-react`)

## Development

First, set up your `.env.local` to point to the FastAPI backend:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Then, run the development server:

```bash
npm run dev
# Server will start on http://localhost:3007
```

Open [http://localhost:3007](http://localhost:3007) with your browser to see the result.
