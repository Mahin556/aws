#!/bin/bash

set -e

# DynamoDB table name
TABLE_NAME="UsersTable"
NO_OF_ITEMS=1000

CITY_LIST=("Jaipur" "Delhi" "Mumbai" "Bangalore" "Pune")

for ((i=1; i<=NO_OF_ITEMS; i++)); do
    ID=$(uuidgen)
    AGE=$((RANDOM % 60 + 18))
    CITY=${CITY_LIST[$RANDOM % ${#CITY_LIST[@]}]}
    TIMESTAMP=$(date +"%Y-%m-%dT%H:%M:%S")

    aws dynamodb put-item \
      --table-name "$TABLE_NAME" \
      --item "{
        \"id\": {\"S\": \"$ID\"},
        \"age\": {\"N\": \"$AGE\"},
        \"city\": {\"S\": \"$CITY\"},
        \"created_at\": {\"S\": \"$TIMESTAMP\"}
      }"

    echo "Inserted item $i : ID=$ID | AGE=$AGE | CITY=$CITY | TIME=$TIMESTAMP" >> Item_list.log
done
