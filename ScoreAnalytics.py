# Ask for input for the Google Sheets credentials file in command line arguments
import sys
credentials_file = sys.argv[1] if len(sys.argv) > 1 else input("Please enter the path to your Google Sheets credentials JSON file: ")
# Ensure the credentials file is provided
if not credentials_file:
    print("Error: No credentials file provided. Please provide the path to your Google Sheets credentials JSON file.")
    exit(1)
# Ensure the credentials file exists
import os
if not os.path.exists(credentials_file):
    print(f"Error: The credentials file '{credentials_file}' does not exist.")
    exit(1)
# Ensure the required libraries are installed
try:
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError as e:
    print(f"Error: {e}. Please ensure you have the required libraries installed.")
    print("You can install them using pip:")
    print("pip install gspread oauth2client pandas matplotlib")
    exit(1)
# Ask if user want to convert data to percentage
convert_to_percentage = input("Do you want to convert the data to percentage? (yes/no): ").strip().lower()
while convert_to_percentage not in ['yes', 'no']:
    print("Invalid input. Please enter 'yes' or 'no'.")
    convert_to_percentage = input("Do you want to convert the data to percentage? (yes/no): ").strip().lower()
if convert_to_percentage == 'no':
    print("Note: The data will not be converted to percentage. Ensure your data is already in the correct format.")
    convert_to_percentage = False
else:
    convert_to_percentage = True
# Ask where to start searching for header rows
header_row = input("Please enter the row number to start searching for headers (default is 1): ")
header_row = int(header_row) if header_row.isdigit() else 1
if not header_row or header_row < 1:
    print("Error: Invalid header row number. Please enter a positive integer.")
    exit(1)
# Ask what is the expected header names
expected_headers = input("Please enter the expected header names separated by commas (default is 'Student Name, Total, Math, English, Science'): ")
expected_headers = [header.strip() for header in expected_headers.split(',')] if expected_headers else ['Student Name', 'Total', 'Math', 'English', 'Science']
# Ensure the expected headers are valid
if not all(isinstance(header, str) for header in expected_headers):
    print("Error: Invalid header names provided. Please ensure all headers are strings.")
    exit(1)
# Ask what subjects to include in the analysis
subjects = input("Please enter the subjects to include in the analysis separated by commas (default is 'Math, English, Science'): ")
subjects = [subject.strip() for subject in subjects.split(',')] if subjects else ['Math', 'English', 'Science']

# Authenticate and connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
client = gspread.authorize(creds)

# Load data from the sheet
sheet = client.open("Student Grades").sheet1  # Make sure your sheet is named exactly this
data = sheet.get_all_records(head=header_row,expected_headers=expected_headers)  # Get all rows as a list of dictionaries
# Convert to DataFrame for analysis
df_original = pd.DataFrame(data)
df = df_original.copy()

# Convert and update scores to percentage format in Google Sheets
if convert_to_percentage:
    print("\nWe'll convert scores to percentages in the sheet and decimals in code.")
    for subject in subjects:
        
        if subject in df.columns:
            print(f"\nConverting scores for subject: {subject}")
            print("\nChoose your current scoring format for this subject: ")
            print("\n1. Out of 100")
            print("\n2. Out of 10")
            print("\n3. Out of 20")
            print("\n4. Custom (you will enter the conversion factor)")
            choice = input("Enter your choice (1-4): ").strip()
            if choice == '1':
                pass  # Already in percentage format, no conversion needed
            elif choice == '2':
                df[subject] = df[subject].astype(float) / 10.0
            elif choice == '3':
                df[subject] = df[subject].astype(float) / 20.0
            elif choice == '4':
                while True:
                    print("You chose custom conversion. Please enter the conversion factor (e.g., if scores are out of 50, enter 50):")
                    try:
                        custom_factor = float(input().strip())
                        df[subject] = df[subject].astype(float) / custom_factor
                        break
                    except ValueError:
                        print("Invalid input. Please enter a numeric value.")
    # After all subjects are converted in the DataFrame
    cell_updates = []

    for subject in subjects:
        if subject not in df.columns:
            continue

        col_idx = df.columns.get_loc(subject) + 1  # gspread is 1-based
        for row_idx in range(len(df)):
            new_val = df.at[row_idx, subject]
            cell = gspread.Cell(row=row_idx + header_row + 1, col=col_idx, value=new_val)
            cell_updates.append(cell)

    if cell_updates:
        sheet.update_cells(cell_updates)
        print("✅ Batch update to Google Sheets completed.")


# Convert percentage strings to floats
for col in subjects:
    # Check if the column contains percentage strings
    if col not in df.columns:
        continue
    if df[col].dtype == 'object' and df[col].str.contains('%').any():
        df[col] = df[col].str.replace('%', '').astype(float) / 100

# Calculate averages and find top student
df['Average'] = df[subjects].mean(axis=1)
top_student = df.loc[df['Average'].idxmax()]

# Print top student info
print("Top Student:")
print(top_student)

# Plot average scores
plt.figure(figsize=(8, 5))
df.plot(kind='bar', x='Student Name', y='Average', legend=False, color='skyblue')
plt.title("Average Scores by Student")
plt.ylabel("Average Score")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("averages.png")  # Save to file
plt.show()  # Display the plot
