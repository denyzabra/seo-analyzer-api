# SEO Analyzer API

**A scalable, containerized backend API for comprehensive SEO analysis, built with Django, Docker, Celery, PostgreSQL, and Hugging Face LLMs.**

## Features

- Analyze website/content for SEO best practices
- Keyword density, readability scoring, and automated recommendations
- Async background jobs (Celery, Redis)
- RESTful API endpoints for integration
- Config-ready for cloud deployment (Docker, Railway, Heroku, etc.)

## Tech Stack

- **Python / Django:** backend API and business logic
- **Celery + Redis:** background task queue for scalable async processing
- **PostgreSQL:** relational database (in Docker)
- **LangChain & HuggingFace:** built-in LLM support for advanced recommendations
- **Docker / docker-compose:** manage and deploy app & services easily

## Getting Started

### Prerequisites

- Docker & Docker Compose installed
- Python 3.10+ (for local dev)


### Local Setup

1. **Clone the repo:**
