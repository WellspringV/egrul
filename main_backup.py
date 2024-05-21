
import os
import zipfile
import logging

from progress.bar import IncrementalBar

from parse_json import *
from downloader import DownloadManager, main_download
from wget_download import run_cmd
from f_data_base import write_to_default_db



logging.basicConfig(filename='mylog.log', level=logging.DEBUG)
logging.basicConfig(
    format='%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)



def smart_unzip(json_archive, first_filter_param, second_filter_param):       
    with zipfile.ZipFile(json_archive, 'r') as zip_ref:
        filenames = zip_ref.namelist()
        bar = IncrementalBar('Handling', max = len(filenames)) 

        for filename in filenames:
            try:
                bar.next()
                zip_ref.extract(filename)
                res = complex_filter(filename, first_filter_param, second_filter_param)                
            except Exception as e:
                logging.warning('Error {e} on filename {filename}')
            else:
                if res:
                    write_to_default_db(res)
            finally:                                    
                os.remove(filename)
        bar.finish()
        

def main():
    URL ='https://ofdata.ru/open-data/download/egrul.json.zip'
    TARGET_FILE = 'egrul.json.zip'
    TARGET_SIZE = DownloadManager(URL)._get_origin_size()
    FIRST_FILTER_PARAM = ('КодОКВЭД', ['62.'])
    HOME_REGIONS = ('КодРегион', ['10', '11', '29', '35', '39', '47', '51', '53', '60', '78', '83'])
    JSON_ZIP_FILE = 'egrul.json.zip'


    if os.path.exists(TARGET_FILE):        
        os.path.getsize(TARGET_FILE) == TARGET_SIZE
        reload = input('Файл с архивом уже существует, требуется перезаписать?\n')
        while reload not in ('Yes', 'No'):
            reload = input('Ввдедите Yes или No\n')
        if reload == 'Yes':   
            print("Начинаю скачивание файла")
            main_download(URL) 
        elif reload == 'No':
            print('Загрузка была принудительно завершена')
    else:
        print("Начинаю скачивание файла")   
        main_download(URL)  
        
    
    if os.path.exists(TARGET_FILE) and (os.path.getsize(TARGET_FILE) == TARGET_SIZE): 
        print('Начата обработка архива')        
        smart_unzip(JSON_ZIP_FILE, FIRST_FILTER_PARAM, HOME_REGIONS)
    else:
        print('Retry download')
        run_cmd('echo "Wait download!"', verbose=True)
        run_cmd("wget -cO - https://ofdata.ru/open-data/download/egrul.json.zip > egrul.json.zip", verbose=True)    




if __name__ == "__main__":
    main()