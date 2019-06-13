import gzip
import os
import re
from datetime import datetime, timedelta

import wget

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_URL = "http://files.tmdb.org/p/exports/"
FILE_NAME = "{0}_ids_{1}_{2}_{3}.json.gz"
EXPORT_TYPES = {
    "movie",
    "tv_series",
    'person',
    "collection",
    "tv_network",
    "keyword",
    "production_company"
}


def check_file_exist(file_name):
    return os.path.isfile(file_name)


def download_daily_files():
    time = datetime.now() - timedelta(1)
    for e_type in EXPORT_TYPES:
        file_name = FILE_NAME.format(e_type, time.strftime('%m'), time.strftime('%d'), time.strftime('%Y'))

        if not check_file_exist(file_name):
            url = DOWNLOAD_URL + file_name
            download_file(url, file_name)
        else:
            print(file_name, " is exist")


def download_file(url, local_filename):
    print(url)
    print("downloading", local_filename)
    wget.download(url)
    print("done")
    extract_json(local_filename)


def check_files_expired():
    print('check file in', os.path.join(BASE_DIR, "dataset"))
    directory = os.path.join(BASE_DIR, "dataset")
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for name in filenames:
            print("name", name)
            try:
                file_date = str(re.search("([0-9]{2}\_[0-9]{2}\_[0-9]{4})", name).group())
                file_date = datetime.strptime(file_date, "%m_%d_%Y")
                date_now = datetime.now()

                time_dif = date_now - file_date
                if time_dif.days > 3:
                    print("{} file is too old delete.".format(name))
                    os.remove(name)

                print("time different = ", time_dif.days)

            except:
                print("not exist")


def extract_json(local_filename):
    with gzip.GzipFile(local_filename, 'r') as fin:
        filename = local_filename.split("_ids_")[0] + ".json"
        open(filename, 'wb').write(fin.read())


download_daily_files()
check_files_expired()
