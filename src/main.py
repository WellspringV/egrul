import sys
import os
import zipfile
import shutil


from repository import load
from downloader import download_data, DownloadManager
from wget_downloader import wget_data
from json_parser import *


if sys.platform.startswith("win"):
    zip_loader = download_data
else:
    zip_loader = wget_data


def smart_unzip(json_archive):
    with zipfile.ZipFile(json_archive, "r") as zip_ref:
        filenames = zip_ref.namelist()
        for file in filenames:
            yield zip_ref.extract(file)


def read_and_drop(json_gen, filters):
    first_filter_param, second_filter_param = filters
    try:
        json_file = next(json_gen)

        res = complex_filter(json_file, first_filter_param, second_filter_param)
        if res:
            load(res)
    except Exception as e:
        print(e)
    finally:
        if os.path.exists(json_file):
            os.remove(json_file)


def interactive(question: str) -> bool:
    ask = input(f"{question}\n").strip()
    
    while ask not in ("Yes", "No"):
        ask = input("Введите Yes или No\n")
    
    if ask == "Yes":
        return True
    elif ask == "No":
        return False
    


def download_solition(solution: bool, url: str) -> None:
    if not solution:
        print("Работа программы принудительо завершена")
    else:
        print("Начинаю скачивание файла")
        zip_loader(url)





def main():

    URL = "https://ofdata.ru/open-data/download/egrul.json.zip"
    TARGET_FILE = "egrul.json.zip"
    FIRST_FILTER_PARAM = ("КодОКВЭД", ["62."])
    HOME_REGIONS = (
        "КодРегион",
        ["10", "11", "29", "35", "39", "47", "51", "53", "60", "78", "83"],
    )
    TARGET_SIZE = DownloadManager(URL)._get_origin_size()
    total, user, free = shutil.disk_usage('/')

    if free < TARGET_SIZE:
        print(f'На диске недостаточно места, небоходимо {TARGET_SIZE / (1024 ** 3)}GB, доступно {free / (1024 ** 3)}GB')
        return

    try:
        if os.path.exists(TARGET_FILE):

            current_size = os.path.getsize(TARGET_FILE)

            if current_size != TARGET_SIZE:
                solution = interactive(
                    "Размер файла не соответствует ожидаемому, требуется перезаписать? (Yes/No)"
                )
                
                download_solition(solution, URL)
            else:
                solution = interactive(
                    "Локальная копия файла уже существует, требуется повторное скачивание? (Yes/No)"
                )
                download_solition(solution, URL)

        else:
            solution = interactive(
                "Локальная копия файла отуствует, начать загрузку? (Yes/No)"
            )
            download_solition(solution, URL)

    except Exception as e:
        print(f"Во время работы скачивания файла возникло исключение {e}")
    else:
        if os.path.exists(TARGET_FILE) and os.path.getsize(TARGET_FILE) == TARGET_SIZE:
            print("Начата обработка архива")
            g = smart_unzip(TARGET_FILE)
            read_and_drop(g, (FIRST_FILTER_PARAM, HOME_REGIONS))
        else:
            print("Попробуйте повторить загрузку файла")



if __name__ == "__main__":
    main()
