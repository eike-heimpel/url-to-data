import pytest
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
from url_to_data import all_csvs_to_file

@pytest.fixture
def list_of_test_urls_with_csvs():

    url_list =  ["https://statweb.stanford.edu/~sabatti/data.html",
            "https://www.bka.de/DE/AktuelleInformationen/StatistikenLagebilder/PolizeilicheKriminalstatistik/PKS2019/PKSTabellen/BundFalltabellen/bundfalltabellen.html?nn=130872",
            "https://ourworldindata.org/coronavirus-source-data"]

    return url_list


def test_saving_all_csvs(list_of_test_urls_with_csvs):

    for url in list_of_test_urls_with_csvs:
        all_csvs_to_file(url, "C:/Users/eikeh/Desktop/Python_Projects/KriminalStats/data/test17")
