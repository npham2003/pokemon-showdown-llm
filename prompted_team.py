import json
import requests

def load_metadata(file_path):
    data = []
    with open(file_path, 'r') as file:
        # Reading each line assuming each line is a complete JSON object
        for line in file:
            if line.strip():  # This will skip any empty lines
                data.append(json.loads(line.strip()))
    return data

def create_prompt(data):
    prompt = "You are a pokemon showdown player. your task is to generate a team of 6 pokemon in the following packed format: \'Species name and form||Held Item|Ability|Move 1,Move 2,Move 3,Move 4|Nature|HP EVs,Atk EVs,Def EVs,SpAtk EVs,SpDef EVs,Speed EVs||HP IVs,Atk IVs,Def IVs,SpAtk IVs,SpDef IVs,Speed IVs|||]\' following these rules: EVs must add up to 508 total IVs can be 0 to 31, leave blank if all are 31. Special Attackers prefer 31 in all stats and 0 Attack IVs. Place ']' in between each Pokemon of the first 5. When you are at the last 6th pokemon, there must not be a ']' character after, instead just end with the normal \'|||\'. All pokemon must be on the same line. All pokemon must be on the same line. The team MUST be valid for Gen 8 OU. You must generate a team based on the attached meta data in the 'meta.txt' file and ensure that it is the statistically most likely to win. Your output needs to be in the format: Species name and form||Held Item|Ability|Move 1,Move 2,Move 3,Move 4|Nature|HP EVs,Atk EVs,Def EVs,SpAtk EVs,SpDef EVs,Speed EVs||HP IVs,Atk IVs,Def IVs,SpAtk IVs,SpDef IVs,Speed IVs|||]. YOU MUST NOT DARE INCLUDE ANY ADDITIONAL TEXT! ONLY OUTPUT THE TEAM! MAKE SURE YOUR TEXT IS NOT SURROUNDED IN QUOTATIONS AND THAT THE FINAL POKEMON ENDS WITH ||| without a ]. MAKE SURE ALL 6 POKEMON ARE OUTPUT ON THE SAME LINE (no line breaks).The pokemon and team needs to be Gen8ou vaild. The pokemons need to have valid happiness value."


    with open('meta.txt', 'r') as file:
        file_content = file.read()
    prompt+=file_content
    return prompt

def create_prompt_wo_context():
    prompt = "You are a pokemon showdown player. your task is to generate a team of 6 pokemon in the following packed format: \'Species name and form||Held Item|Ability|Move 1,Move 2,Move 3,Move 4|Nature|HP EVs,Atk EVs,Def EVs,SpAtk EVs,SpDef EVs,Speed EVs||HP IVs,Atk IVs,Def IVs,SpAtk IVs,SpDef IVs,Speed IVs|||]\' following these rules: EVs must add up to 508 total IVs can be 0 to 31, leave blank if all are 31. Special Attackers prefer 31 in all stats and 0 Attack IVs. Place ']' in between each Pokemon of the first 5. When you are at the last 6th pokemon, there must not be a ']' character after, instead just end with the normal \'|||\'. All pokemon must be on the same line. All pokemon must be on the same line. You must generate a team based to ensure that it is the statistically most likely to win. Your output needs to be in the format: Species name and form||Held Item|Ability|Move 1,Move 2,Move 3,Move 4|Nature|HP EVs,Atk EVs,Def EVs,SpAtk EVs,SpDef EVs,Speed EVs||HP IVs,Atk IVs,Def IVs,SpAtk IVs,SpDef IVs,Speed IVs|||]. YOU MUST NOT DARE INCLUDE ANY ADDITIONAL TEXT! ONLY OUTPUT THE TEAM! MAKE SURE YOUR TEXT IS NOT SURROUNDED IN QUOTATIONS AND THAT THE FINAL POKEMON ENDS WITH ||| without a ]. MAKE SURE ALL 6 POKEMON ARE OUTPUT ON THE SAME LINE (no line breaks).The team needs to be in Gen8ou vaild. The pokemons need to have valid happiness value."
    return prompt

def create_prompt_opponent(meta,data):
    prompt = "You are a pokemon showdown player. your task is to generate a team of 6 pokemon in the following packed format: 'Species name and form||Held Item|Ability|Move 1,Move 2,Move 3,Move 4|Nature|HP EVs,Atk EVs,Def EVs,SpAtk EVs,SpDef EVs,Speed EVs||HP IVs,Atk IVs,Def IVs,SpAtk IVs,SpDef IVs,Speed IVs|||]' following these rules: EVs must add up to 508 total IVs can be 0 to 31, leave blank if all are 31. Special Attackers prefer 31 in all stats and 0 Attack IVs. Place ']' in between each Pokemon of the first 5. When you are at the last 6th pokemon, there must not be a ']' character after, instead just end with the normal '|||'. All pokemon must be on the same line. You must generate a team that is statistically most likely to win by countering your opponents playing style inferred from the data below:\n"
    prompt += f"You have played this opponent {meta['num_battles']} times, out of which you have won {meta['win_count']}, your opponent has used the following pokemons:\n"
    for key, value in meta["opponent_pokemon"].items():
        prompt += f"- {key} (times used: {value})\n"
    prompt += "you must make sure you are also designing the most statistically likely to win pokemon team to counter your opponents playing style, taking your insights from the battle logs, and the attached 'meta:'\n"

    with open('meta.txt', 'r') as file:
        i=0
        while i<20:
            file_content = file.readline()
            prompt+=file_content
            i+=1
    
    prompt += "Your output needs to be in the format: Species name and form||Held Item|Ability|Move 1,Move 2,Move 3,Move 4|Nature|HP EVs,Atk EVs,Def EVs,SpAtk EVs,SpDef EVs,Speed EVs||HP IVs,Atk IVs,Def IVs,SpAtk IVs,SpDef IVs,Speed IVs|||]. YOU MUST NOT DARE INCLUDE ANY ADDITIONAL TEXT! ONLY OUTPUT THE TEAM! MAKE SURE YOUR TEXT IS NOT SURROUNDED IN QUOTATIONS AND THAT THE FINAL POKEMON ENDS WITH ||| without a ]. MAKE SURE ALL 6 POKEMON ARE OUTPUT ON THE SAME LINE (no line breaks). The team MUST be valid for Gen 8 OU."
    return prompt
def call_chatgpt_api(prompt, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    messages = [{
        "role": "user",
        "content": prompt
    }]
    data = {
        "model": "gpt-4-turbo", # Please use only gpt 4 turbo
        "messages": messages
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    return response.json()

def output_team(opponent_meta = None , context=None):
    prompt = None
    file_path = 'meta.txt'  # Path to your meta.txt file
    metadata = load_metadata(file_path)


    if context and not opponent_meta:
        print('USING METADATA')
        prompt = create_prompt(metadata)
    elif not context and not opponent_meta:
        print('USING NO METADATA')
        prompt = create_prompt_wo_context()
    elif context and opponent_meta:
        print('USING OPPONENT META')
        prompt = create_prompt_opponent(opponent_meta,metadata)
        
    # print(prompt)

    api_key = 'sk-proj-p8puiPFqfjumNr8A6STpT3BlbkFJaaJAIeLGq9zqIGxxOst7'  # Your OpenAI API key
    response = call_chatgpt_api(prompt, api_key)

    print("API Response:")
    print(response['choices'][0]['message']['content'])
    return response['choices'][0]['message']['content']