Этот проект представляет собой комплекс инструментов для загрузки файлов и фильтрации данных в JSON формате.
Он включает в себя загрузчик для скачивания больших файлов с использованием многопоточности и набор функций для работы с JSON-данными, таких как поиск ключей, получение значений по иерархии ключей и сложная фильтрация данных.
Скачивание производится частями, что позволяет избежать переполнения оперативной памяти.
Полученные результаты сохраняются в БД.

Загрузка и обработка файла состоит из трех шагов:
  1. Скачивание архива (downloader.py)
  2. Парсинг JSON файлов (parse_json.py)
  3. Запись в БД (f_data_base.py)

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
