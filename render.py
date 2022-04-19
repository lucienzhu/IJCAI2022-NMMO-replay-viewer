import json
import pickle

import lz4
import nmmo
from ijcai2022nmmo import CompetitionConfig, TeamBasedEnv, scripted


class Config(CompetitionConfig):
    RENDER = True
    SAVE_REPLAY = "demo"


def rollout():
    config = Config()
    env = TeamBasedEnv(config=Config())
    scripted_ai = [
        scripted.CombatTeam(None, config),
        scripted.ForageTeam(None, config),
        scripted.MeanderTeam(None, config)
    ]
    obs = env.reset()
    t, horizon = 0, 1024
    while True:
        env.render()
        decision = {}
        for team_id, o in obs.items():
            decision[team_id] = scripted_ai[team_id % len(scripted_ai)].act(o)
        obs, rew, done, info = env.step(decision)
        t += 1
        if t >= horizon:
            break
    env.terminal()


def render_replay():
    replay = nmmo.Replay.load(Config.SAVE_REPLAY + ".replay")
    replay.render()


def replay_to_json():
    path = Config.SAVE_REPLAY + ".replay"
    with open(path, 'rb') as fp:
        data = fp.read()
    data = pickle.loads(lz4.block.decompress(data))
    assert isinstance(data, dict)
    with open(Config.SAVE_REPLAY + ".json", "w") as fp:
        json.dump(data, fp)

if __name__ == "__main__":
    replay_to_json()
    render_replay()
