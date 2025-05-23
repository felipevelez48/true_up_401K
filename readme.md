# TRUE_UP_401K

This project calculates the **Employer Match True-Up** for a 401(k) retirement plan, based on employee deferrals, employer match rules, and eligibility criteria. It uses data cleaning, filtering, and business rule implementation in Python, and is organized for review and automation.

## 📁 Project Structure
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

## ⚙️ Features

- Cleans and formats census data for processing
- Applies eligibility rules:
  - Full-time status
  - 1,000+ hours worked in 2022
  - Entry date before Jan 1, 2023
  - Active as of the last day of 2022
- Calculates:
  - Employee deferral percentage
  - Employer match based on a tiered formula
  - True-up amount (difference between actual and entitled match)
- Outputs results as CSV files in the `outputs/` folder:
  - `elegible_true_up.csv` — eligible employees with true-up amounts
  - `non_elegible_employee.csv` — non-eligible employees with reasons for ineligibility
- Includes a per-employee recap script (`recap_true_up.py`) for detailed summaries by Employee ID

## 🚀 How to Run

1. Clone the repository
2. Place your census CSV in the `data/` directory
3. Install dependencies: pandas
4. Run in terminal: python  true_up_calculation.py
5. Check. If you want a resume for only one employee, run recap_tru_up.py