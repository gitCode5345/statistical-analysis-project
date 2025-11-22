import csv
import numpy as np
from scipy import stats

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


def analyze_csv(file):
    with open(file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        prices = []
        pieces = []

        for row in reader:
            prices_str = row.get("US_retailPrice", "").strip()
            pieces_str = row.get("pieces", "").strip()

            if prices_str:
                try:
                    price = float(prices_str)
                    prices.append(price)
                except ValueError:
                    pass
            
            if pieces_str:
                try:
                    piece_count = int(pieces_str)
                    pieces.append(piece_count)
                except ValueError:
                    pass

        if prices:
            max_price = max(prices)
            min_price = min(prices)
            mean_price = np.mean(prices)
            median_price = np.median(prices)
            mode_price = stats.mode(prices).mode.item()
            stddev_price = np.std(prices)
            skew_price = stats.skew(prices)
            var_price = np.var(prices)

            print("\n=== Price Statistics ===")
            print("-" * 50)
            print(f"{'Max':<12}: {max_price:>8.2f}$   {'Min':<12}: {min_price:>8.2f}$")
            print(f"{'Mean':<12}: {mean_price:>8.2f}   {'Median':<12}: {median_price:>8.2f}")
            print(f"{'Mode':<12}: {mode_price:>8.2f}   {'Variance':<12}: {var_price:>8.2f}")
            print(f"{'Std Dev':<12}: {stddev_price:>8.2f}   {'Skewness':<12}: {skew_price:>8.2f}")
            print("-" * 50)

        if pieces:
            max_pieces = max(pieces)
            min_pieces = min(pieces)
            mean_pieces = np.mean(pieces)
            median_pieces = np.median(pieces)
            mode_pieces = stats.mode(pieces).mode.item()
            stddev_pieces = np.std(pieces)
            skew_pieces = stats.skew(pieces)
            var_pieces = np.var(pieces)

            print("\n=== Pieces Statistics ===")
            print("-" * 50)
            print(f"{'Max':<12}: {max_pieces:>8}   {'Min':<12}: {min_pieces:>8}")
            print(f"{'Mean':<12}: {mean_pieces:>8.2f}   {'Median':<12}: {median_pieces:>8}")
            print(f"{'Mode':<12}: {mode_pieces:>8}   {'Variance':<12}: {var_pieces:>8.2f}")
            print(f"{'Std Dev':<12}: {stddev_pieces:>8.2f}   {'Skewness':<12}: {skew_pieces:>8.2f}")
            print("-" * 50)


fileter_csv("lego_sets.csv", "sorted_lego_sets.csv")
analyze_csv("sorted_lego_sets.csv")
