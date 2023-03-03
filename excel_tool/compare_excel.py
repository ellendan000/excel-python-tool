import pandas as pd
pd.options.display.max_rows = None
pd.options.display.max_columns = None

sample_df = pd.read_excel('./files/sample.xlsx')
cms_df = pd.read_excel('./files/20230302233836BC.xlsx')

def export_duplicated_rows(df, duplicated_key_list):
    duplicated = df[df.duplicated(keep=False,subset=duplicated_key_list )]
    duplicated.to_excel('./target/duplicated.xlsx')

def drop_duplicated_rows(df, duplicated_key_list):
    df = df[df.duplicated(keep='first', subset=duplicated_key_list)]
    print(f'Duplicated: {df.shape[0]}')
    return df.drop_duplicates(keep='first')

# 查重
export_duplicated_rows(sample_df, ['BC Code'])

# 去重
sample_df = drop_duplicated_rows(sample_df, ['BC Code'])
cms_df = drop_duplicated_rows(cms_df, ['BC Code'])

# 所有行并集：bc code
whole_indexs = list(set(set(sample_df['BC Code']).union(set(cms_df['BC Code']))))
print(f'总行数: {len(whole_indexs)}')
# 所有列并集
whole_cols = list(set(set(sample_df.columns).union(set(cms_df.columns))))
print(f'总列数: {len(whole_cols)}')

# 拉齐行和列
sample_df = pd.DataFrame(sample_df, columns=whole_cols)
sample_df.set_index('BC Code', inplace=True)
sample_df = sample_df.reindex(whole_indexs)

# 拉齐行和列
cms_df = pd.DataFrame(cms_df, columns=whole_cols)
cms_df.set_index('BC Code', inplace=True)
cms_df = cms_df.reindex(whole_indexs)

# 比较
target_df = sample_df.compare(cms_df, result_names=('sample', 'cms'))

# 差异的计数器
count_series = target_df.count()
count_row = pd.DataFrame([count_series.values.T], columns=count_series.index)

result = pd.concat([count_row, target_df])
result.to_excel('./target/compare_result.xlsx')

