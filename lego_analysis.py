import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("./sorted_lego_sets.csv")

prices = df["US_retailPrice"].astype(float)
pieces = df["pieces"].astype(int)

plt.figure(figsize=(10, 5))
plt.hist(prices, bins=50)
plt.title("Histogram of Prices")
plt.xlabel("Price ($)")
plt.ylabel("Frequency")
plt.show()

plt.figure(figsize=(10, 5))
plt.hist(pieces, bins=50)
plt.title("Histogram of Piece Counts")
plt.xlabel("Number of pieces")
plt.ylabel("Frequency")
plt.show()

log_prices = np.log(prices[prices > 0])

plt.figure(figsize=(10, 5))
plt.hist(log_prices, bins=50, density=True)
xmin, xmax = plt.xlim()

mu, sigma = stats.norm.fit(log_prices)
x = np.linspace(xmin, xmax, 200)
pdf = stats.norm.pdf(x, mu, sigma)
plt.plot(x, pdf)
plt.title("Log-Prices Histogram with Normal PDF")
plt.xlabel("log(price)")
plt.ylabel("Density")
plt.show()

shapiro_raw = stats.shapiro(prices)
shapiro_log = stats.shapiro(log_prices)

ks_log = stats.kstest(log_prices, "norm", args=(mu, sigma))

print("\n=== Distribution Tests ===")
print("Shapiro-Wilk on RAW prices:", shapiro_raw)
print("Shapiro-Wilk on LOG-prices:", shapiro_log)
print("KS test on log-normal hypothesis:", ks_log)
