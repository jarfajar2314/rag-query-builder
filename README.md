<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<br />
<div align="center">

<h3 align="center">RAG Query Builder</h3>

  <p align="center">
    A robust, dynamic natural-language-to-SQL query builder built with FastAPI, PostgreSQL, Next.js, and OpenAI. Safely convert user prompts into interactive charts and tables using catalog-driven query planning.
    <br />
    <a href="https://github.com/jarfajar2314/rag-query-builder"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/jarfajar2314/rag-query-builder">View Demo</a>
    &middot;
    <a href="https://github.com/jarfajar2314/rag-query-builder/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/jarfajar2314/rag-query-builder/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#architecture">Architecture</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About The Project

**RAG Query Builder** bridges the gap between natural language and complex relational databases. Instead of letting LLMs directly write unverified SQL, this project uses a multi-step pipeline:
1. Keyword search against an active Database Catalog.
2. Generating a structured JSON query plan via OpenAI.
3. Backend normalization (date parsing, validation).
4. Safe SQL compilation using vetted templates.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- [![Next][Next.js]][Next-url]
- [![React][React.js]][React-url]
- [![FastAPI][FastAPI]][FastAPI-url]
- [![PostgreSQL][PostgreSQL]][PostgreSQL-url]
- [![Tailwind][Tailwind]][Tailwind-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

- npm
- Python 3.12+
- PostgreSQL server

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/jarfajar2314/rag-query-builder.git
   ```
2. Navigate to the backend and install dependencies
   ```sh
   cd backend
   pip install -r requirements.txt
   ```
3. Set up backend environment variables in `.env`
   ```env
   DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
   OPENAI_API_KEY=your_key
   USE_OPENAI_INTENT=true
   ```
4. Navigate to the frontend and install dependencies
   ```sh
   cd ../frontend
   npm install
   ```
5. Set up frontend environment variables in `.env.local`
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Architecture

The project is split into two primary components:
- **[Backend](./backend/README.md)**: A FastAPI application responsible for catalog management, database interaction, intent extraction, and secure SQL generation.
- **[Frontend](./frontend/README.md)**: A Next.js application utilizing Tailwind CSS and Apache ECharts to provide a beautiful conversational interface.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

- [x] Database Catalog Sync
- [x] OpenAI Intent Extraction & Query Planning
- [x] Dynamic SQL Templates (Trend, Summary, Compare, Raw Table)
- [x] Next.js Chat Interface MVP
- [ ] Downtime Query Support
- [ ] Saved Query Results
- [ ] Vector Search (pgvector/ChromaDB)

See the [open issues](https://github.com/jarfajar2314/rag-query-builder/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Muhammad Fajar Yusuf Firdaus - mfajaryusuff@gmail.com

Project Link: [https://github.com/jarfajar2314/rag-query-builder](https://github.com/jarfajar2314/rag-query-builder)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


[contributors-shield]: https://img.shields.io/github/contributors/jarfajar2314/rag-query-builder.svg?style=for-the-badge
[contributors-url]: https://github.com/jarfajar2314/rag-query-builder/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/jarfajar2314/rag-query-builder.svg?style=for-the-badge
[forks-url]: https://github.com/jarfajar2314/rag-query-builder/network/members
[stars-shield]: https://img.shields.io/github/stars/jarfajar2314/rag-query-builder.svg?style=for-the-badge
[stars-url]: https://github.com/jarfajar2314/rag-query-builder/stargazers
[issues-shield]: https://img.shields.io/github/issues/jarfajar2314/rag-query-builder.svg?style=for-the-badge
[issues-url]: https://github.com/jarfajar2314/rag-query-builder/issues
[license-shield]: https://img.shields.io/github/license/jarfajar2314/rag-query-builder.svg?style=for-the-badge
[license-url]: https://github.com/jarfajar2314/rag-query-builder/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[FastAPI]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
[FastAPI-url]: https://fastapi.tiangolo.com/
[PostgreSQL]: https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[Tailwind]: https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white
[Tailwind-url]: https://tailwindcss.com/
