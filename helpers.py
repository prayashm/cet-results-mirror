import csv


def write_to_csv(data):
    with open("../data/results.csv", "w") as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        for row in data:
            writer.writerow(row)

