docker network create back_net
docker volume create postgres_volume


docker run --rm -d \
  --name database \
  --net=back_net \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=123 \
  -e POSTGRES_DB=postgres \
  -v postgres_volume:/var/lib/postgresql/data \
  postgres:14


docker run --rm \
  -it \
  --name back \
  --net=back_net \
  -p 8000:8000 \
  -e DB_HOST=database \
  -e DB_USER=postgres \
  -e DB_PASS=123 \
  -e DB_NAME=postgres \
  egrul:2
