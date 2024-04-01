import openai
import time

def generator(keyword: str,titles: str) -> str:
    '''
    
    '''
    tries = 0
    description = ""
    
    while tries < 5:  
        try:
            tries += 1
            response= openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": ""},
                {"role": "assistant", "content": ""},
                {"role": "user", "content": f""}
            ],
            temperature=0.3,
            max_tokens=800
            )
            description = response["choices"][0]["message"]["content"].strip()
            return description
        
        except Exception as e:
            time.sleep(2**tries)

    return description