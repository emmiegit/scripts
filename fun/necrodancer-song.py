#!/usr/bin/env python3

"""
Helps finding song numbers for Crypt of the NecroDancer songs.
"""

import re
import sys
from dataclasses import dataclass
from typing import Optional, Union

LOCATION_REGEX = re.compile(r"([0-9]+)-([0-9]+)")

@dataclass
class Location:
    zone: int
    floor: int
    variant: Optional[str] = None

    def __str__(self):
        display = f"{self.zone}-{self.floor}"

        if self.variant is not None:
            display += f" {self.variant}"

        return display

@dataclass
class Song:
    number: int
    name: str
    location: Union[str, Location]
    shopkeeper: bool = False  # Song has shopkeeper singing
    feat: Optional[str] = None  # "Featuring"

    def __str__(self):
        extra = f" with Shopkeeper" if self.shopkeeper else ""
        display = f"{self.number:02}. {self.name} ({self.location}{extra})"

        if self.feat is not None:
           display += f", feat. {self.feat}"

        return display

SONGS = [
    Song(0, "Dead End", "Credits"),  # Can't prefix with zero because octal
    Song(1, "Tombtorial", "Tutorial"),
    Song(2, "Rhythmortis", "Lobby"),
    Song(3, "Watch Your Step", "Training"),
    Song(4, "Disco Descent", Location(1, 1)),
    Song(5, "Crypteque", Location(1, 2)),
    Song(6, "Mausoleum Mash", Location(1, 3)),
    Song(7, "Konga Conga Kappa", "King Conga"),
    Song(8, "Fungal Funk", Location(2, 1)),
    Song(9, "Grave Throbbing", Location(2, 2)),
    Song(10, "Portabellohead", Location(2, 3)),
    Song(11, "Metalmancy", "Death Metal", feat="FamilyJules7x"),
    Song(12, "Stone Cold", Location(3, 1, "Cold")),
    Song(13, "Igneous Rock", Location(3, 1, "Hot"), feat="FamilyJules7x"),
    Song(14, "Dance of the Decorous", Location(3, 2, "Cold")),
    Song(15, "March of the Profane", Location(3, 2, "Hot"), feat="FamilyJules7x"),
    Song(16, "A Cold Sweat", Location(3, 3, "Cold")),
    Song(17, "A Hot Mess", Location(3, 3, "Hot"), feat="FamilyJules7x"),
    Song(18, "Knight to C, Sharp", "Deep Blues"),
    Song(19, "Styx and Stones", Location(4, 1)),
    Song(20, "Heart of the Crypt", Location(4, 2)),
    Song(21, "The Wight to Remain", Location(4, 3)),
    Song(22, "Deep Sea Bass", "Coral Riff"),
    Song(23, "For Whom the Knell Tolls", "Dead Ringer"),
    Song(24, "Momentum Mori", "Necrodancer Fight 1st Phase"),
    Song(25, "Last Dance", "Necrodancer Fight 2nd Phase"),
    Song(26, "Absolutetion", "Golden Lute Fight", feat="FamilyJules7x"),
    Song(27, "Rhythmortis", "Lobby Filtered"),
    Song(28, "Disco Descent", Location(1, 1), shopkeeper=True),
    Song(29, "Crypteque", Location(1, 2), shopkeeper=True),
    Song(30, "Mausoleum Mash", Location(1, 3), shopkeeper=True),
    Song(31, "Fungal Funk", Location(2, 1), shopkeeper=True),
    Song(32, "Grave Throbbing", Location(2, 2), shopkeeper=True),
    Song(33, "Portabellohead", Location(2, 3), shopkeeper=True),
    Song(34, "Stone Cold", Location(3, 1, "Cold"), shopkeeper=True),
    Song(35, "Igneous Rock", Location(3, 1, "Hot"), shopkeeper=True),
    Song(36, "Dance of the Decorous", Location(3, 2, "Cold"), shopkeeper=True),
    Song(37, "March of the Profane", Location(3, 2, "Hot"), shopkeeper=True, feat="FamilyJules7x"),
    Song(38, "A Cold Sweat", Location(3, 3, "Cold"), shopkeeper=True),
    Song(39, "A Hot Mess", Location(3, 3, "Hot"), shopkeeper=True, feat="FamilyJules7x"),
    Song(40, "Styx and Stones", Location(4, 1), shopkeeper=True),
    Song(41, "Heart of the Crypt", Location(4, 2), shopkeeper=True),
    Song(42, "The Wight to Remain", Location(4, 3), shopkeeper=True),
    Song(43, "Voltzwaltz", Location(5, 1)),
    Song(43, "Voltzwaltz", Location(5, 1), shopkeeper=True),
    Song(44, "Power Cords", Location(5, 2)),
    Song(44, "Power Cords", Location(5, 2), shopkeeper=True),
    Song(45, "Six Feet Thunder", Location(5, 3)),
    Song(45, "Six Feet Thunder", Location(5, 3), shopkeeper=True),
    Song(46, "Notorious D.I.G.", "Fortissimole"),
    Song(47, "Steinway to Heaven", "Frankensteinway"),
    Song(48, "Vamplified", "Conductor"),
]

if __name__ == "__main__":
    results = SONGS

    for term in sys.argv[1:]:
        # Special handling:
        # * If it begins with "-", then negate the condition
        # * If it's only an integer, then search for this index directly
        # * If it's a pair of integers, then search for that location

        if term.startswith("-"):
            term = term[1:]
            flip = lambda x: not x
        else:
            flip = lambda x: x

        match = LOCATION_REGEX.fullmatch(term)
        if match is not None:
            zone = int(match[1])
            floor = int(match[2])

            def zone_floor_filter(song):
                if not isinstance(song.location, Location):
                    return False

                return song.location.zone == zone and song.location.floor == floor

            term_filter = zone_floor_filter
        elif term.isdecimal():
            number = int(term)
            term_filter = lambda song: song.number == number
        else:
            term = term.casefold()
            term_filter = lambda song: term in str(song).casefold()

        results = [song for song in results if flip(term_filter(song))]

    # Finished filtering, print results
    if results:
        for song in results:
            print(song)
    else:
        print("No results")
