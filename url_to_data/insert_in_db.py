from api import all_csvs_to_file

bka_zeitreihen_daten_url = "https://www.bka.de/DE/AktuelleInformationen/StatistikenLagebilder/PolizeilicheKriminalstatistik/PKS2019/PKSTabellen/Zeitreihen/zeitreihen_node.html"

bka_bund_fall_tabellen_url = "https://www.bka.de/DE/AktuelleInformationen/StatistikenLagebilder/PolizeilicheKriminalstatistik/PKS2019/PKSTabellen/BundFalltabellen/bundfalltabellen.html?nn=130872"


corona_url = "https://ourworldindata.org/coronavirus-source-data"





all_csvs_to_file(bka_zeitreihen_daten_url, "bka_zeitreihe")
