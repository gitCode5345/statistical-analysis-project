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


def bootstrap_skew(data, n_bootstrap=1000, alpha=0.05):
    bootstrapped_skews = []
    n = len(data)
    for _ in range(n_bootstrap):
        sample = np.random.choice(data, size=n, replace=True)
        bootstrapped_skews.append(stats.skew(sample))
    lower = np.percentile(bootstrapped_skews, 100*alpha/2)
    upper = np.percentile(bootstrapped_skews, 100*(1-alpha/2))
    return lower, upper

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
                    prices.append(float(prices_str))
                except ValueError:
                    pass
            
            if pieces_str:
                try:
                    pieces.append(int(pieces_str))
                except ValueError:
                    pass

        alpha = 0.05

        if prices:
            n = len(prices)
            mean_price = np.mean(prices)
            median_price = np.median(prices)
            mode_price = stats.mode(prices).mode.item()
            stddev_price = np.std(prices, ddof=1)
            var_price = np.var(prices, ddof=1)
            skew_price = stats.skew(prices)
            se = stddev_price / np.sqrt(n)
            ci_mean = stats.t.interval(0.95, df=n-1, loc=mean_price, scale=se)

            chi2_lower = stats.chi2.ppf(alpha/2, df=n-1)
            chi2_upper = stats.chi2.ppf(1 - alpha/2, df=n-1)
            ci_var = ((n-1)*stddev_price**2 / chi2_upper, (n-1)*stddev_price**2 / chi2_lower)
            ci_std = (np.sqrt(ci_var[0]), np.sqrt(ci_var[1]))

            skew_ci = bootstrap_skew(prices, n_bootstrap=1000, alpha=alpha)

            percentile_5_price = np.percentile(prices, 5)
            percentile_25_price = np.percentile(prices, 25)
            percentile_75_price = np.percentile(prices, 75)
            percentile_95_price = np.percentile(prices, 95)

            print("\n=== Price Statistics ===")
            print("-" * 60)
            print(f"{'Max':<12}: {max(prices):>8.2f}$   {'Min':<12}: {min(prices):>8.2f}$")
            print(f"{'Mean':<12}: {mean_price:>8.2f}$   95% CI: ({ci_mean[0]:.2f}, {ci_mean[1]:.2f})")
            print(f"{'Median':<12}: {median_price:>8.2f}$   {'Mode':<12}: {mode_price:>8.2f}$")
            print(f"{'Variance':<12}: {var_price:>8.2f}$   {'Std Dev':<12}: {stddev_price:>8.2f}$")
            print(f"{'Std Dev CI':<12}: ({ci_std[0]:.2f}, {ci_std[1]:.2f})   {'Skewness':<12}: {skew_price:>8.2f}$")
            print(f"{'Skewness CI':<12}: ({skew_ci[0]:.2f}, {skew_ci[1]:.2f})")
            print(f"{'5th Percentile':<12}: {percentile_5_price:>8.2f}$   {'25th Percentile':<12}: {percentile_25_price:>8.2f}$")
            print(f"{'75th Percentile':<12}: {percentile_75_price:>8.2f}$   {'95th Percentile':<12}: {percentile_95_price:>8.2f}$")
            print("-" * 60)

        if pieces:
            n = len(pieces)
            mean_pieces = np.mean(pieces)
            median_pieces = np.median(pieces)
            mode_pieces = stats.mode(pieces).mode.item()
            stddev_pieces = np.std(pieces, ddof=1)
            var_pieces = np.var(pieces, ddof=1)
            skew_pieces = stats.skew(pieces)
            se = stddev_pieces / np.sqrt(n)
            ci_mean = stats.t.interval(0.95, df=n-1, loc=mean_pieces, scale=se)

            chi2_lower = stats.chi2.ppf(alpha/2, df=n-1)
            chi2_upper = stats.chi2.ppf(1 - alpha/2, df=n-1)
            ci_var = ((n-1)*stddev_pieces**2 / chi2_upper, (n-1)*stddev_pieces**2 / chi2_lower)
            ci_std = (np.sqrt(ci_var[0]), np.sqrt(ci_var[1]))

            skew_ci = bootstrap_skew(pieces, n_bootstrap=1000, alpha=alpha)

            percentile_5_pieces = np.percentile(pieces, 5)
            percentile_25_pieces = np.percentile(pieces, 25)
            percentile_75_pieces = np.percentile(pieces, 75)
            percentile_95_pieces = np.percentile(pieces, 95)

            print("\n=== Pieces Statistics ===")
            print("-" * 60)
            print(f"{'Max':<12}: {max(pieces):>8}   {'Min':<12}: {min(pieces):>8}")
            print(f"{'Mean':<12}: {mean_pieces:>8.2f}   95% CI: ({ci_mean[0]:.2f}, {ci_mean[1]:.2f})")
            print(f"{'Median':<12}: {median_pieces:>8}   {'Mode':<12}: {mode_pieces:>8}")
            print(f"{'Variance':<12}: {var_pieces:>8.2f}   {'Std Dev':<12}: {stddev_pieces:>8.2f}")
            print(f"{'Std Dev CI':<12}: ({ci_std[0]:.2f}, {ci_std[1]:.2f})   {'Skewness':<12}: {skew_pieces:>8.2f}")
            print(f"{'Skewness CI':<12}: ({skew_ci[0]:.2f}, {skew_ci[1]:.2f})")
            print(f"{'5th Percentile':<12}: {percentile_5_pieces:>8}   {'25th Percentile':<12}: {percentile_25_pieces:>8}")
            print(f"{'75th Percentile':<12}: {percentile_75_pieces:>8}   {'95th Percentile':<12}: {round(percentile_95_pieces, 3):>8}")
            print("-" * 60)


