"""
class used to read and write csv files
"""
import csv
import os
import logging

import coloredlogs

log = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


class CsvReader:
    def __init__(self, csv_directory):
        self.csv_directory = csv_directory
        self.origins_file = "origins.csv"
        self.destinations_file = "destinations.csv"
        self.origins = set()
        self.destinations = set()

    def read_directory(self):
        for file in os.listdir(self.csv_directory):
            if file.endswith(".csv") and not file.startswith("CDR format"):
                path = self.csv_directory + file
                self.read_file(path)

    def read_file(self, filename):
        with open(self.csv_directory + filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            log.info("Reading file " + filename)
            line_count = 0
            for row in csv_reader:
                if row[0] != ' orig_longitude':
                    line_count += 1
                    self.origins.add((row[1], row[0]))
                    self.destinations.add((row[3], row[2]))

        log.info("Finished reading %d rows", line_count)

    def write_to_files(self):
        with open(self.origins_file, "a", newline="") as origins_file, open(self.destinations_file, "a", newline="") as destinations_file:
            origins_writer = csv.writer(origins_file, delimiter=",")
            destinations_writer = csv.writer(destinations_file, delimiter=",")

            origins_writer.writerow(["origin_lat", "origin_long"])
            destinations_writer.writerow(["destination_lat", "destination_long"])

            for o, d in zip(self.origins, self.destinations):
                origins_writer.writerow([o[0], o[1]])
                destinations_writer.writerow([d[0], d[1]])

    def main(self):
        self.read_directory()
        self.write_to_files()


csvReader = CsvReader("../CDR SAMPLE (No User ID)/")
csvReader.main()
