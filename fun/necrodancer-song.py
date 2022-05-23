#!/usr/bin/env python3

"""
Helps finding song numbers for Crypt of the NecroDancer songs.
"""

import sys
from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class Location:
    zone: int
    floor: int
    variant: Optional[str] = None

    def __iter__(self):
        yield f"{self.zone}-{self.floor}"

        if self.variant is not None:
            yield self.variant

@dataclass
class Song:
    number: int
    name: str
    location: Union[str, Location]
    shopkeeper: bool = False  # Song has shopkeeper singing
    feat: Optional[str] = None  # "Featuring"

    def __iter__(self):
        yield self.number
        yield self.name

        if isinstance(self.location, Location):
            yield from self.location
        else:
            yield self.location

        if self.shopkeeper:
            yield "Shopkeeper"

        if self.variant is not None:
            yield self.variant


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
    pass
