import pandas as pd
from datetime import datetime
import os

today= pd.to_datetime('today')
filename = 'ForUsAll_External Technical Test CSV File - Employee Census Data.csv'

try:
    file_path= os.path.join('../data', filename) 
    df= pd.read_csv(file_path, na_values=['0', '0.00', '$0.00'],encoding='utf-8', thousands=',')

    print(f"----------Successfully uploaded {filename}!-------------")
    print(f"\n First 5 rows of the df: \n")
    print(df.head())
except FileNotFoundError:
    print("Error: The file does not find in the path. \n Make sure to put the correct path")
except Exception as e:
    print(f"Error to load the file .csv: {e}")

df.columns= df.columns.str.strip().str.replace(' ','_').str.replace('(','').str.replace(')','')

#print(df.columns)

date_columns = [
    'Birth_Date_MM/DD/YYYY', 
    'Hire_Date', 
    'Termination_Date',
    'Rehire_Date',
    'Entry_date'
]
clean_date_columns = [col.strip().replace(' ', '_').replace('(', '').replace(')', '') for col in date_columns]

num_columns = [
    'Gross_compensation',
    'Plan_eligible_comp',
    'Employee_deduction_1_Pre-tax_amount',
    'Employee_deduction_2_Roth_Deferral'
]


for col in num_columns:
    cleaned_strings = df[col].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False)
    df[col] = pd.to_numeric(cleaned_strings, errors='coerce')
    

print(f"\n \n The clenaing columns are: \n {num_columns}")

#print(f"\n \n las columnas limpias son: \n {clean_date_columns}")
for col in clean_date_columns:
    df[col]= pd.to_datetime(df[col], errors='coerce', format='%m/%d/%y')

current_year=datetime.now().year

df['Birth_Date_MM/DD/YYYY'] = df['Birth_Date_MM/DD/YYYY'].apply(
    lambda x: x - pd.DateOffset(years=100) if pd.notnull(x) and x.year > current_year - 18 else x
)

#print(df[clean_date_columns].head())
#print(f"\n \n \n the new df: \n {df.head()}")

df['Age']= df['Birth_Date_MM/DD/YYYY'].apply(
    lambda x: (today.year - x.year) if pd.notnull(x) else None
    )
df['Ternure_Years'] = ((df['Termination_Date'].fillna(today)-df['Hire_Date']) / pd.Timedelta(days=365)).round(2)
df['Is_Active'] = df['Termination_Date'].isna()

print(f"\n \n \n the new df: \n {df.info()} ")

#----------------------------------------------------------------------------------------------------------------

cutoff_date= pd.to_datetime('2023-01-01')

elegible_df = df[ (df['Entry_date'] < cutoff_date) &
                 (df['Is_Active']) &
                 (df['Hours_worked_2022'] >= 1000) &
                 (df['Employee_Status'].str.strip().str.lower() == 'full-time')
].copy()
print(f"The number og eligible employees for promotion is: {len(elegible_df)}")

# So the formula is employee_deferral_pct = (pre-tax+roth)/plan_elegieble_comp
elegible_df['Total_Deferral'] = elegible_df['Employee_deduction_1_Pre-tax_amount'].fillna(0) + elegible_df['Employee_deduction_2_Roth_Deferral'].fillna(0)

elegible_df['Deferral_Pct'] = elegible_df['Total_Deferral'] / elegible_df['Plan_eligible_comp']

match_comp = elegible_df['Plan_eligible_comp'].clip(upper=305000)

elegible_df['Match_Pct'] = elegible_df['Deferral_Pct'].apply(lambda x: x if x <= 0.03 else (0.03 + min(x - 0.03, 0.02) * 0.5))

elegible_df['Match_Pct'] = elegible_df['Match_Pct'].clip(upper=0.04)

elegible_df['Expected_Employer_Match'] = (match_comp * elegible_df['Match_Pct']).round(2)

elegible_df['Employer_Match_Actual'] = elegible_df['Employer_Match'].fillna(0)

elegible_df['True_up_Amount'] = elegible_df['Expected_Employer_Match'] - elegible_df['Employer_Match_Actual']

elegible_df['Expected_Employer_Match'] = elegible_df['Expected_Employer_Match'].clip(upper=12200)

elegible_df['True_up_Amount'] = (elegible_df['Expected_Employer_Match'] - elegible_df['Employer_Match'].fillna(0)).clip(lower=0).round(2)

#print(elegible_df.head())

def get_ineligibility_reason(row):
    reasons = []
    if pd.isna(row['Entry_date']) or row['Entry_date'] >= pd.Timestamp("2023-01-01"):
        reasons.append("Entry date after 2022")
    if not row['Is_Active']:
        reasons.append("Not active on 12/31/2022")
    if row['Hours_worked_2022'] < 1000:
        reasons.append("Less than 1000 hours")
    if str(row['Employee_Status']).strip().lower() != "full-time":
        reasons.append("Not full-time")
    return "; ".join(reasons) if reasons else None

# Crear df de no elegibles
non_eligible_df = df[~df.index.isin(elegible_df.index)].copy()
non_eligible_df['Ineligibility_Reason'] = non_eligible_df.apply(get_ineligibility_reason, axis=1)

output_folder= '../outputs/'
os.makedirs(output_folder, exist_ok=True)

elegible_output_filename= "eligible_true_up.csv"
elegible_output_path= os.path.join(output_folder,elegible_output_filename)

non_elegible_output_filename= "non_eligible_employees.csv"
non_elegible_output_path= os.path.join(output_folder,non_elegible_output_filename)

# Elegibles con True-up
elegible_df.to_csv(elegible_output_path, index=False)

# No elegibles con razones
non_eligible_df.to_csv(non_elegible_output_path, index=False)




print(f" \n \n \n\n \n \n --------✅Files save successfully in: {output_folder} ✅------------\n \n \n\n \n \n")
