#!/bin/bash

CUR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$CUR_DIR"
# cp .env.example .env

source .env.local

while getopts ":u:" opt; do
  case $opt in
    u)
      sed -i "s/API_HOST=.*/API_HOST=$OPTARG/" .env
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

docker compose -p lb -f docker-compose-lb.yml up --build -d
docker compose --env-file .env.local -p bilingual-doc-extractor -f docker-compose.yml -f docker-compose.local.yml up --build -d