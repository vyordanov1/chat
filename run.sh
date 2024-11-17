#!/bin/bash

export $(grep -v '^#' .env | xargs)

docker compose up -d
sleep 15
docker exec -it ${PSQL_CONTAINER_NAME} bash scripts/init.sh
docker compose restart