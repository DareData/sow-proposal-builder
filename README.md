# DareData Proposal Builder

A beautiful Streamlit application for creating project proposals with a consistent format.

## Features

- User-friendly form interface for capturing proposal information
- Automatic generation of formatted Markdown proposals
- Containerized for easy deployment

## Project Structure

```
.
├── src/
│   └── app.py                  # Streamlit application
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker build instructions
├── pyproject.toml              # Poetry dependencies
└── README.md                   # Project documentation
```

## Usage

### Option 1: Using Docker

1. Make sure you have Docker and Docker Compose installed
2. Run the start script:

```bash
docker-compose build
docker-compose up -d
```

3. Access the application at http://localhost:8501

### Option 2: Running Locally with Poetry

1. Install Poetry (https://python-poetry.org/docs/#installation)
2. Install dependencies:

```bash
poetry install
```

3. Start the backend API

```bash
poetry run python src/api.py
```

4. Run the Frontend:

```bash
poetry run streamlit run src/app.py
```

## Fields Included

- Client name
- National/International scope
- Proposal language
- Project name
- Project type
- Main goals and deliverables
- Technology focus
- General description
- Planning details
- Key client stakeholders
- DareData team members
- Client expectations
- Special financial conditions

## Output

The application generates both:
- A formatted Markdown proposal

Both outputs can be copied to the clipboard for easy sharing.
