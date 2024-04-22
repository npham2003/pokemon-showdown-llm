f= open("./battle_log/pokellmon_vs_invited_player/literally an ai - battle-gen8ou-45.html", "r")

player="p1"
turn_count=0
with f as openfileobject:
    for line in openfileobject:
        print(line.split('|'))
        if line[1]=="player":
            if line[3]=="literally an ai":
                player = line[2]
        if line[1]=="turn":
            turn_count+=1;

        