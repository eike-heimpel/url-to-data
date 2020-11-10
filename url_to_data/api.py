from .csv_table import csvTable, Website


def all_csvs_to_file(url, folder_path):

    website = Website()
    website.find_csvs(url)

    for table_file_name, table_url in website.links_to_csvs.items():
        csv_table = csvTable(folder_path, table_url, table_file_name, second_row_headers=True)
        csv_table.table_from_csv_url()

        csv_table.clean_table()
        csv_table.save_clean_csv()
