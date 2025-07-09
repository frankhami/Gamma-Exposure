import pandas as pd

df = pd.read_csv("order_books.csv")

df[['asset', 'expiration', 'strike', 'type']] = df['instrument_name'].str.split('-', expand=True)

df['strike'] = pd.to_numeric(df['strike'])
df['gamma'] = pd.to_numeric(df['gamma'])
df['open_interest'] = pd.to_numeric(df['open_interest'])

grouped = df.groupby('expiration')

for exp, group in grouped:
    calls = group[group['type'] == 'C']
    puts = group[group['type'] == 'P']
    

gex_results = []

for expiration in df['expiration'].unique():
    exp_group = df[df['expiration'] == expiration]

    calls = exp_group[exp_group['type'] == 'C']
    calls['gex_level'] = calls['gamma'] * calls['open_interest'] * 1

    puts = exp_group[exp_group['type'] == 'P']
    puts['gex_level'] = puts['gamma'] * puts['open_interest'] * (-1)

    total_gex = calls['gex_level'].sum() + puts['gex_level'].sum()

    gex_call = calls.loc[calls['gex_level'].idxmax()]
    gex_put = puts.loc[puts['gex_level'].idxmin()]

    gex_call = gex_call[['instrument_name', 'open_interest', 'strike', 'type', 'gex_level']]
    gex_put = gex_put[['instrument_name', 'open_interest', 'strike', 'type', 'gex_level']]

    gex_call['total_gex'] = total_gex
    gex_put['total_gex'] = total_gex
    
    gex_results.append(gex_call)
    gex_results.append(gex_put)

gex_results_df = pd.DataFrame(gex_results)
gex_results_df.to_csv("gex_results.csv", index=False)