#!/bin/sh

set -e

host="$1"
port="$2"
user="$3"
pass="$4"
shift 4
cmd="$@"

until PGPASSWORD="$pass" psql -h "$host" -p "$port" -U "$user" -d "postgres" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd