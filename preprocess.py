import pandas as pd

df = pd.read_csv('data/bigvul.csv')
df = df[['func_before', 'target']].dropna()
df = df.rename(columns={'func_before': 'code', 'target': 'label'})
df = df[df['code'].str.len() < 1500]

vulnerable = df[df['label'] == 1]
not_vulnerable = df[df['label'] == 0]

print(f'Total vulnerable: {len(vulnerable)}')
print(f'Total not vulnerable: {len(not_vulnerable)}')

# Take 2000 of each for balanced dataset
n = min(2000, len(vulnerable))
vulnerable_sample = vulnerable.sample(n, random_state=42)
not_vulnerable_sample = not_vulnerable.sample(n, random_state=42)

df_balanced = pd.concat([vulnerable_sample, not_vulnerable_sample]).sample(frac=1, random_state=42)
df_balanced.to_csv('data/clean.csv', index=False)

print(f'Balanced dataset: {df_balanced["label"].value_counts().to_dict()}')
print(f'Total samples: {len(df_balanced)}')
print('Saved data/clean.csv')
