Данный репозиторий представляет собой комплекс инструментов для скачивания файлов и фильтрации данных в JSON формате.
Основные компоненты:
  1. Скачивание архива (downloader.py / wget_downloader.py)
  2. Парсинг JSON файлов (json_parser.py)
  3. Запись в БД (repository.py)

## Установка 
git clone git@github.com:WellspringV/egrul.git

cd egrul/

docker build -t egrul .

После сборки образа создаем общую сеть docker network create back_net
и запускаем 2 контейнера.
```shell
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
  egrul
```


## Использованные библиотеки
- Requests
- json
- Concurrent.futures
- Os
- Urllib
- re
- Logging
