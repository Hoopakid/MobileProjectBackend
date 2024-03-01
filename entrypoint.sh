if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    wait-for-it $SQL_HOST:$SQL_PORT -t 30
    echo "PostgresSQL started"
fi

exec "$@"