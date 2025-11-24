import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./sorted_lego_sets.csv')

def calculate_bayes_manual(df, condition_A, condition_B, label_A, label_B):
    N = len(df)

    count_A = len(df[condition_A])
    p_a = count_A / N

    count_B = len(df[condition_B])
    p_b = count_B / N

    intersection = len(df[condition_A & condition_B])
    p_b_given_a = intersection / count_A if count_A > 0 else 0

    p_a_given_b = (p_b_given_a * p_a) / p_b if p_b > 0 else 0

    print("\n--------------------------------------------")
    print(f"Bayesian Calculation: P({label_A} | {label_B})")
    print("--------------------------------------------")
    print(f"Total dataset size (N): {N}")
    print(f"Count(A) [{label_A}]: {count_A}")
    print(f"P(A): {p_a:.4f}")
    print(f"Count(B) [{label_B}]: {count_B}")
    print(f"P(B): {p_b:.4f}")
    print(f"Intersection A ∩ B: {intersection}")
    print(f"P(B|A): {p_b_given_a:.4f}")
    print(f"Posterior P(A|B): {p_a_given_b:.4f}")
    print("--------------------------------------------")

    return p_a, p_a_given_b


# Scenario 1: P(Licensed | Pieces > 1000)
cond_A1 = df['themeGroup'] == 'Licensed'
cond_B1 = df['pieces'] > 1000
p_a1, p_post1 = calculate_bayes_manual(df, cond_A1, cond_B1,
                                       "Licensed", "Pieces > 1000")

# Scenario 2: P(Price > $100 | Minifigs > 6)
cond_A2 = df['US_retailPrice'] > 100
cond_B2 = df['minifigs'] > 6
p_a2, p_post2 = calculate_bayes_manual(df, cond_A2, cond_B2,
                                       "Price > $100", "Minifigs > 6")

# Scenario 3: P(Star Wars | Age ≥ 12)
cond_A3 = df['theme'] == 'Star Wars'
cond_B3 = df['agerange_min'] >= 12
p_a3, p_post3 = calculate_bayes_manual(df, cond_A3, cond_B3,
                                       "Star Wars", "Age ≥ 12")

# Pre-calculation for Scenario 5
df['price_per_piece'] = df['US_retailPrice'] / df['pieces']
median_ppp = df['price_per_piece'].median()

# Scenario 4: P(Large Set (>1k pcs) | Year >= 2018)
cond_A4 = df['pieces'] > 1000
cond_B4 = df['year'] >= 2018
p_a4, p_post4 = calculate_bayes_manual(df, cond_A4, cond_B4,
                                       "Large Set (>1k pcs)", "Year >= 2018")

# Scenario 5: P(High PPP | Licensed)
cond_A5 = df['price_per_piece'] > median_ppp
cond_B5 = df['themeGroup'] == 'Licensed'
p_a5, p_post5 = calculate_bayes_manual(df, cond_A5, cond_B5,
                                       "High PPP", "Licensed")

# Scenario 6: P(Cheap (<$10) | 1 Minifig)
cond_A6 = df['US_retailPrice'] < 10
cond_B6 = df['minifigs'] == 1
p_a6, p_post6 = calculate_bayes_manual(df, cond_A6, cond_B6,
                                       "Cheap (<$10)", "1 Minifig")


def plot_scenarios(fignum, scenarios, priors, posteriors, title):
    x = range(len(scenarios))
    width = 0.35
    
    plt.figure(fignum, figsize=(10, 6))
    plt.bar([i - width / 2 for i in x], priors, width,
            label='Prior P(A)', color='skyblue')
    plt.bar([i + width / 2 for i in x], posteriors, width,
            label='Posterior P(A|B)', color='salmon')

    plt.ylabel('Probability')
    plt.title(title)
    plt.xticks(x, scenarios)
    plt.legend()
    plt.tight_layout()


scenarios_1 = [
    'Licensed | Pieces > 1000',
    'Price > $100 | Minifigs > 6',
    'Star Wars | Age ≥ 12'
]
priors_1 = [p_a1, p_a2, p_a3]
posteriors_1 = [p_post1, p_post2, p_post3]

plot_scenarios(2, scenarios_1, priors_1, posteriors_1, 
               'Bayesian analysis №2')

scenarios_2 = [
    'Large Set | New Year',
    'High PPP | Licensed',
    'Cheap | 1 Minifig'
]
priors_2 = [p_a4, p_a5, p_a6]
posteriors_2 = [p_post4, p_post5, p_post6]

plot_scenarios(1, scenarios_2, priors_2, posteriors_2, 
               'Bayesian analysis №1')

plt.show()
