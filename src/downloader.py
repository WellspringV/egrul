import os
import urllib
import logging.config
from pathlib import Path
from urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor

import requests
from requests.adapters import HTTPAdapter

from log_settings import logger_config


logging.config.dictConfig(logger_config)
logger = logging.getLogger("app_logger")


class DownloadManager:
    def __init__(self, url: str) -> None:
        self.url = url
        self.filename = ""
        self.response_headers = {}
        self.origin_file_size = 0  
        self.session = None     
        self.partially_downloaded = False
        self.ready_to_download = False
        self._prepare_download()   
                
    def _get_response_headers(self) -> dict:      
        request = urllib.request.Request(self.url, method="HEAD")
        response = urllib.request.urlopen(request)
        return response.headers
        
    def _get_origin_size(self) -> int:
        size = int(self.response_headers.get('Content-Length', 0))
        return size
    
    def _get_origin_name(self) -> str:
        name = self.response_headers.get('filename', "")
        if not name:
            name = Path(urllib.parse.urlparse(self.url).path).name
        return name
    
    @property
    def local_file_exists(self) -> bool:
        if os.path.exists(self.filename):
            return True
    
    def _prepare_session(self) -> None:
        self.session = requests.Session()
        retry_strategy = Retry(    
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET"],
            backoff_factor=0.5,
            raise_on_status=False,
            raise_on_redirect=False,
        )         
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)


    def _prepare_download(self) -> None:
        try:
            response_headers = self._get_response_headers()
        except Exception as ex:
            logging.error(ex)
        else:
            self.response_headers = response_headers
            self.origin_file_size = self._get_origin_size()
            self.filename = self._get_origin_name()
            self._prepare_session()
            self.ready_to_download = True

    def download(self, url: str, start: int, end: int, output: str, timeout: int = 10) -> None:        
        headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 "
            "YaBrowser/22.11.3.838 Yowser/2.5 Safari/537.36",
            'Range': f'bytes={start}-{end}' 
        }
        
        try:
            rs = self.session.get(url=url, headers=headers, stream=True, timeout=timeout)
            if 200 <= rs.status_code <= 299:                
                with open(f'tmp/{output}', 'wb') as file:
                    for part in rs.iter_content(1024):
                        file.write(part)
            else:
                return
        except requests.exceptions.IncompleteRead as e:
            logging.error(f"Ошибка чтения: {e}. Попытка повторения...")
        except Exception as ex:
            logging.error(ex)
            return
        

    def thread_run(self, thread_count: int) -> tuple:
        file_size = self.origin_file_size
        name = self.filename
        chunk_size = int(file_size / thread_count)
        chunks = range(0, file_size, chunk_size)        

        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            future_list = []
            for i, chunk in enumerate(chunks):
                future = executor.submit(self.download, url=self.url, start=chunk, end=chunk + chunk_size - 1, output=f'{self.filename}.{i}')
                future_list.append(future)

            for f in future_list:
                print(f.result())
        return len(chunks), name  



def download_data(url):
    download_manager = DownloadManager(url)
    chunks, name = download_manager.thread_run(10)

    with open(name, "wb") as file:
        for i in range(chunks):
            with open(f'tmp/{Path(url).name}.{i}', 'rb') as ch:
                file.write(ch.read())
            Path(f'tmp/{Path(url).name}.{i}').unlink()


if __name__ == "__main__":
    download_data('https://ofdata.ru/open-data/download/egrul.json.zip')