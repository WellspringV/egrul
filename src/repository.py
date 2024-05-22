import logging.config
from contextlib import contextmanager
from os import getenv
from playhouse.postgres_ext import *
from peewee import *
from log_settings import logger_config


logging.config.dictConfig(logger_config)
logger = logging.getLogger("app_logger")


credentials = {
    "user": getenv("DB_USER"),
    "password": getenv("DB_PASS"),
    "host": getenv("DB_HOST", "database"),
    "database": getenv("DB_NAME", "postgres"),
}


db = PostgresqlDatabase(**credentials)


@contextmanager
def DatabaseContextManager(database: PostgresqlDatabase):
    try:
        yield database
    finally:
        database.close()


class UL(Model):
    ogrn = CharField(unique=True)
    inn = TextField()
    kpp = CharField()
    name = TextField()
    full_name = TextField()
    data = BinaryJSONField()
    data_version = TextField()

    class Meta:
        database = db


class EGRRepository:
    def __init__(self, session) -> None:
        self.session = session

    def create_tables(self, list_of_tables):
        with self.session as s:
            try:
                s.create_tables(list_of_tables)
            except Exception as e:
                logger.error(e)

    def add(self, rows):
        with self.session.atomic():
            for row in rows:
                try:
                    UL.create(**row)
                except Exception as e:
                    logger.error(e)




def load(data: list):
    with DatabaseContextManager(db) as db_context:
        repository = EGRRepository(db_context)
        repository.create_tables([UL])
        repository.add(data)


if __name__ == "__main__":
    pass
