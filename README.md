# Fuel Station Geohash Checker

## Introduction

The UK's Competition and Markets Authority (CMA) has recommended that each fuel retailer in the UK provide a web link to a JSON file containing metadata about each fuel station and its daily prices. This initiative aims to promote transparency and help consumers make informed decisions when purchasing fuel. You can read more about it [here](https://www.gov.uk/guidance/access-fuel-price-data). As part of this scheme, the CMA has provided a [technical specification](https://assets.publishing.service.gov.uk/media/64d4ac7b5cac65000dc2dd1a/A._Appendix_A.pdf) for the JSON file format, which includes a unique identifier for each fuel station called `site_id`. This identifier is a 12-character geohash derived from the latitude and longitude coordinates of the station.

## Problem Statement

Given the CMA's specification, developers reasonably expect each unique station to have a unique 'site_id' value. However, when building an application that consumes the JSON files provided by the fuel retailers, it was discovered that some retailers had the same `site_id` for more than one station, which should not be possible if:

1.  Each station's latitude and longitude coordinates were different; analysis of the data showed that this was the case.
2.  A sufficient number of geohash characters were specified as to make each `site_id` unique; given that the `site_id` is a 12-character geohash, the probability of a collision is extremely low.
3.  The geohashes were calculated correctly.

This led to the hypothesis that some retailers were not calculating the `site_id` geohashes correctly. To investigate this issue, a program called `fuel_station_geohash_checker` was developed to compare the provided `site_id` geohashes with the actual geohashes calculated using the `geohash2` library based on the latitude and longitude coordinates of each station.

## Analysis Results

The `fuel_station_geohash_checker` program was run on the daily fuel price JSON files provided by 14 different retailers for the date 06-04-2024. The output revealed that some retailers had mismatches between the provided `site_id` geohashes and the correctly calculated geohashes:

| Retailer            | Total Stations | Mismatched Geohashes | Percentage Mismatch |
| ------------------- | -------------- | -------------------- | ------------------- |
| Tescos              | -              | 0                    | 0%                  |
| JET Retail UK       | -              | 0                    | 0%                  |
| Morrisons           | -              | 0                    | 0%                  |
| bp                  | -              | 0                    | 0%                  |
| Moto                | 47             | 47                   | 100%                |
| Applegreen UK       | -              | 0                    | 0%                  |
| Shell               | -              | 0                    | 0%                  |
| Asda                | 667            | 559                  | 83.81%              |
| Sainsbury's         | -              | 0                    | 0%                  |
| Rontec              | -              | 0                    | 0%                  |
| Motor Fuel Group    | -              | 0                    | 0%                  |
| Esso Tesco Alliance | -              | 0                    | 0%                  |
| SGN                 | -              | 0                    | 0%                  |
| Ascona Group        | 60             | 47                   | 78.33%              |

The results show that Moto, Asda, and Ascona Group had a significant number of mismatched geohashes.

Furthermore, analysis of the 06-04-2024 data also identified a duplicate `site_id` value in Asda's file:

```
site_id, count
gcr3m8rsmk3h, 2
```

Please refer to the error files in the `./errors/06-04-2024` directory for detailed information on the mismatched geohashes and duplicate `site_id` entries for each retailer. For example, here is the first three rows of `./errors/06-04-2024/Asda_geohash_mismatches.csv`:

| site_id      | actual geohash | lat       | lon       |
| ------------ | -------------- | --------- | --------- |
| gcqfn1wd5k4j | gcqfn1wdqk9d   | 52.391463 | -1.484944 |
| gcjw4hhp6ywh | gcjw4hpgvt0p   | 51.702332 | -3.416855 |
| gfj6057mn7se | gfj6057mj0v4   | 56.620278 | -3.862503 |

## Recommendations

Based on the findings, it is recommended that the CMA communicate to all participating fuel retailers the importance of ensuring that the `site_id` geohashes are calculated correctly according to the technical specification provided. Retailers should review their JSON file generation process and ensure that the geohashes are derived accurately from the unique latitude and longitude coordinates of each fuel station. If the geohashes are calculated correctly, there should be no duplicate `site_id` values.

## Replicating the Analysis

To replicate the analysis using the cached data for 06-04-2024 present in the file tree, follow these steps:

1. Ensure that you have Python installed on your system.

2. Clone the repository containing the `fuel_station_geohash_checker` program and the cached data.

3. Navigate to the project directory.

4. Install the required dependencies by running the following command:

   ```
   pip install -r requirements.txt
   ```

5. Run the `compare_site_id_with_actual_latlon_geohash.py` script using the following command:

   ```
   python compare_site_id_with_actual_latlon_geohash.py --fuel_prices_directory ./fuel_prices --date 06-04-2024
   ```

6. The script will process the JSON files in the specified directory for the date 06-04-2024 and generate separate error files for any retailers with mismatched geohashes or duplicate `site_id` values. The error files will be stored in the `./errors/06-04-2024` directory.

7. Review the generated error files in the `./errors/06-04-2024` directory to see the details of the mismatched geohashes and duplicate `site_id` entries for each retailer.
