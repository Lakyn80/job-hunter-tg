# Job Hunter TG

Telegram-based job aggregation and ingestion backend focused on collecting, filtering, and storing IT job offers from multiple Telegram channels.

The project is built as a production-oriented backend service with clean modular architecture, database persistence, and CI support. It is designed to support both automated ingestion and manual post-processing workflows (e.g. translation and curation).

---

## Overview

Job Hunter TG continuously ingests job postings from selected Telegram channels, normalizes the data, and stores only relevant offers based on configurable rules.

Core goals:
- automated multi-channel ingestion
- strict deduplication and data consistency
- selective job filtering (avoid noise)
- clean logs and deterministic behavior
- testability and containerized deployment

---

## Architecture

Telegram Channels  
→ Ingestion Layer (scripts / collectors)  
→ Normalization & Filtering  
→ Database (SQLAlchemy ORM)  
→ API / Internal Services  
→ Optional manual workflows (translation, review)

The system is designed to run continuously as a backend service.

---

## Backend

Tech stack:
- Python 3.11+
- SQLAlchemy
- pytest
- Docker
- Telegram API (client-based ingestion)

Key features:
- Multi-channel Telegram ingestion
- Duplicate protection at database level
- Stable SQLAlchemy model definitions
- Selective job ingestion rules
- Clean, structured logging
- Health checks covered by tests

---

## Database

- SQLAlchemy ORM
- Explicit handling of duplicate table definitions
- Persistent storage of channels and job offers
- Database-agnostic design (SQLite for dev, easily replaceable)

---

## Scripts & Workflows

- Background ingestion scripts
- Selective job saving (only relevant offers stored)
- Manual translation and review workflow supported
- Separation between ingestion logic and processing logic

---

## Testing & CI

- Unit tests with pytest
- Coverage tracking
- GitHub Actions pipeline
- Docker build verification in CI
- Health checks validated via tests

---

## Configuration & Security

- Secrets and credentials handled via environment variables
- `.env` files excluded from version control
- Example environment configuration provided
- No sensitive data committed to the repository

---

## Repository Structure

app/ – application logic and models  
core/ – shared core utilities  
data/ – ingestion and processing logic  
scripts/ – job ingestion and workflow scripts  
tests/ – pytest-based test suite  
.github/workflows/ – CI pipelines  
Dockerfile / docker-compose.yml – containerized runtime  
README.md

---

## Project Status

Active development.

Planned extensions:
- Smarter job classification
- Language detection and auto-translation pipeline
- Web or dashboard interface for browsing jobs
- Scheduling and alerting

---

## Author

Developed and maintained by Lukas Krumpach  
Backend-focused Python developer
