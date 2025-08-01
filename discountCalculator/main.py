from discountCalculator.calculation import DiscountCalculator
from discountCalculator.loadExcel import load_excel
from configparser import ConfigParser
from pathlib import Path
import pandas as pd
import os
import numpy as np
def main(input_file=None, output_file=None):
    print("🔍 Starting discount calculation...")
    config = ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read(config_path, encoding='utf-8')
    input_path = Path(input_file)
    if input_path.is_dir():
        excel_files = list(input_path.glob("*.xlsx"))
        if not excel_files:
            print("❌ No Excel files found in the folder.")
            return
        input_path = excel_files[0]

    print(f"📂 Using Excel file: {input_path}")
    df = load_excel(input_path)

    if df is not None:
        col_discount = config['Settings']['COLUMN_DISCOUNT']
        col_debt = config['Settings']['COLUMN_DEBT_SUM']
        col_overdue = config['Settings']['COLUMN_OVERDUE_BODY']

        df[col_discount] = df.apply(
            lambda row: DiscountCalculator(row[col_debt], row[col_overdue]).calculate_discount(),
            axis=1
        )

        df.to_excel(input_path, index=False)  # Перезаписуємо той самий файл
        print(f"💾 File overwritten: {input_path}")

def compare_excel_files(file1, file2, key_columns=None):
    # Зчитування Excel-файлів
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    # Якщо вказано ключові колонки — встановлюємо індекс для порівняння
    if key_columns:
        df1 = df1.set_index(key_columns)
        df2 = df2.set_index(key_columns)

    # Вирівнюємо типи та сортуємо
    df1 = df1.sort_index().astype(str)
    df2 = df2.sort_index().astype(str)

    # Рядки, які є в df2, але не в df1
    added = df2[~df2.index.isin(df1.index)]

    # Рядки, які є в df1, але не в df2
    removed = df1[~df1.index.isin(df2.index)]

    # Рядки з однаковим індексом, але зміненим вмістом
    common = df1[df1.index.isin(df2.index)]
    updated = df2[df2.index.isin(df1.index)]
    changed = common[common.ne(updated)].dropna(how='all')

    return {
        'added': added,
        'removed': removed,
        'changed': changed
    }

def compare():
    # compare two excel files
    result = compare_excel_files(
        "ТЕСТ_empty.xlsx",
        "ТЕСТ.xlsx",
        key_columns=["id"]  # або None
    )

    # Порівняльна таблиця: старі vs нові значення
    common_ids = result['changed'].index
    df_old = pd.read_excel('ТЕСТ_empty.xlsx').set_index('id')
    df_new = pd.read_excel('ТЕСТ.xlsx').set_index('id')

    comparison = pd.concat([df_old.loc[common_ids], df_new.loc[common_ids]],
                           axis=1,
                           keys=["OLD", "NEW"])

    # Порівняння лише "Дисконт (до)"
    discount_comparison = comparison[[("OLD", "Дисконт (до)"), ("NEW", "Дисконт (до)")]].copy()
    discount_comparison.columns = ["OLD_Дисконт", "NEW_Дисконт"]
    discount_comparison["Сума боргу, грн"] = df_new.loc[common_ids, "Сума боргу, грн"].values
    discount_comparison["Просрочене тіло, грн"] = df_new.loc[common_ids, "Просрочене тіло, грн"].values

    # Обчислити різницю


    # Показати лише ті, де справді щось змінилося
    changed_only = discount_comparison[
        ~np.isclose(
            discount_comparison["NEW_Дисконт"].astype(float),
            discount_comparison["OLD_Дисконт"].astype(float),
            atol=1e-5
        )
    ]
    pd.set_option('display.max_rows', None)
    print("\n📊 Порівняння дисконту (тільки зміни):")
    print(f"Total changes: {len(changed_only)}")
    print(changed_only)
if __name__     == "__main__":
     config = ConfigParser()
     config.read('config.ini', encoding='utf-8')
     file_name = config['Settings']['FILE_NAME_DISCOUNT']
     main(file_name, output_file="discounted_" + file_name)
     #print(DiscountCalculator("7146.30", "4200.00").calculate_discount())
     compare()


