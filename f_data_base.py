import os
import json
import psycopg2
import logging

from abc import ABC, abstractmethod


logging.basicConfig(filename='mylog.log', level=logging.DEBUG)
logging.getLogger('urllib3').setLevel(logging.WARNING)

logging.basicConfig(
    format='%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)



class BaseRepository(ABC):

    @abstractmethod
    def connect_to_db(self, credentials: dict) -> bool:
        pass

    @abstractmethod
    def execute_querry(self, query: str) -> None:
        pass

    @abstractmethod
    def insert_row(self, query: str) -> None:
        pass

    @abstractmethod
    def select(self, query: str) -> list:
        pass




class PostgresRepository(BaseRepository):
    def __init__(self):
        self.credentials = self.get_db_credentials()
        self.conn = self.connect_to_db(self.credentials)


    @staticmethod
    def get_db_credentials() -> dict:
        db_user = os.getenv('DB_USER')
        db_pass = os.getenv('DB_PASS')
        db_host = os.getenv('DB_HOST', 'database')  
        db_name = os.getenv('DB_NAME', 'postgres') 

        if not db_user or not db_pass:
            logging.error("Необходимы переменные окружения DB_USER и DB_PASS.")
            exit(1)    
        return {'user': db_user, 'password': db_pass, 'host': db_host, 'dbname': db_name}
    

    def connect_to_db(self, credentials: dict):
        conn = None
        try:
            conn = psycopg2.connect(**credentials)        
            return conn
        except Exception as e:
            logging.error(f"Не удалось подключиться к базе данных: {e}")
            return None
                

    def execute_querry(self, schema: str) -> None:
            try:
                with self.conn.cursor() as cur:
                    cur.execute(schema)
                self.conn.commit()
            except Exception as e:
                logging.error(f"Ошибка выполнения запроса: {e}")
            finally:
                if self.conn:
                    self.conn.close()
   
   
    def insert_row(self, query: str) -> None:    
        try:    
            if self.conn.closed:  
                self.conn = self.connect_to_db(self.credentials) 
            with self.conn.cursor() as cur:               
                cur.execute(query) 
            self.conn.commit()    
        except Exception as e:
            logging.error(f"Ошибка при вставке данных: {e}")
            if self.conn:
                self.conn.rollback()
        finally:
            if self.conn:
                self.conn.close()


    def select(self, query: str) -> list:
        try:
            if self.conn.closed:  
                self.conn = self.connect_to_db(self.credentials) 
            with self.conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return rows
        except Exception as e:
            logging.error(f"Ошибка при выполнении SELECT запроса: {e}")
            return []
        finally:
            if self.conn:
                self.conn.close()
        





def write_to_default_db(data):
    repo = PostgresRepository()
    
    schema = """
        CREATE TABLE IF NOT EXISTS companies (    
            id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            data JSONB
        );
        """
    if repo.connect_to_db(repo.credentials):
        repo.execute_querry(schema)
    else:
        logging.error("Подключение к базе данных не удалось.")

    json_string = json.dumps(data)
    query = f"""
        INSERT INTO companies (data)
        VALUES ('{json_string}');
        """ 
    repo.insert_row(query)



if __name__ == "__main__":
    pass