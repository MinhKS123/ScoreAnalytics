# Score Analytics

**Score Analytics** is a Python-powered tool that analyzes student scores from Google Sheets. It supports converting raw scores into percentages, calculating average scores, identifying top students, and visualizing the results with a chart.

## ✨ Features

- 🔐 Connects to Google Sheets using a service account
- 🔄 Converts scores from 10, 20, 100, or custom scales to percentages
- 🧮 Computes average scores for selected subjects
- 🏆 Identifies the top-performing student
- 📊 Generates a bar chart of student averages
- 📤 Batch updates Google Sheets with formatted percentage values

## 📦 Requirements

- Python 3.7 or later
- Google Sheets API credentials (JSON file)
- Required libraries (install with `pip install -r requirements.txt`)

Install requirements:

```bash
pip install -r requirements.txt
```

🚀 How to Use
python main.py path/to/credentials.json
The script will guide you through:

Specifying the header row and expected column names

Choosing the subjects to include in the analysis

Selecting how to convert each subject’s score (out of 10, 20, 100, or custom)

After running, it will update your Google Sheet with converted percentage values and save a bar chart to averages.png.

🧪 Example Interaction
```bash
Do you want to convert the data to percentage? (yes/no): yes
Please enter the row number to start searching for headers: 3
Please enter the expected header names: Student Name, Math, English, Science
Please enter the subjects to include: Math, English, Science

Choose your current scoring format for this subject:
1. Out of 100
2. Out of 10
3. Out of 20
4. Custom
Enter your choice (1-4): 2
📂 Output
averages.png: A bar chart showing average scores per student

Updated values in your Google Sheet (as formatted percentages like 85.00%)
```
🧾 License
This project is licensed under the MIT License. See the LICENSE file for more details.

🙋 Support
Feel free to open issues or pull requests to contribute or report bugs!

```graphql
score-analytics/
├── main.py                  # Main script for data analysis
├── requirements.txt         # List of required Python packages
├── README.md                # Project documentation and usage instructions
├── LICENSE                  # Open source license (MIT)
├── .gitignore               # Git ignore rules
├── averages.png             # Output plot 
└── credentials.json         # Your Google Sheets API credentials 
```
