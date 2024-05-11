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
from poke_env.data import opponent_meta

parser = argparse.ArgumentParser()
parser.add_argument("--backend", type=str, default="gpt-4-turbo", choices=["gpt-3.5-turbo-0125", "gpt-4-1106-preview", "gpt-4-0125-preview"])
parser.add_argument("--temperature", type=float, default=0.8)
parser.add_argument("--prompt_algo", default="io", choices=["io", "sc", "cot", "tot"])
parser.add_argument("--log_dir", type=str, default="./battle_log/pokellmon_vs_bot/with_context_gpt_4_turbo_5_9/")
args = parser.parse_args()


async def main():
    
    team1= """Urshifu-Rapid-Strike @ Choice Band  
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
- Leaf Blade"""



    team2="""Rillaboom @ Leftovers  
Ability: Grassy Surge  
EVs: 236 HP / 252 Atk / 20 Spe  
Adamant Nature  
- Swords Dance  
- Grassy Glide  
- Knock Off  
- Drain Punch  

Tornadus-Therian (M) @ Heavy-Duty Boots  
Ability: Regenerator  
EVs: 252 HP / 52 Def / 40 SpD / 164 Spe  
Timid Nature  
- Heat Wave  
- Knock Off  
- U-turn  
- Defog  

Blaziken @ Leftovers  
Ability: Speed Boost  
EVs: 144 HP / 252 Atk / 112 Spe  
Adamant Nature  
- Swords Dance  
- Close Combat  
- Flare Blitz  
- Protect  

Melmetal @ Leftovers  
Ability: Iron Fist  
EVs: 20 HP / 232 Atk / 224 SpD / 32 Spe  
- Double Iron Bash  
- Superpower  
- Thunder Punch  
- Protect  

Garchomp @ Leftovers  
Ability: Rough Skin  
EVs: 240 HP / 252 SpD / 16 Spe  
Careful Nature  
- Stealth Rock  
- Earthquake  
- Toxic  
- Protect  

Slowbro @ Rocky Helmet  
Ability: Regenerator  
EVs: 252 HP / 252 Def / 4 SpD  
Relaxed Nature  
IVs: 0 Atk / 0 Spe  
- Scald  
- Future Sight  
- Toxic  
- Teleport"""



    heuristic_player = SimpleHeuristicsPlayer(battle_format="gen8ou",team=team1)
    opponentMeta = opponent_meta.OpponentMeta(args.log_dir).get_opponent_meta('SimpleHeuristics 1')
    os.makedirs(args.log_dir, exist_ok=True)

    llm_player = LLMPlayer(battle_format="gen8ou",
                           api_key="sk-proj-p8puiPFqfjumNr8A6STpT3BlbkFJaaJAIeLGq9zqIGxxOst7",
                           backend=args.backend,
                           temperature=args.temperature,
                           prompt_algo=args.prompt_algo,
                           log_dir=args.log_dir,
                           account_configuration=AccountConfiguration("divyansh7877", "123456789"),
                           save_replays=args.log_dir,
                           team=output_team(opponent_meta=opponentMeta,context=True)
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