def price_to_piece_ratio(file):
    with open(file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        minPrice = 1000000000000
        maxPrice = 0
        
        prices = []
        pieces = []
        
        for row in reader:
            prices_str = row.get("US_retailPrice", "").strip()
            pieces_str = row.get("pieces", "").strip()
            name_str = row.get("name", "").strip()
            theme_str = row.get("theme", "").strip()

            price_value = float(prices_str)
            piece_count = int(pieces_str)

            price_per_piece = price_value / piece_count

            if price_per_piece < minPrice:
                minPrice = price_per_piece
                minPriceName = name_str

            if price_per_piece > maxPrice:
                if theme_str != "Books":
                    maxnotBooksPrice = price_per_piece
                    maxnotBooksPriceName = name_str
                
                maxPrice = price_per_piece
                maxPriceName = name_str

            if prices_str:
                price = float(prices_str)
                prices.append(price)

            if pieces_str:
                piece_count = int(pieces_str)
                pieces.append(piece_count)
        
        average = sum(prices) / sum(pieces)


        print("\n=== Price to Piece Ratio ===")
        print("-" * 100)
        print(f"Average cost per piece: {average:.2f}$")
        print(f"Minimum cost per piece: {minPrice:.2f}$ ({minPriceName})")
        print(f"Maximum cost per piece: {maxPrice:.2f}$ ({maxPriceName})")
        print(f"Maximum cost per piece (excluding 'Books' theme): {maxnotBooksPrice:.2f}$ ({maxnotBooksPriceName})")
        print("-" * 100)


def the_expensive_theme(file):
    with open(file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        lego_themes = {}

        for row in reader:
            prices_str = row.get("US_retailPrice", "").strip()
            pieces_str = row.get("pieces", "").strip()
            theme_str = row.get("theme", "").strip()

            price_value = float(prices_str)
            piece_count = int(pieces_str)

            if theme_str in lego_themes:
                lego_themes[theme_str][0] += price_value
                lego_themes[theme_str][1] += 1
            else:
                lego_themes[theme_str] = [price_value, piece_count]

        max_price_per_piece = 0
        expensive_theme_name = ""

        for theme, (total_price, total_pieces) in lego_themes.items():
            avarage_price_per_piece = total_price / total_pieces

            if avarage_price_per_piece > max_price_per_piece:
                max_price_per_piece = avarage_price_per_piece
                expensive_theme_name = theme
                
        print("\n=== Most Expensive LEGO Theme ===")
        print("-" * 50)
        print(f"The most expensive LEGO theme is '{expensive_theme_name}' with a price of {max_price_per_piece:.2f}$")
        print("-" * 50)
    
def run_full_analysis():
    fileter_csv("lego_sets.csv", "sorted_lego_sets.csv")
    analyze_csv("sorted_lego_sets.csv")
    price_to_piece_ratio("sorted_lego_sets.csv")
    the_expensive_theme("sorted_lego_sets.csv")


if __name__ == "__main__":
    run_full_analysis()
    