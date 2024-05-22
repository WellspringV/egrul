Данный репозиторий представляет собой комплекс инструментов для скачивания файлов и фильтрации данных в JSON формате.
Основные компоненты:
  1. downloader.py / wget_downloader.py (скачивание архива) 
  2. json_parser.py (парсинг JSON файлов)
  3. repository.py (работа с БД)

Требуется доработать:
1. Выбор параметров фильтрации.
2. Уплощение и разбиение схемы JSON для записи в несколько таблиц.


## Пример установки и запуска 

Копируем репозиторий
```shell
git clone git@github.com:WellspringV/egrul.git && cd egrul/ \
&& docker build -t egrul .
```


После сборки образа создаем кастомную сеть и volume
```shell
docker network create back_net && \
docker volume create postgres_volume
```

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
```

```shell
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

Процесс загрузки 

![image](https://github.com/WellspringV/egrul/assets/58819893/2b5cf9d9-abc7-452d-bfca-71afb53290b0)

После скачивания архива производится поэтапное разархивирование, чтение и фильтрация данных.
Целевые данные записываются в БД.

Проверка результата:
```shell
docker exec -it database psql --username postgres --dbname postgres
 \dt
\d+ ul
```
![image](https://github.com/WellspringV/egrul/assets/58819893/f12c469d-8bee-47ff-a989-599e197752da)
![image](https://github.com/WellspringV/egrul/assets/58819893/e6b26b08-2509-4faa-8536-5b7c2bc1dfaa)

```shell
select id, ogrn, inn, kpp from ul order by id limit 5;
```
![image](https://github.com/WellspringV/egrul/assets/58819893/c531107b-947e-4e0e-9c02-1f00f7e341a4)


