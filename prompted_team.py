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
    prompt = "You are a pokemon showdown player. your task is to generate a team of 6 pokemon in the following packed format: \'Species name and form||Held Item|Ability|Move 1,Move 2,Move 3,Move 4|Nature|HP EVs,Atk EVs,Def EVs,SpAtk EVs,SpDef EVs,Speed EVs||HP IVs,Atk IVs,Def IVs,SpAtk IVs,SpDef IVs,Speed IVs|||]\' following these rules: EVs must add up to 508 total IVs can be 0 to 31, leave blank if all are 31. Special Attackers prefer 31 in all stats and 0 Attack IVs. Place ']' in between each Pokemon of the first 5. When you are at the last 6th pokemon, there must not be a ']' character after, instead just end with the normal \'|||\'. All pokemon must be on the same line. All pokemon must be on the same line. You must generate a team based on the attached meta data in the 'meta.txt' file and ensure that it is the statistically most likely to win. Your output needs to be in the format: Species name and form||Held Item|Ability|Move 1,Move 2,Move 3,Move 4|Nature|HP EVs,Atk EVs,Def EVs,SpAtk EVs,SpDef EVs,Speed EVs||HP IVs,Atk IVs,Def IVs,SpAtk IVs,SpDef IVs,Speed IVs|||]. YOU MUST NOT DARE INCLUDE ANY ADDITIONAL TEXT! ONLY OUTPUT THE TEAM! MAKE SURE YOUR TEXT IS NOT SURROUNDED IN QUOTATIONS AND THAT THE FINAL POKEMON ENDS WITH ||| without a ]. MAKE SURE ALL 6 POKEMON ARE OUTPUT ON THE SAME LINE (no line breaks)"

    for pokemon in data:
        prompt += f"- {pokemon['name']} (Type: {', '.join(pokemon['type'])}, Usage Rate: {pokemon['usage_rate']}%)\n"
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
        "model": "gpt-4",
        "messages": messages
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    return response.json()

def output_team():
    file_path = 'meta.txt'  # Path to your meta.txt file
    api_key = 'sk-proj-p8puiPFqfjumNr8A6STpT3BlbkFJaaJAIeLGq9zqIGxxOst7'  # Your OpenAI API key

    metadata = load_metadata(file_path)
    prompt = create_prompt(metadata)
    response = call_chatgpt_api(prompt, api_key)

    print("API Response:")
    print(response['choices'][0]['message']['content'])
    return response['choices'][0]['message']['content']