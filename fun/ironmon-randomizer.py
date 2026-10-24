#!/usr/bin/env python

import argparse
import subprocess
from pathlib import Path
from typing import Final

# Randomizer settings from https://gist.github.com/UTDZac/a147c497424dfbd537d8c4b0c22b5621
# Converted to *.rnqs files by the GUI

IRONMON_DIRECTORY: Final[Path] = Path("/media/media/games/emulator/DS/Ironmon")
RANDOMIZER_DIRECTORY: Final[Path] = IRONMON_DIRECTORY / "PokeRandoZX"

def get_rom_file_stem(game: str) -> tuple[str, str]:
    match game:
        case "heartgold":
            return "Ironmon_HeartGold_Original", "Ironmon_HeartGold"
        case "platinum":
            return "Ironmon_Platinum_Original", "Ironmon_Platinum"
        case _:
            raise ValueError(f"Invalid game type: '{game}'")


def get_rom_paths(game: str) -> tuple[Path, Path]:
    input_stem, output_stem = get_rom_file_stem(game)

    input_rom_path = IRONMON_DIRECTORY / f"{input_stem}.nds"
    output_rom_path = IRONMON_DIRECTORY / f"{output_stem}.nds"
    return input_rom_path, output_rom_path


def get_rnqs_path(game: str, variant: str) -> Path:
    path = RANDOMIZER_DIRECTORY / f"{game}_{variant}.rnqs"
    if not path.exists():
        raise ValueError(f"No rnqs file: {path}")
    return path


def main() -> None:
    argparser = argparse.ArgumentParser("ironmon-randomizer")
    argparser.add_argument(
        "game",
        choices=["heartgold", "platinum"],
        help="The Pokémon game to randomize",
    )
    argparser.add_argument(
        "variant",
        choices=["standard", "ultimate", "kaizo", "doubles"],
        help="The Ironmon variant to play",
    )
    args = argparser.parse_args()

    input_rom_path, output_rom_path = get_rom_paths(game)
    rnqs_path = get_rnqs_path(game, variant)

    # TODO


if __name__ == "__main__":
    main()
