# ETL Pipeline with Docker & PostgreSQL

This project demonstrates a simple yet powerful **ETL (Extract, Transform, Load) pipeline** built with **Python, Docker, and PostgreSQL**.

It automates the process of:
- Extracting a dataset from a provided URL.
- Transforming the dataset (cleaning, normalizing, preparing it).
- Loading the final data into a **Postgres database** running in a container.

The pipeline is containerized and orchestrated using Docker, with a single bash script to streamline the setup.

---

## Project Overview

- A **Postgres container** is created from the official Postgres image.
- An **ETL pipeline container** is built from the provided `Dockerfile`.
- Both containers communicate over a custom Docker network (`etl_network`).
- The pipeline is triggered via a simple bash script (`run_script.sh`) that automates the entire process.

When executed:
1. The Postgres container is started.
2. The ETL container runs the `etl_pipeline.py` script.
3. Data from the `DATA_URL` (defined in `config.env`) is extracted, transformed, and loaded into the Postgres database.

---

## Repository Structure
```bash
├── Dockerfile              # Builds the ETL pipeline image
├── run_script.sh           # Automates the entire setup & execution
├── etl_pipeline.py         # Python script performing the ETL
├── requirements.txt        # Python dependencies
├── config.env              # Environment file
└── README.md               # Project documentation
```
# Data Pipeline with Docker and PostgreSQL

This project sets up a data pipeline using Docker, PostgreSQL, and a Bash script to automate Extract, Transform, and Load (ETL) processes.

---

## Prerequisites

Ensure you have the following installed on your system:

- [Docker](https://docs.docker.com/get-docker/)
- [Git](https://git-scm.com/downloads)
- Git Bash (for Windows users)
- Terminal (for Linux/Mac users)
- Basic knowledge of Bash, Docker, and PostgreSQL

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/<username>/<repo>.git
cd <your-repo>
```
### 2. Configure Environment Variables

The config.env file in the root directory has the following values:
```bash
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database
#Replace the placeholders with your preferred PostgreSQL credentials.
```
#### 3. Running the Project
Execute the provided Bash script:
```bash
./run_script.sh
```

The script will:

- Extract data
- Transform it as required
- Load it into the PostgreSQL database

#### Accessing PostgreSQL Database

1. Connect to the Container
```bash
docker exec -it <postgres_container> psql -U <POSTGRES_USER> -d <POSTGRES_DB>

# -i keeps STDIN open
# -t allocates a pseudo-terminal
# Replace <postgres_container_name> with your container name (docker ps will show it)

```
3. Run Queries
Once inside PostgreSQL:
```bash
SELECT * FROM your_table
LIMIT 10;
```
3. Exit PostgreSQL
Type:
```bash
\q
```
