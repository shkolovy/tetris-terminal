# Tetris in terminal

Classic version of tile-matching puzzle video game made in Python3 and
courses

![ScreenShot](https://raw.githubusercontent.com/shkolovy/tetris-terminal/master/screenshots/game.png)

**Controls**
- Move     - ← ↓ →
- Drop     - Space
- Rotate   - ↑
- Pause    - p
- Quit     - q
- New Game - Enter

**Points**
- **5** for each new block
- **100** for each burnt line
- best score saved in file *best_score*

**Levels**
- each 10 burnt lines speed will be increased


#### Play on mac

build it `PyInstaller tetris.py --onefile` and add *path* to the .bash_profile

`export PATH="/Users/your_name/tetris-terminal:$PATH"`

type in terminal and play :) `>tetris`