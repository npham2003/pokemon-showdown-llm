import asyncio
from poke_env import AccountConfiguration, ShowdownServerConfiguration
from poke_env.data import opponent_meta
from poke_env.player import LLMPlayer
import pickle as pkl
from tqdm import tqdm
import argparse
import os
from prompted_team import output_team

parser = argparse.ArgumentParser()
parser.add_argument("--backend", type=str, default="gpt-4-turbo", choices=["gpt-3.5-turbo-0125", "gpt-4-1106-preview", "gpt-4-0125-preview"])
parser.add_argument("--temperature", type=float, default=0.8)
parser.add_argument("--prompt_algo", default="io", choices=["io", "sc", "cot", "tot"])
parser.add_argument("--log_dir", type=str, default="./battle_log/pokellmon_vs_invited_player")
args = parser.parse_args()

async def main():

    opponentMeta = opponent_meta.OpponentMeta(args.log_dir).get_opponent_meta('AqoursBaelz')

    os.makedirs(args.log_dir, exist_ok=True)
    # myteam = output_team(opponentMeta)
    myteam = output_team()
    llm_player = LLMPlayer(battle_format="gen8ou",
                           api_key="sk-proj-p8puiPFqfjumNr8A6STpT3BlbkFJaaJAIeLGq9zqIGxxOst7",
                           backend=args.backend,
                           temperature=args.temperature,
                           prompt_algo=args.prompt_algo,
                           log_dir=args.log_dir,
                           account_configuration=AccountConfiguration("literally an ai", "NYUTesting"),
                           save_replays=args.log_dir,
                           team=myteam
                           )

    llm_player._dynamax_disable = True # If you choose to disable Dynamax for PokeLLMon, please do not use Dynamax to ensure fairness.

    # Playing 5 games on local
    for i in tqdm(range(5)):
        try:
            await llm_player.ladder(1)
            for battle_id, battle in llm_player.battles.items():
                with open(f"{args.log_dir}/{battle.opponent_username}-{battle_id}.pkl", "wb") as f:
                    pkl.dump(battle, f)
        except:
            continue

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())


# Urshifu-Rapid-Strike @ Choice Band  
# Ability: Unseen Fist  
# EVs: 252 Atk / 4 Def / 252 Spe  
# Jolly Nature  
# - Surging Strikes  
# - Close Combat  
# - Aqua Jet  
# - U-turn  

# Heatran @ Air Balloon  
# Ability: Flash Fire  
# EVs: 252 SpA / 4 SpD / 252 Spe  
# Timid Nature  
# IVs: 0 Atk  
# - Magma Storm  
# - Taunt  
# - Earth Power  
# - Stealth Rock  

# Rotom-Wash @ Leftovers  
# Ability: Levitate  
# Shiny: Yes  
# EVs: 252 HP / 248 SpD / 8 Spe  
# Calm Nature  
# IVs: 0 Atk  
# - Volt Switch  
# - Hydro Pump  
# - Thunder Wave  
# - Pain Split  

# Landorus-Therian (M) @ Leftovers  
# Ability: Intimidate  
# EVs: 248 HP / 8 Def / 252 SpD  
# Careful Nature  
# IVs: 23 Spe  
# - Defog  
# - Earthquake  
# - U-turn  
# - Knock Off  

# Tapu Lele @ Choice Scarf  
# Ability: Psychic Surge  
# EVs: 252 SpA / 4 SpD / 252 Spe  
# Timid Nature  
# IVs: 0 Atk  
# - Psyshock  
# - Moonblast  
# - Focus Blast  
# - Future Sight  

# Kartana @ Protective Pads  
# Ability: Beast Boost  
# Shiny: Yes  
# EVs: 252 Atk / 4 SpD / 252 Spe  
# Jolly Nature  
# - Swords Dance  
# - Knock Off  
# - Sacred Sword  
# - Leaf Blade

