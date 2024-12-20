#!/bin/bash

CUR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$CUR_DIR"
# cp ~/.env .env

source .env

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

docker compose -p lb -f docker-compose.traefik.yml up --build -d
docker compose -p bilingual-doc-extractor  -f docker-compose.server.yaml up --build -d