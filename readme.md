# TRUE_UP_401K

This project calculates the **Employer Match True-Up** for a 401(k) retirement plan, based on employee deferrals, employer match rules, and eligibility criteria. It uses data cleaning, filtering, and business rule implementation in Python, and is organized for review and automation.

## 📁 Project Structure


```plaintext
TRUE_UP_401K/
│
├── data/
│ └── ForUsAll_External Technical Test CSV File - Employee Census Data.csv
│
├── notebooks/
│ └── exploration.ipynb # Initial data exploration and cleaning
│
├── scripts/
│ ├── trueup_calculation.py # Cleans data, filters eligible employees, calculates true-up
│ └── recap_true_up.py # Allows per-employee recap summary by ID
│
├── gpt_interaction/
│ └── chat_transcript.md # ChatGPT conversation for documentation and context
│
├── outputs/
│ ├── eligible_true_up.csv # List of employees with their respective calculations
│ └── non_eligible_employees.csv # List of employees who do not meet the requirements with reasons
│
└── README.md # This file

```

⚙️ Features
Cleans and formats census data for processing.

Applies eligibility rules:

Full-time employee status.

1,000+ hours worked in 2022.

Plan entry date before January 1, 2023.

Active on December 31, 2022.

Calculates:

Employee deferral percentage.

Employer match using a tiered formula.

True-up amount (difference between actual match and entitled match).

Outputs results as CSV files in the outputs/ folder:

eligible_true_up.csv — eligible employees and their respective calculations.

non_eligible_employees.csv — ineligible employees with reasons for ineligibility.

Includes a per-employee recap script (recap_true_up.py) for detailed summaries by Employee ID.

## 🚀 How to Run

1. Clone the repository
```bash
git clone https://github.com/felipevelez48/true_up_401K.git
cd true_up_401K
```
2. Install the required dependencies:
```bash
pip install pandas
```
3. Place your census CSV file into the data/ directory.
4. Run the main script:
```bash
python scripts/trueup_calculation.py
```
5. To get a recap for a specific employee:
```bash
python scripts/recap_true_up.py --Employee 16
```

# 💡 Autor 📊🤖
## John Felipe Vélez
### Data Engineer