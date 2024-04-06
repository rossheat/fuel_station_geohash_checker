# download_retailers_fuel_prices.py
import requests
import os
import csv
from datetime import datetime


def download_json_files_from_csv(csv_file):
    date_str = datetime.now().strftime("%d-%m-%Y")
    directory = os.path.join(os.getcwd(), "fuel_prices", date_str)

    if not os.path.exists(directory):
        os.makedirs(directory)

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    }

    with open(csv_file, mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            try:
                response = requests.get(
                    row["json_url"], headers=headers, timeout=10
                )  # 10 seconds timeout
                response.raise_for_status()

                json_file_path = os.path.join(directory, f"{row['name']}.json")
                with open(json_file_path, "w", encoding="utf-8") as json_file:
                    json_file.write(response.text)
                print(f"Downloaded JSON for {row['name']}")
            except requests.RequestException as e:
                print(f"Failed to download JSON for {row['name']}: {e}")


csv_file_name = "retailers.csv"
download_json_files_from_csv(csv_file_name)
