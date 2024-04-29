import asyncio
from poke_env import AccountConfiguration, ShowdownServerConfiguration
from poke_env.player import LLMPlayer
import pickle as pkl
from tqdm import tqdm
import argparse
import os
from prompted_team import output_team

parser = argparse.ArgumentParser()
parser.add_argument("--backend", type=str, default="gpt-4-0125-preview", choices=["gpt-3.5-turbo-0125", "gpt-4-1106-preview", "gpt-4-0125-preview"])
parser.add_argument("--temperature", type=float, default=0.8)
parser.add_argument("--prompt_algo", default="io", choices=["io", "sc", "cot", "tot"])
parser.add_argument("--log_dir", type=str, default="./battle_log/pokellmon_vs_invited_player")
args = parser.parse_args()

async def main():

    os.makedirs(args.log_dir, exist_ok=True)
    myteam = output_team()
    llm_player = LLMPlayer(battle_format="gen8ou",
                           api_key="sk-proj-p8puiPFqfjumNr8A6STpT3BlbkFJaaJAIeLGq9zqIGxxOst7",
                           backend=args.backend,
                           temperature=args.temperature,
                           prompt_algo=args.prompt_algo,
                           log_dir=args.log_dir,
                           account_configuration=AccountConfiguration("oklabaraa", "osos12@1"),
                           save_replays=args.log_dir,
                           team=myteam
                           )

    llm_player._dynamax_disable = True # If you choose to disable Dynamax for PokeLLMon, please do not use Dynamax to ensure fairness.

    # Playing 5 games on local
    for i in tqdm(range(5)):
        try:
            await llm_player.ladder(1)
            for battle_id, battle in llm_player.battles.items():
                with open(f"{args.log_dir}/{battle_id}.pkl", "wb") as f:
                    pkl.dump(battle, f)
        except:
            continue

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())