docker rm -f postgres_test_mvcs

set -e

docker run -p 5555:5432 -e POSTGRES_PASSWORD=mvcs --name postgres_test_mvcs -d postgres:11
sleep 20
cat tests/resources/test_metabase_database.sql | docker run -i -e PGPASSWORD=mvcs --network host --rm postgres:11 psql -h localhost --user postgres --port 5555