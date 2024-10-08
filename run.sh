#!/bin/bash

export $(grep -v '^#' .env | xargs)

docker compose up -d
sleep 2
docker exec -it ${PSQL_CONTAINER_NAME} bash scripts/init.sh
docker compose restart