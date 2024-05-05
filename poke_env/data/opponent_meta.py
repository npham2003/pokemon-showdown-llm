import pickle
import os
import glob
class OpponentMeta:
    def __init__(self, data_path):
        self.data_path = data_path
    def get_opponent_meta(self, username:str) -> dict[str, str]:
        meta = {}
        opponent_pokemon = {}
        for filename in glob.glob(os.path.join(self.data_path, '*.pkl')):
            with open(filename,'rb') as f:
                battle = pickle.load(f)
                battle_history = battle.battle_msg_history
                if battle.opponent_username == username:
                    meta["num_battles"] = meta.get("num_battles", 0) + 1
                    meta["win_count"] = meta.get("win_count", 0) + 1 if battle.won else meta.get("win_count", 0)
                    for key in battle.opponent_team:
                        opponent_pokemon[key[key.find(':') + 1:]] = opponent_pokemon.get(key[key.find(':') + 1:], 0) + 1
                """ Adds battle log to meta
                    if battle.opponent_role == "p1":
                        dic = {"p1a":"Opponent", "Player1": "Opponent", "p2a": "Player", "Player2": "Player"}
                        battle_history = self._replace_all(battle_history, dic)
                    else:
                        battle_history = self._replace_all(battle_history,
                                                           {"p1a": "Player", "Player1": "Player", "p2a": "Opponent",
                                                            "Player2": "Opponent"})
                meta[battle.battle_tag] = battle_history
                """
        meta["opponent_pokemon"] = opponent_pokemon
        return meta

    @staticmethod
    def _replace_all(text, dict) :
        for i, j in dict.items():
            text = text.replace(i, j)
        return text