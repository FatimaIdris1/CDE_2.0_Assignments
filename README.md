## Overview

This repository contains Bash and SQL scripts for CoreDataEngineers’ data infrastructure. The scripts are Linux-based and automate data extraction, transformation, loading, file management, and competitor data analysis.

The project includes:

1. An ETL pipeline in Bash.
2. Cron job scheduling for daily automation.
3. A file-moving script for CSV and JSON files.
4. A PostgreSQL ingestion pipeline for competitor data (Parch & Posey) and SQL queries for analysis.
5. A conceptual ETL diagram for management presentation.

---

## Repository Structure

```
.
├── Bash_Scripts/
│   ├── CDE_ETL_Bash.sh        # Task 1: ETL pipeline
│   ├── json_csv.sh            # Task 3: Move CSV and JSON files
│   └── csv_bash_to_postgres.sh   # Task 4: Load Parch & Posey CSVs into PostgreSQL
│
├── SQL_Scripts/
│   └── Posey_Query_Script.sql # SQL queries for competitor analysis
│
├── Manager_ETL_Diagram.png        # Conceptual ETL diagram for Task 1
│
└── README.md
```

> Note: `raw/`, `Transformed/`, and `Gold/` directories are **not in the repo**. They are generated automatically when running the ETL script.

---

## Task 1: ETL Pipeline

**Script:** `Bash_Scripts/CDE_ETL_Bash.sh`

* **Extract**: Downloads CSV data into a `raw/` folder.
* **Transform**: Renames `Variable_code → variable_code`, selects required columns, and saves the output into `Transformed/`.
* **Load**: Copies the transformed file into `Gold/`.
* Prints confirmations for each step.

Run manually with:

```bash
./Bash_Scripts/CDE_ETL_Bash.sh
```

---

## Task 2: Cron Job Scheduling

The ETL pipeline is scheduled to run daily at **12:00 AM**.

Example crontab entry:

```
0 0 * * * /path/to/Bash_Scripts/CDE_ETL_Bash.sh >> /path/to/CDE_Pipline_Log_Files.log 2>&1
```

* Runs the ETL script every midnight.
* Logs are stored in `CDE_Pipline_Log_Files.log`.

---

## Task 3: Moving CSV and JSON Files

**Script:** `Bash_Scripts/json_csv.sh`

* Moves all `.csv` and `.json` files from the current directory into a `json_and_CSV/` folder.
* Works with one or multiple files.

Run with:

```bash
./Bash_Scripts/json_csv.sh
```

---

## Task 4: Parch & Posey Competitor Data

### Loading into PostgreSQL

**Script:** `Bash_Scripts/csv_bash_to_postgres.sh`

* Creates the `posey` database if not already present.
* Sets up required tables (`accounts`, `orders`, `region`, `sales_reps`, `web_events`).
* Iterates through CSVs in `data-raw/` and loads them into PostgreSQL using `\COPY`.

Run with:

```bash
./Bash_Scripts/csv_bash_to_postgres.sh
```

### SQL Analysis Queries

**File:** `SQL_Scripts/Posey_Query_Script.sql`

Queries included:

1. Order IDs where `gloss_qty` or `poster_qty` > 4000.
2. Orders where `standard_qty = 0` and `gloss_qty` or `poster_qty` > 1000.
3. Company names starting with `C` or `W`, with contacts containing `ana`/`Ana` but not `eana`.
4. A report showing region, sales rep, and accounts (sorted by account name).

---

## Manager ETL Diagram

**File:** `Manager_ETL_Diagram/ETL_Diagram.png`

This diagram illustrates the conceptual Extract → Transform → Load (ETL) process used in Task 1.

---

## Requirements

* Linux
* Bash
* PostgreSQL installed and running
* Tools: `curl`, `sed`, `cut`, `psql`, `cron`
