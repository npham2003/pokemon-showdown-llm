import asyncio
import time
from tqdm import tqdm
import numpy as np
from poke_env import AccountConfiguration, ShowdownServerConfiguration
import os
import pickle as pkl
import argparse
from prompted_team import output_team
from poke_env.player import LLMPlayer, SimpleHeuristicsPlayer

parser = argparse.ArgumentParser()
parser.add_argument("--backend", type=str, default="gpt-4-turbo", choices=["gpt-3.5-turbo-0125", "gpt-4-1106-preview", "gpt-4-0125-preview"])
parser.add_argument("--temperature", type=float, default=0.8)
parser.add_argument("--prompt_algo", default="io", choices=["io", "sc", "cot", "tot"])
parser.add_argument("--log_dir", type=str, default="./battle_log/pokellmon_vs_bot/without_context/")
args = parser.parse_args()

async def main():

    heuristic_player = SimpleHeuristicsPlayer(battle_format="gen8ou",team="""Urshifu-Rapid-Strike @ Choice Band  
Ability: Unseen Fist  
EVs: 252 Atk / 4 Def / 252 Spe  
Jolly Nature  
- Surging Strikes  
- Close Combat  
- Aqua Jet  
- U-turn  

Heatran @ Air Balloon  
Ability: Flash Fire  
EVs: 252 SpA / 4 SpD / 252 Spe  
Timid Nature  
IVs: 0 Atk  
- Magma Storm  
- Taunt  
- Earth Power  
- Stealth Rock  

Rotom-Wash @ Leftovers  
Ability: Levitate  
Shiny: Yes  
EVs: 252 HP / 248 SpD / 8 Spe  
Calm Nature  
IVs: 0 Atk  
- Volt Switch  
- Hydro Pump  
- Thunder Wave  
- Pain Split  

Landorus-Therian (M) @ Leftovers  
Ability: Intimidate  
EVs: 248 HP / 8 Def / 252 SpD  
Careful Nature  
IVs: 23 Spe  
- Defog  
- Earthquake  
- U-turn  
- Knock Off  

Tapu Lele @ Choice Scarf  
Ability: Psychic Surge  
EVs: 252 SpA / 4 SpD / 252 Spe  
Timid Nature  
IVs: 0 Atk  
- Psyshock  
- Moonblast  
- Focus Blast  
- Future Sight  

Kartana @ Protective Pads  
Ability: Beast Boost  
Shiny: Yes  
EVs: 252 Atk / 4 SpD / 252 Spe  
Jolly Nature  
- Swords Dance  
- Knock Off  
- Sacred Sword  
- Leaf Blade""")

    os.makedirs(args.log_dir, exist_ok=True)
    llm_player = LLMPlayer(battle_format="gen8ou",
                           api_key="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",
                           backend=args.backend,
                           temperature=args.temperature,
                           prompt_algo=args.prompt_algo,
                           log_dir=args.log_dir,
                           account_configuration=AccountConfiguration("divyansh7877", "123456789"),
                           save_replays=args.log_dir,
                           team=output_team(opponent_meta=False,context=False)
                           )

    # dynamax is disabled for local battles.
    heuristic_player._dynamax_disable = True
    llm_player._dynamax_disable = True

    # play against bot for five battles
    for i in tqdm(range(5)):
        x = np.random.randint(0, 100)
        if x > 50:
            await heuristic_player.battle_against(llm_player, n_battles=1)
        else:
            await llm_player.battle_against(heuristic_player, n_battles=1)
        for battle_id, battle in llm_player.battles.items():
            with open(f"{args.log_dir}/{battle_id}.pkl", "wb") as f:
                pkl.dump(battle, f)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
