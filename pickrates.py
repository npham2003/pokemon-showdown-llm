import pandas as pd
import ast

#Paste the path to the csv generated.
csvpath = 'battle_metrics_wo_context_5_5_div.csv'
df = pd.read_csv(csvpath)
pickrates= {}

for inx,row in df.iterrows():
    for poke in ast.literal_eval(row['Pokemons']).keys():
        if poke in pickrates:
            pickrates[poke]+=1
        else:
            pickrates[poke]=1

print('-------PICKRATES--------')
for key,value in pickrates.items():
    print(key,'\t {:.2f}%'.format(100*value/len(df)))