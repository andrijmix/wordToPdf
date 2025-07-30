#I have an exel file with the following columns:
# id	     Дисконт (до)	Сума боргу, грн	Просрочене тіло, грн
# 25770894745		        1 864,75	    1 001,40
# 25770894769		        3 121,20	    1 400,00
# 25770894621		        3 684,92	    1 336,20
# 25770894664		        4 083,60	    2 400,00
# 25770894697		        4 083,60	    2 400,00
# 25770894756		        4 083,60	    2 400,00
# 25770894815		        4 083,60	    2 400,00
# 25770894902		        4 083,60	    2 400,00
#
#Need to load this excel file and calculate the discount for each row.
import pandas as pd
from pathlib import Path
from configparser import ConfigParser
def load_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        print(f"📊 Loaded {len(df)} rows from {file_path.name}")
        return df
    except Exception as e:
        print(f"🚨 Error loading Excel file: {e}")
        return None

if __name__  == "__main__":
    # Example usage
    #get pinformation via config.ini

    config = ConfigParser()
    config.read('config.ini', encoding='utf-8')

    file_name = config['Settings']['FILE_NAME_DISCOUNT']
    col_discount = config['Settings']['COLUMN_DISCOUNT']
    col_debt = config['Settings']['COLUMN_DEBT_SUM']
    col_overdue = config['Settings']['COLUMN_OVERDUE_BODY']

    print(f"📂 Using Excel file: {file_name}")
    excel_file = Path(file_name)  # Replace with your actual file path
    df = load_excel(excel_file)

    if df is not None:
        print(df.head())  # Display the first few rows of the DataFrame
        # Further processing can be done here, e.g., calculating discounts
        # Example calculation (assuming columns are numeric)
