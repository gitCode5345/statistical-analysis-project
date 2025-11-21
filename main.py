import csv


def fileter_csv(input_file, output_file):
    infile = open(input_file, "r", encoding="utf-8")
    reader = csv.reader(infile)

    outfile = open(output_file, "w", encoding="utf-8", newline="")
    writer = csv.writer(outfile)

    for row in reader:
        if all(cell.strip() != "" for cell in row):
            writer.writerow(row)

    infile.close()
    outfile.close()


data = fileter_csv("lego_sets.csv", "sorted_lego_sets.csv")

