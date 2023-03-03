import pandas as pd

df = pd.read_excel('./files/bc.xlsx')
bc_df = (df[['BC Code', 'TS', 'Store code', 'Store name']])

sc_df = pd.read_csv('./files/store_counter.csv')

target_df = pd.merge(bc_df, sc_df, left_on=['TS', 'Store code'], right_on=['ts_name', 'store_code'], how='left')
target_df = target_df[['BC Code', 'TS', 'ts_code']].fillna('null')

series = target_df.apply(lambda row: f'update table ppl_cms_bc where bc_code = \'{row["BC Code"]}\' set ts_user_code = \'{row["ts_code"]}\', ts_user_name = \'{row["TS"]}\';', axis=1)
series = series.drop_duplicates()
series.to_csv('./target_script/update_ts_name_sql.csv', index=False)