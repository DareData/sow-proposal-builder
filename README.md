# DareData Proposal Builder

A beautiful Streamlit application for creating project proposals with a consistent format.

## Features

- User-friendly form interface with helpful tooltips explaining each field
- Automatic generation of formatted Markdown proposals
- Support for English and Portuguese (PT-PT) proposals
- Optional best practices sections (MLOps, DevOps, LLMOps, Way of Working)
- Adjustable output length for project descriptions (standard or extended)
- Containerized for easy deployment


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
- Proposal language  (English / Portuguese)
- Project name
- Project type
- Technology focus
- General description
- Planning details
- Key client stakeholders
- DareData team members
- Client expectations
- Special financial conditions
- Best practices sections (optional): MLOps, DevOps, LLMOps, Way of Working
- Output length preference (for larger projects)

## Output

The application generates:
- A formatted Markdown proposal


## Example

- Client name: 
ACME
- Proposal language: 
English
- Project name: 
Automatic Email Replier
- Project type:
Gen-OS
- Technology focus:
Azure
- General description:
ACME aims to develop an automatic email replier for their contact center in order to reduce the amount of time that their workers spend on communication with the client, since they have a team of over 12 people replying to emails and making quotations of purchase orders.
DareData's solution is based on an orchestrator that decides how to answer the client with access to two main agents: a Knowledge Specialist with access to general information about customer support and an API Specialists that knows how to query ACME's Products DB to extract information such as pricing, alternative products and product availability. 
These Agents will be deployed as microservices using Azure Kubernetes Service (AKS) and registered using Azure's Container Registry. The vector DB will be postgres with pgvector extension hosted on Azure Cosmos DB. We will also use Azure Monitor, Key Vault, API management and Microsoft Entra ID for Gen-OS users.
Gen-OS will allow operators to solve edge cases that cannot be resolved by AI, allowing also for monitoring of the metrics, as well as continuous improvement via Issue Management. Any modification of the system will launch an Azure Pipeline that will test the new system against an Eval Set and the new container registry will appear in Gen-OS. 
- Planning details:
We will have a 4-week "SETUP: Build" phase, followed by a 2-week "SETUP: Tuning" one.
As milestones, we are considering having a simple PoC around week 2, Gen-OS set up around week 3 and launch to production around week 4 to a 10% of incoming emails. After the tuning phase we will roll out to 100%. 
- Key client stakeholders:
RoadRunner - Head of Managed Solutions
Coyote - Head of AI
- DareData team members:
DEFAULT
- Client expectations:
DEFAULT
- Special financial conditions:
DEFAULT
