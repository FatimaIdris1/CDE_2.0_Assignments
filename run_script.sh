#!/bin/bash

# Load environment variables from config.env
set -a
source ./config.env
set +a

###########

# Create a network
docker network create etl_network

# Run Postgres container
docker run -d --name postgres_container \
  --env-file ./config.env \
  --network etl_network \
  -p 5433:5432 \
  postgres:15

# Wait until Postgres is ready
until docker exec postgres_container pg_isready -U $POSTGRES_USER; do
  echo "Waiting for Postgres..."
  sleep 1
done

# Build ETL Image
docker build -t etl_pipeline .

# Run ETL container
docker run --rm --name etl_container \
  --env-file ./config.env \
  --network etl_network \
  etl_pipeline

