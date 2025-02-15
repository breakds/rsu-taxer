from typing import NamedTuple
from rich.console import Console
from rich import print

# Define tax brackets and rates
FEDERAL_BRACKETS = [
    (0, 0.10), (11600, 0.12), (47150, 0.22), (100525, 0.24),
    (191950, 0.32), (243725, 0.35), (609350, 0.37)
]

CALIFORNIA_BRACKETS = [
    (0, 0.01), (10412, 0.02), (49223, 0.04), (62163, 0.06),
    (322499, 0.08), (412187, 0.093), (1000000, 0.103),
    (1200000, 0.113), (1500000, 0.123)
]

# Social Security and Medicare rates
SOCIAL_SECURITY_RATE = 0.062
SOCIAL_SECURITY_LIMIT = 168600
MEDICARE_RATE = 0.0145
ADDITIONAL_MEDICARE_RATE = 0.009  # Applies above $200,000

# Default withholding rates
FEDERAL_WITHHOLDING_RATE = 0.22
CALIFORNIA_WITHHOLDING_RATE = 0.093

# Define a named tuple for output
class TaxEstimate(NamedTuple):
    federal_tax: float
    california_tax: float
    social_security_tax: float
    medicare_tax: float
    total_tax: float
    withholding: float
    net_after_tax: float
    break_even_price: float

def compute_taxes(num_shares: int, price_per_share: float, other_income: float) -> TaxEstimate:
    rsu_income = num_shares * price_per_share
    total_income = rsu_income + other_income
    
    def progressive_tax(income, brackets):
        tax = 0
        for i in range(len(brackets) - 1):
            lower, rate = brackets[i]
            upper = brackets[i + 1][0]
            if income > lower:
                taxable = min(income, upper) - lower
                tax += taxable * rate
            else:
                break
        if income > brackets[-1][0]:
            tax += (income - brackets[-1][0]) * brackets[-1][1]
        return tax

    # Compute Federal Tax
    federal_tax = progressive_tax(total_income, FEDERAL_BRACKETS)
    
    # Compute California State Tax
    california_tax = progressive_tax(total_income, CALIFORNIA_BRACKETS)
    
    # Compute Social Security Tax
    social_security_tax = min(rsu_income, SOCIAL_SECURITY_LIMIT - max(0, total_income - rsu_income)) * SOCIAL_SECURITY_RATE
    
    # Compute Medicare Tax
    medicare_tax = rsu_income * MEDICARE_RATE
    if total_income > 200000:
        medicare_tax += (total_income - 200000) * ADDITIONAL_MEDICARE_RATE
    
    # Compute total tax
    total_tax = federal_tax + california_tax + social_security_tax + medicare_tax
    
    # Compute default employer withholding (may be under-withheld)
    federal_withholding = rsu_income * FEDERAL_WITHHOLDING_RATE
    california_withholding = rsu_income * CALIFORNIA_WITHHOLDING_RATE
    total_withholding = federal_withholding + california_withholding + social_security_tax + medicare_tax

    net_after_tax = rsu_income - total_tax
    break_even_price = total_tax / num_shares

    return TaxEstimate(
        federal_tax=round(federal_tax, 2),
        california_tax=round(california_tax, 2),
        social_security_tax=round(social_security_tax, 2),
        medicare_tax=round(medicare_tax, 2),
        total_tax=round(total_tax, 2),
        withholding=round(total_withholding, 2),
        net_after_tax=round(net_after_tax, 2),
        break_even_price=round(break_even_price, 2)
    )


if __name__ == "__main__":
    console = Console()
    num_shares = int(input("Enter the number of RSU shares: "))
    console.print(f"Number of shares: {num_shares}")
    price_per_share = float(input("Enter the price per share at tax day: "))
    console.print(f"Price per share: {price_per_share}")
    other_income = float(input("Enter your other income: "))
    console.print(f"Other income: {other_income}")
    taxes = compute_taxes(num_shares, price_per_share, other_income)
    console.print(f"Federal Tax: {taxes.federal_tax}")
    console.print(f"California Tax: {taxes.california_tax}")
    console.print(f"Social Security Tax: {taxes.social_security_tax}")
    console.print(f"Medicare Tax: {taxes.medicare_tax}")
    console.print(f"Total Tax: {taxes.total_tax}")
    console.print(f"Withholding: {taxes.withholding}")
    console.print(f"Net After Tax: {taxes.net_after_tax}")
    console.print(f"Break-even price per share: {taxes.break_even_price}")
