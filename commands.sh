docker network create back_net
docker run --rm -d \
  --name database \
  --net=back_net \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=123 \
  -e POSTGRES_DB=postgres \
  postgres:14

# docker exec -it database psql --username  postgres --dbname postgres
docker run --rm -d \
  --name back \
  --net=back_net \
  -p 8000:8000 \
  -e DB_HOST=database \
  -e DB_USER=postgres
  -e DB_PASS=123 \
  -e DB_NAME=postgres
  custom_cli:1

