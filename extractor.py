

import re

f= open("./battle_log/pokellmon_vs_invited_player/literally an ai - battle-gen8ou-45.html", "r")
player="p1"
turn_count=0
attack_count=0
switch_count=-1
with f as openfileobject:
    for line in openfileobject:
        if bool(re.search('literally an ai', line)) and bool(re.search('player', line)):
            if bool(re.search('p1', line)):
                player="p1"
            elif bool(re.search('p2', line)):
                player="p2"
        if bool(re.search('\|turn\|', line)):
            turn_count+=1
        if bool(re.search(player,line)):
            if bool(re.search("\|move\|"+player, line)):
                print(line)
                attack_count+=1
            elif bool(re.search("\|switch\|", line)):
                switch_count+=1

print("Turns: "+ str(turn_count))
print("Did a move "+str(attack_count)+" times")
print(str(attack_count/turn_count))
print("Switched "+str(switch_count)+" times")
print(str(switch_count/turn_count))