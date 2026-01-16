[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/TigreGotico/pyFrotz)

# Frotz-Translate

**Frotz-Translate** is a minimal Python wrapper around [Frotz](https://gitlab.com/DavidGriffith/frotz), a popular interpreter for Infocom's text adventure games. It complies with the Z-Machine Standard version 1.1, making it compatible with classic interactive fiction.

This also translate commands and description in french but adaptable to any language

**THIS IS A PROTOTYPE FOR THE MOMENT, A LOTS OF BUGS**

 <img src='./pyfrotz/gui/all/pyfrotz.png' card_color='#00ff00' width='150' height='150' style='vertical-align:bottom'/> 

Get some classic games to try [@The Obsessively Complete Infocom Catalog](https://eblong.com/infocom/). 

Source code for a lot of infocom games can be found [@historicalsource](https://github.com/historicalsource)

---

## Installation

Additionally, ensure you have [dfrotz](https://gitlab.com/DavidGriffith/frotz.git) installed on your system. It is often packaged as `frotz-dumb` in Linux distributions.

---

## Usage

PyFrotz can be used programmatically or interactively in the command line interface (CLI).

### Programmatic Usage

```python
from pyfrotz import Frotz

# Load your game file
data = '/path/to/your/game/data.z5'
game = Frotz(data)

# Interact with the game in your code
game_intro = game.get_intro()
room, description = game.do_command("look")
game.save()  # Optionally pass filename, default='save.qzl'
game.restore()  # Optionally pass filename, default='save.qzl'
```

### CLI Gameplay

You can also play games directly in the CLI:

```python
from pyfrotz import Frotz

data = '/path/to/your/game/data.z5'

game = Frotz(data)
game.play_loop()
```

---

## OVOS Skills

PyFrotz can be used as a voice interpreter for all Infocom and other Z-Machine games.

An OpenVoiceOS template class is provided to wrap games into a skill.

### Template OVOS Class: `FrotzSkill`

The `FrotzSkill` class is a template for creating conversational game skills based on PyFrotz. It simplifies the integration of Z-Machine games with OpenVoiceOS by handling game state, input/output, and optional auto-save features.

#### Features

- **Game Initialization**: Automatically loads the game data and prepares the save file location.
- **Intro Parser**: Parses and announces the game's introductory text when starting a new game.
- **Command Handling**: Pipes user inputs to the game, processes the output, and optionally translates input/output for multilingual support.
- **Save/Load Management**: Handles game saving and restoring with customizable dialogs.
- **GUI Integration**: Updates the OVOS GUI with game-specific visuals during gameplay.
- **Abandon Game Handling**: Manages mid-interaction abandonment with optional auto-save.

#### Example Usage

Below is an example of how to use the `FrotzSkill` template to wrap a game like *Zork* into an OVOS skill.

```python
from pyfrotz.ovos import FrotzSkill


class ZorkSkill(FrotzSkill):
    def __init__(self, *args, **kwargs):
        super().__init__(
            game_id="zork",
            game_data="/path/to/zork.z5",
            game_lang="en",
            skill_icon="/path/to/zork/icon.png",
            game_image="/path/to/zork/bg.png",
            *args, **kwargs
        )
```

To package this into an OVOS skill:

1. Set the game-specific parameters (`game_id`, `game_data`, `game_lang`, etc.).
2. Customize dialogs and GUI assets (e.g., images and icons) as needed.
3. Override methods like `on_play_game`, `on_game_command`, or `on_abandon_game` for additional functionality.
4. Include a `{game_id}.voc` file in the `locale` directory, listing various ways the game can be referred to by voice. The file name must match the `game_id` with a `.voc` suffix (e.g., `zork.voc`).

#### Key Methods

- **`on_play_game`**: Initializes the game and displays the introductory text.
- **`on_save_game`**: Saves the current game state to a file.
- **`on_load_game`**: Restores the game state from a save file.
- **`on_stop_game`**: Handles cleanup when the game ends.
- **`on_game_command(utterance, lang)`**: Processes user commands, with optional language translation.

### Existing Game Skills

Several prebuilt OVOS skills based on PyFrotz are available:

- [Planetfall Game](https://github.com/JarbasSkills/ovos-skill-planet-fall-game)
- [Stationfall Game](https://github.com/JarbasSkills/ovos-skill-station-fall-game)
- [Starcross Game](https://github.com/JarbasSkills/ovos-skill-starcross-game)
- [The Hitchhiker's Guide to the Galaxy](https://github.com/JarbasSkills/ovos-skill-hhgg-game)
- [White House Adventure](https://github.com/OVOSHatchery/ovos-skill-white-house-adventure)
- [Zork II](https://github.com/JarbasSkills/ovos-skill-zork2-game)
- [Zork III](https://github.com/JarbasSkills/ovos-skill-zork3-game)
- [Zork 0](https://github.com/JarbasSkills/ovos-skill-zork0-game)
- [Colossal Cave Adventure](https://github.com/OVOSHatchery/ovos-skill-cave-adventure-game)

---

Enjoy bringing these timeless text-based adventures to life with PyFrotz!

