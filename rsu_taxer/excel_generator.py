import openpyxl

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

# Federal Tax (using a simplified example - replace with actual tax bracket logic)
worksheet['A8'] = "Federal Tax"
worksheet['B8'] = "=IF(B6<=11000, B6*0.1, IF(B6<=44725, 1100+ (B6-11000)*0.12, B6*0.22))"  # Example

#California Tax (using a simplified example - replace with actual tax bracket logic)
worksheet['A9'] = "California Tax"
worksheet['B9'] = "=IF(B6<=10000, B6*0.01, IF(B6<=50000, 100+ (B6-10000)*0.02, B6*0.04))"  # Example

worksheet['A10'] = "Social Security Tax"
worksheet['B10'] = "=MIN(B5,168600)*0.062"
worksheet['A11'] = "Medicare Tax"
worksheet['B11'] = "=B5*0.0145"

worksheet['A12'] = "Total Tax"
worksheet['B12'] = "=B8+B9+B10+B11"

worksheet['A13'] = "Net After Tax"
worksheet['B13'] = "=B5-B12"

worksheet['A14'] = "Break-even Price per Share"
worksheet['B14'] = "=B12/B1"

# Save the workbook
workbook.save("rsu_tax_calculator.xlsx")

print("Excel file 'rsu_tax_calculator.xlsx' created successfully.")