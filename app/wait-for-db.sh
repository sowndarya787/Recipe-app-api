#!/bin/sh
# wait-for-db.sh

set -e

host="$1"
shift
cmd="$@"

until pg_isready -h "$host" -p 5432; do
  echo "Waiting for PostgreSQL at $host..."
  sleep 2
done

exec $cmd
