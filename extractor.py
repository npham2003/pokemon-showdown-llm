import re
import os
import pandas as pd

PLAYER_NAME = 'divyansh7877'

def metric_calculator(f,filename):
    '''
    Need to something to validate the log.
    Need to add heals for HP.
    
    '''
    player="p1"
    turn_count=0
    attack_count=0
    switch_count=-1
    pokemon_cnt = 6
    damage_cnt = 0
    pokemons={}

    for line in f:
        if bool(re.search(PLAYER_NAME, line)) and bool(re.search('player', line)):
            if bool(re.search('p1', line)):
                player="p1"
            elif bool(re.search('p2', line)):
                player="p2"
        if re.search('\|poke\|',line) and re.search(player,line):  # Get pokemon names
            name_raw = line[9:]
            name_raw = name_raw.replace('|','').strip()
            name = name_raw.split(',')[0].strip()
            base = name.split('-')[0].strip() # Unsure
            pokemons[name]={'base_form':base,
                            'HP':1}

        if bool(re.search('\|turn\|', line)):
            turn_count+=1
        if bool(re.search(player,line)):
            if bool(re.search("\|move\|"+player, line)):
                attack_count+=1
            elif bool(re.search("\|switch\|", line)):
                switch_count+=1
         

        if re.search('\|-heal\|',line) and re.search(player,line): #Player gets heal
            if re.search('[\d]{1,3}\/[\d]{1,3}',line):   
                text=re.findall('[\d]{1,3}\/[\d]{1,3}',line)[0]
                num,dem = text.split('/')
                perc=int(num)/int(dem)
                for pokemon_name,tdic in pokemons.items():
                    base = tdic['base_form']
                    if re.search(pokemon_name,line) or re.search(base,line):
                        pokemons[pokemon_name]= {'base_form':base,
                                                'HP':perc}
        
        if re.search('\|-damage\|',line) and re.search(player,line):   # Player takes damage
            if re.search('0 fnt',line):  # Pokemon is dead
                pokemon_cnt -= 1
                for pokemon_name,tdic in pokemons.items():
                    base = tdic['base_form']
                    if re.search(pokemon_name,line) or re.search(base,line):
                        pokemons[pokemon_name]= {'base_form':base,
                                                'HP': 0}
            if re.search('[\d]{1,3}\/[\d]{1,3}',line):
                
                damage_cnt +=1
                text=re.findall('[\d]{1,3}\/[\d]{1,3}',line)[0]
                num,dem = text.split('/')
                perc=int(num)/int(dem)
                for pokemon_name,tdic in pokemons.items():
                    base = tdic['base_form']
                    if re.search(pokemon_name,line) or re.search(base,line):
                        pokemons[pokemon_name]= {'base_form':base,
                                                'HP':perc}
                        
        if re.search('\|faint\|',line) and re.search(player,line):   # Player faints, aka dead
            for pokemon_name,tdic in pokemons.items():
                    base = tdic['base_form']
                    if re.search(pokemon_name,line) or re.search(base,line):
                        pokemons[pokemon_name]= {'base_form':base,
                                                'HP':0}
    if len(pokemons) == 0:
        avg_hp = 0
    else:
        avg_hp = sum([tdic['HP'] for tdic in pokemons.values()])/len(pokemons)

    
    return [turn_count,attack_count,switch_count,avg_hp*100,pokemons,filename]


df = pd.DataFrame(columns = ['Turn Count','Attack Count','Switch Count','Average HP','Pokemons','File'])


# You can to check specific logs, you can create a list of file names and place here.file

filepath = 'battle_log\pokellmon_vs_invited_player'

for file in os.listdir(filepath):

    if file.endswith(".html") and re.search(PLAYER_NAME,file):
        filename=os.path.join(filepath, file)
        print(filename)
        f =open(filename)
        metric = metric_calculator(f,filename)
        df.loc[len(df.index)] = metric
        f.close()

# You may also change the csv name for particular test
df.to_csv('battle_metrics_opponent_and_meta_context_div.csv',index=None)

lost= 0
avg_hp = 0
for index, row in df.iterrows():
    if row['Average HP'] != 0:
        avg_hp += row['Average HP']
    else:
        lost+=1

print(lost)
win_rate = 1 - (lost /len(df))

try:
    avg_hp = avg_hp/(len(df) - lost)
except:
    avg_hp = 0

print('-------Metrics--------')
print('Battles Lost:\t\t',lost)
print('Battles Won:\t\t',len(df) - lost)
print('Total Battles:\t\t',len(df))
print('Win Rate: \t\t {:.2f}%'.format(win_rate*100))
print('Average Turn Count: \t {:.2f}'.format(df['Turn Count'].mean()))
print('Average Attack Count: \t {:.2f}'.format(df['Attack Count'].mean()))
print('Average Switch Count: \t {:.2f}'.format(df['Switch Count'].mean()))
print('Average HP: \t\t {:.2f}%'.format(avg_hp))

