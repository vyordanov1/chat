#!/bin/bash

export $(grep -v '^#' .env | xargs)

docker compose up -d --build
sleep 10
docker exec -it ${PSQL_HOST} bash scripts/init.sh
docker compose restart
