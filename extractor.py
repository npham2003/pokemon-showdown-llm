f= open("./battle_log/pokellmon_vs_invited_player/literally an ai - battle-gen8ou-45.html", "r")

player="p1"
turn_count=0
attack_count=0
switch_count=-1
with f as openfileobject:
    for line in openfileobject:
        line = line.split('|')
        if len(line)>1:
            if line[1]=="player":
                if line[3]=="literally an ai":
                    player = line[2]
            if line[1]=="turn":
                turn_count+=1;
            if line[1]=="move":
                if player in line[2]:
                    attack_count+=1
            if line[1]=="switch":
                if player in line[2]:
                    switch_count+=1

print("Turns: "+ str(turn_count))
print("Did a move "+str(attack_count)+" times")
print(str(attack_count/turn_count))
print("Switched "+str(switch_count)+" times")
print(str(switch_count/turn_count))