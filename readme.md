# view replay in terminal

1. Support `.json` or `.replay` format
```bash
python render.py
```

2. `terminal_replay_viewer.py` A script to render replay in terminal。

Requirements
```bash
pip install sty
pip install lz4
```

Usage
```bash
# json file, view all
python terminal_replay_viewer.py demo.json --focus_id 9999
# json file, view agent 9
python terminal_replay_viewer.py demo.json --focus_id 9

# replay file, view all
python terminal_replay_viewer.py demo.replay --focus_id 9999
# replay file, view agent 9
python terminal_replay_viewer.py demo.replay --focus_id 9
# replay file, view npc -1
python terminal_replay_viewer.py demo.replay --focus_id -1
```

# obtain replays from nmmo env

1. Install requirements
```bash
conda create --name nmmo python=3.9
conda activate nmmo

git clone https://github.com/IJCAI2022-NMMO/ijcai2022nmmo.git
cd ijcai2022nmmo
make install

pip install supersuit
```
2. Check `render.py`

* `rollout()`: generate replay
* `render_replay()`: load replay and show in Unity Client
* `replay_to_json()`: convert `.replay` to `.json` format

Files：
- demo.json: replay in json
- demo.replay: replay in compressed way
- render.py: script to render replay and convert replay to json
