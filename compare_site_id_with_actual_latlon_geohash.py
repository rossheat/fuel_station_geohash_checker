# compare_site_id_with_actual_latlon_geohash.py
import os
import json
import geohash2
import argparse
from datetime import datetime
from collections import defaultdict


def compare_geohashes(input_directory, date):
    input_directory = os.path.join(input_directory, date)
    print(f"Processing JSON files in directory: {input_directory}")

    json_files = [f for f in os.listdir(input_directory) if f.endswith(".json")]
    print(f"Processing {len(json_files)} files: {json_files}")

    errors_directory = os.path.join("./errors", date)
    if not os.path.exists(errors_directory):
        os.makedirs(errors_directory)
        print(f"Created errors directory: {errors_directory}")

    for filename in json_files:
        print(f"Processing file: {filename}")
        file_path = os.path.join(input_directory, filename)
        with open(file_path, "r") as file:
            data = json.load(file)

        errors = []
        duplicates = defaultdict(int)
        total_stations = len(data["stations"])

        for station in data["stations"]:
            site_id = station["site_id"]
            lat = float(station["location"]["latitude"])
            lon = float(station["location"]["longitude"])
            calculated_geohash = geohash2.encode(lat, lon, precision=12)

            if site_id != calculated_geohash:
                errors.append(
                    {
                        "site_id": site_id,
                        "actual_geohash": calculated_geohash,
                        "lat": lat,
                        "lon": lon,
                    }
                )

            duplicates[site_id] += 1

        duplicate_count = sum(1 for count in duplicates.values() if count > 1)
        if duplicate_count > 0:
            print(f"{filename}: Found {duplicate_count} duplicates")
            duplicates_filename = os.path.splitext(filename)[0] + "_duplicates.csv"
            duplicates_file_path = os.path.join(errors_directory, duplicates_filename)
            with open(duplicates_file_path, "w") as duplicates_file:
                duplicates_file.write("site_id, count\n")
                for site_id, count in duplicates.items():
                    if count > 1:
                        duplicates_file.write(f"{site_id}, {count}\n")

        if errors:
            discrepancy_percentage = (len(errors) / total_stations) * 100
            print(
                f"{filename}: {len(errors)} out of {total_stations} stations ({discrepancy_percentage:.2f}%) have mismatched geohashes"
            )
            error_filename = os.path.splitext(filename)[0] + "_geohash_mismatches.csv"
            error_file_path = os.path.join(errors_directory, error_filename)
            with open(error_file_path, "w") as error_file:
                error_file.write(
                    "site_id (provided geohash), actual geohash, lat, lon\n"
                )
                for error in errors:
                    error_file.write(
                        f"{error['site_id']}, {error['actual_geohash']}, {error['lat']}, {error['lon']}\n"
                    )
            print(f"Error file written: {error_file_path}")
        else:
            print(f"No geohash mismatches found in {filename}")


def main():
    parser = argparse.ArgumentParser(description="Compare geohashes in JSON files.")
    parser.add_argument(
        "--fuel_prices_directory",
        default="./fuel_prices",
        help="Directory containing JSON files.",
    )
    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%d-%m-%Y"),
        help="Date for error file directory (format: dd-mm-yyyy).",
    )
    args = parser.parse_args()

    compare_geohashes(args.fuel_prices_directory, args.date)


if __name__ == "__main__":
    main()
