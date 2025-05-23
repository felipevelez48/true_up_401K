import pandas as pd
import os

def generate_recap_for_id (employee_id, df_elegibles):
    row = df_elegibles[df_elegibles['ID'] == employee_id].copy()

    if row.empty:
        print(f"Employee with {employee_id} not found in the list of elegibles. \n Please check the the list of non elegibles and the reason")
        return
    row_data = row.iloc[0]
    plan_comp = row_data['Plan_eligible_comp'] if pd.notnull(row_data['Plan_eligible_comp']) else 0
    total_deferral = row_data['Total_Deferral'] if pd.notnull(row_data['Total_Deferral']) else 0
    deferral_pct = row_data['Deferral_Pct'] if pd.notnull(row_data['Deferral_Pct']) else 0
    match_pct = row_data['Match_Pct'] if pd.notnull(row_data['Match_Pct']) else 0
    employer_match_actual = row_data['Employer_Match_Actual'] if pd.notnull(row_data['Employer_Match_Actual']) else 0
    expected_employer_match = row_data['Expected_Employer_Match'] if pd.notnull(row_data['Expected_Employer_Match']) else 0
    true_up_amount = row_data['True_up_Amount'] if pd.notnull(row_data['True_up_Amount']) else 0


    resumen = f"""
Resumen True-Up for the employee: {employee_id}
------------------------------------------------------------
Payment Frequency: Monthly
Employer Matching Formula: 100% up to 3%, 50% from 3% to 5% (maximum 4%)

Annual compensation plan: ${plan_comp:,.2f}
Total employee contribution: ${total_deferral:,.2f}
Annual savings percentage: {deferral_pct:.2%}
Match percentage applied:  {match_pct:.2%}

Employer match during the year: ${employer_match_actual:,.2f}
Expected match at year-end: ${expected_employer_match:,.2f}
------------------------------------------------------------
True-up required (final adjustment): ${true_up_amount:,.2f}
------------------------------------------------------------
"""
    print(resumen)

if __name__ == "__main__":
    
    output_folder = '../outputs/'
    eligible_file_name = 'eligible_true_up.csv'
    eligible_file_path = os.path.join(output_folder, eligible_file_name)

    if not os.path.exists(eligible_file_path):
        print(f"Error: The file '{eligible_file_name}' did not found in the path.")
    
    else:
        try:
            elegible_df = pd.read_csv(eligible_file_path)
            print(f"\nDataFrame '{eligible_file_name}' load.")
            
            numeric_cols_for_summary = [
                'Plan_eligible_comp', 'Total_Deferral', 'Deferral_Pct',
                'Match_Pct', 'Employer_Match_Actual', 'Expected_Employer_Match',
                'True_up_Amount'
            ]
            for col in numeric_cols_for_summary:
                if col in elegible_df.columns:
                    elegible_df[col] = pd.to_numeric(elegible_df[col], errors='coerce')


            emp_id = input("\nEnter the employee ID (e.g. Employee 1): ")
            generate_recap_for_id(emp_id, elegible_df)

        except Exception as e:
            print(f"An error occurred while uploading or processing the CSV file: {e}")
