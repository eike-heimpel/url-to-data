import os
from pathlib import Path
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urlsplit
import requests
import pandas as pd
import io
from pandas import errors as pandas_errors
import logging


class Website:

    def __init__(self):

        self.base_url = ""
        self.links_to_csvs = {}


    def find_csvs(self, data_download_url):

        base_url = self.__find_base_url(data_download_url)

        html_page = urllib.request.urlopen(data_download_url)
        soup = BeautifulSoup(html_page, 'html.parser')

        for a in soup.find_all('a', href=True):
            if a.text:
                if ".csv" in a['href']:

                    try:
                        file_name = Path(a["href"].stem)
                    except AttributeError:
                        file_name = a["href"].split("/")[-1]
                        file_name = file_name.strip(".csv")
                    if "http://" in a['href'] or "https://" in a['href']:
                        self.links_to_csvs[f'{file_name}.csv'] = a['href']
                    else:
                        self.links_to_csvs[f'{file_name}.csv'] = f"{base_url}/{a['href']}"


    def __find_base_url(self, full_url):

        split_url = urlsplit(full_url)
        base_url = f"{split_url.scheme}://{split_url.netloc}"

        return base_url


class csvTable:

    def __init__(self, folder_path, table_url, table_file_name, second_row_headers=False):

        self.folder_path = folder_path
        self.table_url = table_url.replace(" ", "%20")
        self.table_file_name = table_file_name
        self.table_full_file_path = "wrong path"
        self.table = None
        self.table_name = "wrong table name"
        self.second_row_headers = second_row_headers


    def table_from_csv_url(self):

        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

        self.table_full_file_path = f"{self.folder_path}/{self.table_file_name}"

        if os.path.exists(self.table_full_file_path):
            os.remove(self.table_full_file_path)


        try:
            csv_link_content = requests.get(self.table_url).content
            _ = io.StringIO(csv_link_content.decode('utf-8'))
            encoding = "utf-8"

        except UnicodeDecodeError:
            encoding = "latin1"
            logging.debug("could not encode with utf-8, forcing latin1 encoding")

        try:
            self.table = pd.read_csv(self.table_url, encoding=encoding)

        except pandas_errors.ParserError:

            try:
                self.table = pd.read_csv(self.table_url, sep=";", encoding=encoding)
                logging.debug("using ';' as separator")

            except pandas_errors.ParserError:
                logging.exception("could not decode the csv, most likely because it "
                                  "could not detect the correct delimiter")


    def clean_table(self):

        self.table = self.table.dropna(how="all")

        if self.second_row_headers:
            self.__update_header_with_first_row()


    def save_clean_csv(self):

        try:
            self.table.to_csv(self.table_full_file_path.strip)
        except ValueError:
            self.table_full_file_path = f"{self.folder_path}/{Path(self.table_url).stem}.csv"
            self.table.to_csv(self.table_full_file_path)
        except OSError:
            self.table_full_file_path = f"{self.folder_path}/{Path(self.table_url).stem}.csv"
            self.table.to_csv(self.table_full_file_path)

    def __update_header_with_first_row(self):

        new_header = self.table.iloc[0]
        self.table = self.table[1:]
        self.table.columns = new_header



