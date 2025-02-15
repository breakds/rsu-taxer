import openpyxl

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

# Create a new workbook
workbook = openpyxl.Workbook()

# Create a worksheet
worksheet = workbook.active
worksheet.title = "Tax Calculation"

# --- Input Cells ---
worksheet['A1'] = "Number of RSU Shares"
worksheet['B1'] = 1000  # Example value
worksheet['A2'] = "Price per Share at Tax Day"
worksheet['B2'] = 100  # Example value
worksheet['A3'] = "Other Income"
worksheet['B3'] = 150000  # Example value

# --- Formula Cells ---
worksheet['A5'] = "RSU Income"
worksheet['B5'] = "=B1*B2"  # Formula for RSU income
worksheet['A6'] = "Total Income"
worksheet['B6'] = "=B5+B3"  # Formula for total income

# Function to convert tax brackets to Excel if-else formula

def convert_brackets_to_formula(income_cell, brackets):
    parts = []
    for i in range(len(brackets) - 1):
        lower, rate = brackets[i]
        upper = brackets[i + 1][0]
        # Adjust bracket calculation by Excel cell income.
        parts.append(f"IF({income_cell}>{lower},MIN({income_cell}-{lower},{upper}-{lower})*{rate},0)")
    # Handle the top bracket
    lower, rate = brackets[-1]
    parts.append(f"IF({income_cell}>{lower},({income_cell}-{lower})*{rate},0)")
    return '+'.join(parts)

# Federal and state tax formulas
federal_tax_formula = convert_brackets_to_formula("B5", FEDERAL_BRACKETS)
california_tax_formula = convert_brackets_to_formula("B5", CALIFORNIA_BRACKETS)

# Placing the formulas into their respective cells
worksheet["A8"] = "Federal Tax on RSU"
worksheet["A9"] = "California Tax on RSU"
for cell, formula in zip(['B8', 'B9'], [federal_tax_formula, california_tax_formula]):
    worksheet[cell]=f'={formula}'

worksheet['A10'] = "Social Security Tax"
worksheet['B10'] = f"=MIN(B5, {SOCIAL_SECURITY_LIMIT})*{SOCIAL_SECURITY_RATE}"
worksheet['A11'] = "Medicare Tax"
worksheet['B11'] = f"=B5*{MEDICARE_RATE} + IF(B6>200000,(B6-200000)*{ADDITIONAL_MEDICARE_RATE}, 0)"

worksheet['A12'] = "Total Tax"
worksheet['B12'] = "=B8+B9+B10+B11"

worksheet['A13'] = "Net After Tax"
worksheet['B13'] = "=B5-B12"

worksheet['A14'] = "Break-even Price per Share"
worksheet['B14'] = "=B12/B1"

# Save the workbook
workbook.save("rsu_tax_calculator.xlsx")

print("Excel file 'rsu_tax_calculator.xlsx' created successfully.")

