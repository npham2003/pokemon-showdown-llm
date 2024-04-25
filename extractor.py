import re

f= open("./battle_log/pokellmon_vs_invited_player/literally an ai - battle-gen8ou-43.html", "r")
player="p1"
turn_count=0
attack_count=0
switch_count=-1
pokemon_cnt = 6
avg_hlth = 100
damage_cnt = 0
pokemons={}


for line in f:
    if bool(re.search('literally an ai', line)) and bool(re.search('player', line)):
        if bool(re.search('p1', line)):
            player="p1"
        elif bool(re.search('p2', line)):
            player="p2"

    if re.search('\|poke\|',line) and re.search(player,line):  # Get pokemon names
        name_raw = line[9:]
        name_raw = name_raw.replace('|','').strip()
        name = name_raw.split(',')[0].strip()
        base_form = name.split('-')[0].strip() # Unsure
        pokemons[name]={
            "base": base_form,
            "health": 1
        }


    if bool(re.search('\|turn\|', line)):
        turn_count+=1
    if bool(re.search(player,line)):
        if bool(re.search("\|move\|"+player, line)):
            attack_count+=1
        elif bool(re.search("\|switch\|", line)):
            switch_count+=1
    if re.search('\|-damage\|',line) and re.search(player,line):
        if re.search('0 fnt',line):  # Pokemon is dead
            pokemon_cnt -= 1
            for pokemon_name in pokemons.keys():
                if re.search(pokemons[pokemon_name]["base"],line):
                    pokemons[pokemon_name]["health"]= 0
                    #print(pokemon_name,'Dead')
        if re.search('[\d]{1,3}\/[\d]{1,3}',line):
            
            damage_cnt +=1
            text=re.findall('[\d]{1,3}\/[\d]{1,3}',line)[0]
            num,dem = text.split('/')
            perc=int(num)/int(dem)
            for pokemon_name in pokemons.keys():
                if re.search(pokemons[pokemon_name]["base"],line):
                    pokemons[pokemon_name]["health"]= perc
                    #print(pokemon_name,perc)
            

print("Turns: "+ str(turn_count))
print("Did a move "+str(attack_count)+" times")
print(str(attack_count/turn_count))
print("Switched "+str(switch_count)+" times")
print(str(switch_count/turn_count))
print(pokemons)
sum_health=0
for pokemon_name in pokemons.keys():
    sum_health+=pokemons[pokemon_name]["health"]
average=sum_health*100/len(pokemons)
print('Average Health {:.2f}%'.format(average))
print('Number of Pokemon',pokemon_cnt)