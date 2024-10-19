#!/usr/bin/env python

"""
Using genre and game type information, this script recommends the best game combinations
based on which ones are presently unlocked / you wish to use.

Data sourced from https://gamefaqs.gamespot.com/xbox-series-x/424246-game-dev-story/faqs/61158
"""

import sys
from enum import Enum, unique


@unique
class Genre(Enum):
    RPG = "RPG"
    SIMULATION = "Simulation"
    SIM_RPG = "Sim RPG"
    TABLE = "Table"
    ACTION = "Action"
    ADVENTURE = "Adventure"
    SHOOTER = "Shooter"
    ACTION_RPG = "Action RPG"
    RACING = "Racing"
    ONLINE_RPG = "Online RPG"
    ONLINE_SIM = "Online Sim"
    TRIVIA = "Trivia"
    LIFE = "Life"
    BOARD = "Board"
    PUZZLE = "Puzzle"
    MUSIC = "Music"
    AUDIO_NOVEL = "Audio Novel"
    MOTION = "Motion"
    EDUCATIONAL = "Educational"
    CARD_GAME = "Card Game"


@unique
class GameType(Enum):
    SPORTS = "Sports"
    EXPLORATION = "Exploration"
    MARTIAL_ARTS = "Martial Arts"
    FANTASY = "Fantasy"
    VIRTUAL_PET = "Virtual Pet"
    SAMURAI = "Samurai"
    DUNGEON = "Dungeon"
    ROMANCE = "Romance"
    PIRATE = "Pirate"
    COMEDY = "Comedy"
    HORROR = "Horror"
    WORD = "Word"
    TRAIN = "Train"
    ANIMAL = "Animal"
    ROBOT = "Robot"
    AIRPLANE = "Airplane"
    CONV_STORE = "Conv. Store"
    HISTORICAL = "Historical"
    BOOKSTORE = "Bookstore"
    COMICS = "Comics"
    ART = "Art"
    MOVIES = "Movies"
    GAME_CO = "Game Co."
    EGYPT = "Egypt"
    TOWN = "Town"
    ARCHITECTURE = "Architecture"
    LAWYER = "Lawyer"
    MEDIEVAL = "Medieval"
    MONSTER = "Monster"
    HUNTING = "Hunting"
    HIGH_SCHOOL = "High School"
    JUNIOR_HIGH = "Junior High"
    WAR = "War"
    NINJA = "Ninja"
    CUTIE = "Cutie"
    OGRE = "Ogre"
    FASHION = "Fashion"
    DETECTIVE = "Detective"
    MYSTERY = "Mystery"
    COWBOY = "Cowboy"
    HORSESHOES = "Horseshoes"
    PRESIDENT = "President"
    STOCKS = "Stocks"
    CARTOON = "Cartoon"
    COSPLAY = "Cosplay"
    SWIMSUIT = "Swimsuit"
    MINI_SKIRT = "Mini-skirt"
    MUSHROOM = "Mushroom"
    POP_STAR = "Pop Star"
    PONCHO = "Poncho"
    CHESS = "Chess"
    CHECKERS = "Checkers"
    MAHJONG = "Mahjong"
    REVERSI = "Reversi"
    DANCE = "Dance"
    DRUMS = "Drums"
    FITNESS = "Fitness"
    WRESTLING = "Wrestling"
    BASKETBALL = "Basketball"
    SKIING = "Skiing"
    SNOWBOARD = "Snowboard"
    GOLF = "Golf"
    SWIMMING = "Swimming"
    VOLLEYBALL = "Volleyball"
    MOTORSPORT = "Motorsport"
    SOCCER = "Soccer"
    PING_PONG = "Ping Pong"
    SUMO = "Sumo"
    BASEBALL = "Baseball"
    MARATHON = "Marathon"
    F1_RACING = "F1 Racing"
    PINBALL = "Pinball"
    SLOTS = "Slots"
    DATING = "Dating"
    HARBOR = "Harbor"
    TIME_TRAVEL = "Time Travel"
    SPY = "Spy"
    CELEBRITY = "Celebrity"


COMBINATION_TIER_NAMES = [
    "Amazing",
    "Creative",
    "Not Bad",
    "Hmm...",
    "Not Good",
]


COMBINATIONS = [
    # Amazing
    [
        (GameType.FANTASY, Genre.RPG),
        (GameType.VIRTUAL_PET, Genre.ACTION),
        (GameType.VIRTUAL_PET, Genre.ONLINE_SIM),
        (GameType.ROMANCE, Genre.SIMULATION),
        (GameType.ROMANCE, Genre.AUDIO_NOVEL),
        (GameType.COMEDY, Genre.TRIVIA),
        (GameType.HORROR, Genre.ACTION),
        (GameType.HORROR, Genre.AUDIO_NOVEL),
        (GameType.WORD, Genre.LIFE),
        (GameType.TRAIN, Genre.SIMULATION),
        (GameType.ANIMAL, Genre.LIFE),
        (GameType.ROBOT, Genre.SHOOTER),
        (GameType.CONV_STORE, Genre.ONLINE_SIM),
        (GameType.HISTORICAL, Genre.ACTION),
        (GameType.BOOKSTORE, Genre.SIMULATION),
        (GameType.COMICS, Genre.SIMULATION),
        (GameType.COMICS, Genre.LIFE),
        (GameType.MOVIES, Genre.SIMULATION),
        (GameType.MOVIES, Genre.AUDIO_NOVEL),
        (GameType.GAME_CO, Genre.SIMULATION),
        (GameType.GAME_CO, Genre.ONLINE_SIM),
        (GameType.GAME_CO, Genre.LIFE),
        (GameType.TOWN, Genre.SIMULATION),
        (GameType.TOWN, Genre.LIFE),
        (GameType.ARCHITECTURE, Genre.SIMULATION),
        (GameType.ARCHITECTURE, Genre.ONLINE_SIM),
        (GameType.MEDIEVAL, Genre.ONLINE_RPG),
        (GameType.HUNTING, Genre.ACTION_RPG),
        (GameType.NINJA, Genre.ACTION),
        (GameType.CUTIE, Genre.SIMULATION),
        (GameType.CUTIE, Genre.AUDIO_NOVEL),
        (GameType.OGRE, Genre.RPG),
        (GameType.OGRE, Genre.ACTION),
        (GameType.DETECTIVE, Genre.ADVENTURE),
        (GameType.DETECTIVE, Genre.AUDIO_NOVEL),
        (GameType.MYSTERY, Genre.SHOOTER),
        (GameType.COWBOY, Genre.ADVENTURE),
        (GameType.COWBOY, Genre.AUDIO_NOVEL),
        (GameType.HORSESHOES, Genre.SHOOTER),
        (GameType.STOCKS, Genre.ONLINE_SIM),
        (GameType.CARTOON, Genre.SIMULATION),
        (GameType.CARTOON, Genre.ADVENTURE),
        (GameType.COSPLAY, Genre.TRIVIA),
        (GameType.POP_STAR, Genre.SIMULATION),
        (GameType.POP_STAR, Genre.ONLINE_SIM),
        (GameType.POP_STAR, Genre.LIFE),
        (GameType.POP_STAR, Genre.MOTION),
        (GameType.MINI_SKIRT, Genre.TRIVIA),
        (GameType.MUSHROOM, Genre.RPG),
        (GameType.MUSHROOM, Genre.SIMULATION),
        (GameType.MUSHROOM, Genre.ONLINE_SIM),
        (GameType.MUSHROOM, Genre.LIFE),
        (GameType.PONCHO, Genre.TABLE),
        (GameType.PONCHO, Genre.ACTION_RPG),
        (GameType.CHESS, Genre.BOARD),
        (GameType.CHECKERS, Genre.PUZZLE),
        (GameType.MAHJONG, Genre.TABLE),
        (GameType.REVERSI, Genre.PUZZLE),
        (GameType.DANCE, Genre.MUSIC),
        (GameType.DANCE, Genre.MOTION),
        (GameType.DRUMS, Genre.MUSIC),
        (GameType.DRUMS, Genre.MOTION),
        (GameType.FITNESS, Genre.MOTION),
        (GameType.WRESTLING, Genre.LIFE),
        (GameType.BASKETBALL, Genre.ACTION),
        (GameType.SKIING, Genre.MOTION),
        (GameType.SNOWBOARD, Genre.RACING),
        (GameType.SNOWBOARD, Genre.MOTION),
        (GameType.SWIMMING, Genre.ONLINE_SIM),
        (GameType.VOLLEYBALL, Genre.MOTION),
        (GameType.MOTORSPORT, Genre.SIMULATION),
        (GameType.MOTORSPORT, Genre.RACING),
        (GameType.SOCCER, Genre.SIMULATION),
        (GameType.SOCCER, Genre.LIFE),
        (GameType.PING_PONG, Genre.LIFE),
        (GameType.DATING, Genre.LIFE),
        (GameType.DATING, Genre.AUDIO_NOVEL),
        (GameType.SUMO, Genre.ACTION),
        (GameType.SUMO, Genre.TRIVIA),
        (GameType.F1_RACING, Genre.SIMULATION),
        (GameType.F1_RACING, Genre.LIFE),
        (GameType.PINBALL, Genre.MOTION),
        (GameType.SLOTS, Genre.MOTION),
    ],
    # Creative
    [
        (GameType.SPORTS, Genre.SIMULATION),
        (GameType.SPORTS, Genre.PUZZLE),
        (GameType.SPORTS, Genre.MOTION),
        (GameType.EXPLORATION, Genre.ONLINE_RPG),
        (GameType.MARTIAL_ARTS, Genre.TABLE),
        (GameType.MARTIAL_ARTS, Genre.ADVENTURE),
        (GameType.MARTIAL_ARTS, Genre.SHOOTER),
        (GameType.MARTIAL_ARTS, Genre.AUDIO_NOVEL),
        (GameType.FANTASY, Genre.SHOOTER),
        (GameType.FANTASY, Genre.LIFE),
        (GameType.FANTASY, Genre.PUZZLE),
        (GameType.VIRTUAL_PET, Genre.RPG),
        (GameType.VIRTUAL_PET, Genre.SHOOTER),
        (GameType.VIRTUAL_PET, Genre.MOTION),
        (GameType.SAMURAI, Genre.RACING),
        (GameType.DUNGEON, Genre.RACING),
        (GameType.ROMANCE, Genre.TRIVIA),
        (GameType.ROMANCE, Genre.MOTION),
        (GameType.PIRATE, Genre.TRIVIA),
        (GameType.COMEDY, Genre.ACTION),
        (GameType.COMEDY, Genre.ADVENTURE),
        (GameType.COMEDY, Genre.MOTION),
        (GameType.HORROR, Genre.RPG),
        (GameType.WORD, Genre.MOTION),
        (GameType.TRAIN, Genre.RPG),
        (GameType.TRAIN, Genre.ACTION),
        (GameType.TRAIN, Genre.ADVENTURE),
        (GameType.TRAIN, Genre.RACING),
        (GameType.ANIMAL, Genre.AUDIO_NOVEL),
        (GameType.CONV_STORE, Genre.MUSIC),
        (GameType.HISTORICAL, Genre.SHOOTER),
        (GameType.BOOKSTORE, Genre.MOTION),
        (GameType.ART, Genre.RPG),
        (GameType.ART, Genre.LIFE),
        (GameType.ART, Genre.PUZZLE),
        (GameType.GAME_CO, Genre.RACING),
        (GameType.EGYPT, Genre.PUZZLE),
        (GameType.TOWN, Genre.AUDIO_NOVEL),
        (GameType.ARCHITECTURE, Genre.RPG),
        (GameType.ARCHITECTURE, Genre.MOTION),
        (GameType.LAWYER, Genre.ACTION),
        (GameType.LAWYER, Genre.SHOOTER),
        (GameType.MONSTER, Genre.RACING),
        (GameType.MONSTER, Genre.MOTION),
        (GameType.HUNTING, Genre.SHOOTER),
        (GameType.NINJA, Genre.ADVENTURE),
        (GameType.CUTIE, Genre.RACING),
        (GameType.CUTIE, Genre.MUSIC),
        (GameType.CUTIE, Genre.MOTION),
        (GameType.OGRE, Genre.RACING),
        (GameType.OGRE, Genre.MOTION),
        (GameType.FASHION, Genre.TABLE),
        (GameType.FASHION, Genre.PUZZLE),
        (GameType.DETECTIVE, Genre.ACTION),
        (GameType.DETECTIVE, Genre.MUSIC),
        (GameType.MYSTERY, Genre.MOTION),
        (GameType.COWBOY, Genre.RACING),
        (GameType.COWBOY, Genre.MUSIC),
        (GameType.HORSESHOES, Genre.ADVENTURE),
        (GameType.HORSESHOES, Genre.BOARD),
        (GameType.HORSESHOES, Genre.MUSIC),
        (GameType.HORSESHOES, Genre.MOTION),
        (GameType.PRESIDENT, Genre.RACING),
        (GameType.STOCKS, Genre.MOTION),
        (GameType.CARTOON, Genre.MOTION),
        (GameType.COSPLAY, Genre.RPG),
        (GameType.COSPLAY, Genre.ADVENTURE),
        (GameType.COSPLAY, Genre.RACING),
        (GameType.COSPLAY, Genre.MOTION),
        (GameType.SWIMSUIT, Genre.ONLINE_RPG),
        (GameType.SWIMSUIT, Genre.TRIVIA),
        (GameType.SWIMSUIT, Genre.MUSIC),
        (GameType.SWIMSUIT, Genre.MOTION),
        (GameType.MINI_SKIRT, Genre.SIMULATION),
        (GameType.MINI_SKIRT, Genre.ADVENTURE),
        (GameType.MINI_SKIRT, Genre.RACING),
        (GameType.MINI_SKIRT, Genre.AUDIO_NOVEL),
        (GameType.MUSHROOM, Genre.SHOOTER),
        (GameType.MUSHROOM, Genre.RACING),
        (GameType.PONCHO, Genre.ONLINE_SIM),
        (GameType.CHECKERS, Genre.RACING),
        (GameType.CHECKERS, Genre.MUSIC),
        (GameType.MAHJONG, Genre.SHOOTER),
        (GameType.MAHJONG, Genre.MUSIC),
        (GameType.REVERSI, Genre.ONLINE_SIM),
        (GameType.DANCE, Genre.RPG),
        (GameType.DANCE, Genre.ACTION),
        (GameType.DANCE, Genre.ACTION_RPG),
        (GameType.FITNESS, Genre.RACING),
        (GameType.WRESTLING, Genre.SHOOTER),
        (GameType.WRESTLING, Genre.MOTION),
        (GameType.BASKETBALL, Genre.ACTION_RPG),
        (GameType.BASKETBALL, Genre.MUSIC),
        (GameType.SNOWBOARD, Genre.BOARD),
        (GameType.GOLF, Genre.RPG),
        (GameType.GOLF, Genre.ACTION),
        (GameType.SWIMMING, Genre.SIMULATION),
        (GameType.SWIMMING, Genre.AUDIO_NOVEL),
        (GameType.VOLLEYBALL, Genre.ACTION_RPG),
        (GameType.PING_PONG, Genre.ADVENTURE),
        (GameType.PING_PONG, Genre.MUSIC),
        (GameType.SUMO, Genre.RPG),
        (GameType.BASEBALL, Genre.RACING),
        (GameType.BASEBALL, Genre.AUDIO_NOVEL),
        (GameType.WRESTLING, Genre.TABLE),
        (GameType.WRESTLING, Genre.MUSIC),
        (GameType.WRESTLING, Genre.MOTION),
        (GameType.F1_RACING, Genre.RPG),
        (GameType.F1_RACING, Genre.SHOOTER),
        (GameType.F1_RACING, Genre.MUSIC),
        (GameType.PINBALL, Genre.ACTION),
        (GameType.DATING, Genre.ACTION),
        (GameType.DATING, Genre.RACING),
        (GameType.DATING, Genre.MUSIC),
        (GameType.DATING, Genre.MOTION),
    ],
    # Not Bad
    [
        (GameType.SPORTS, Genre.ACTION),
        (GameType.SPORTS, Genre.RACING),
        (GameType.SPORTS, Genre.LIFE),
        (GameType.EXPLORATION, Genre.RPG),
        (GameType.EXPLORATION, Genre.ACTION),
        (GameType.EXPLORATION, Genre.ACTION_RPG),
        (GameType.MARTIAL_ARTS, Genre.ACTION),
        (GameType.FANTASY, Genre.TABLE),
        (GameType.FANTASY, Genre.ADVENTURE),
        (GameType.FANTASY, Genre.ACTION_RPG),
        (GameType.FANTASY, Genre.ONLINE_RPG),
        (GameType.VIRTUAL_PET, Genre.SIM_RPG),
        (GameType.VIRTUAL_PET, Genre.RACING),
        (GameType.SAMURAI, Genre.SIMULATION),
        (GameType.SAMURAI, Genre.ACTION),
        (GameType.SAMURAI, Genre.ONLINE_SIM),
        (GameType.SAMURAI, Genre.BOARD),
        (GameType.DUNGEON, Genre.RPG),
        (GameType.DUNGEON, Genre.TABLE),
        (GameType.DUNGEON, Genre.ACTION),
        (GameType.DUNGEON, Genre.SHOOTER),
        (GameType.DUNGEON, Genre.ONLINE_RPG),
        (GameType.DUNGEON, Genre.BOARD),
        (GameType.ROMANCE, Genre.ADVENTURE),
        (GameType.PIRATE, Genre.SIMULATION),
        (GameType.COMEDY, Genre.SIMULATION),
        (GameType.COMEDY, Genre.LIFE),
        (GameType.HORROR, Genre.ADVENTURE),
        (GameType.HORROR, Genre.MOTION),
        (GameType.WORD, Genre.SIMULATION),
        (GameType.WORD, Genre.TABLE),
        (GameType.WORD, Genre.PUZZLE),
        (GameType.TRAIN, Genre.TRIVIA),
        (GameType.TRAIN, Genre.BOARD),
        (GameType.ANIMAL, Genre.SIMULATION),
        (GameType.ANIMAL, Genre.TRIVIA),
        (GameType.ROBOT, Genre.ACTION),
        (GameType.ROBOT, Genre.TRIVIA),
        (GameType.AIRPLANE, Genre.SIMULATION),
        (GameType.AIRPLANE, Genre.ACTION),
        (GameType.AIRPLANE, Genre.SHOOTER),
        (GameType.AIRPLANE, Genre.RACING),
        (GameType.CONV_STORE, Genre.SIMULATION),
        (GameType.CONV_STORE, Genre.LIFE),
        (GameType.HISTORICAL, Genre.SIMULATION),
        (GameType.HISTORICAL, Genre.ONLINE_RPG),
        (GameType.HISTORICAL, Genre.ONLINE_SIM),
        (GameType.HISTORICAL, Genre.AUDIO_NOVEL),
        (GameType.BOOKSTORE, Genre.ONLINE_SIM),
        (GameType.COMICS, Genre.TRIVIA),
        (GameType.ART, Genre.ADVENTURE),
        (GameType.MOVIES, Genre.TRIVIA),
        (GameType.MOVIES, Genre.LIFE),
        (GameType.MOVIES, Genre.MUSIC),
        (GameType.EGYPT, Genre.RPG),
        (GameType.EGYPT, Genre.SIMULATION),
        (GameType.EGYPT, Genre.ADVENTURE),
        (GameType.EGYPT, Genre.TRIVIA),
        (GameType.LAWYER, Genre.SIMULATION),
        (GameType.LAWYER, Genre.TRIVIA),
        (GameType.MEDIEVAL, Genre.RPG),
        (GameType.MEDIEVAL, Genre.TABLE),
        (GameType.MEDIEVAL, Genre.ADVENTURE),
        (GameType.MEDIEVAL, Genre.ACTION_RPG),
        (GameType.MEDIEVAL, Genre.BOARD),
        (GameType.MONSTER, Genre.SHOOTER),
        (GameType.MONSTER, Genre.TRIVIA),
        (GameType.HUNTING, Genre.SIMULATION),
        (GameType.HUNTING, Genre.ONLINE_RPG),
        (GameType.HIGH_SCHOOL, Genre.SIMULATION),
        (GameType.HIGH_SCHOOL, Genre.ACTION),
        (GameType.HIGH_SCHOOL, Genre.AUDIO_NOVEL),
        (GameType.JUNIOR_HIGH, Genre.SIMULATION),
        (GameType.JUNIOR_HIGH, Genre.ACTION),
        (GameType.JUNIOR_HIGH, Genre.AUDIO_NOVEL),
        (GameType.WAR, Genre.TABLE),
        (GameType.WAR, Genre.SHOOTER),
        (GameType.WAR, Genre.ONLINE_SIM),
        (GameType.WAR, Genre.AUDIO_NOVEL),
        (GameType.NINJA, Genre.SHOOTER),
        (GameType.NINJA, Genre.TRIVIA),
        (GameType.CUTIE, Genre.ADVENTURE),
        (GameType.CUTIE, Genre.TRIVIA),
        (GameType.CUTIE, Genre.LIFE),
        (GameType.FASHION, Genre.SHOOTER),
        (GameType.FASHION, Genre.AUDIO_NOVEL),
        (GameType.DETECTIVE, Genre.LIFE),
        (GameType.MYSTERY, Genre.RPG),
        (GameType.MYSTERY, Genre.AUDIO_NOVEL),
        (GameType.COWBOY, Genre.RPG),
        (GameType.COWBOY, Genre.SIMULATION),
        (GameType.COWBOY, Genre.ACTION),
        (GameType.COWBOY, Genre.ACTION_RPG),
        (GameType.COWBOY, Genre.TRIVIA),
        (GameType.PRESIDENT, Genre.SIMULATION),
        (GameType.PRESIDENT, Genre.LIFE),
        (GameType.PRESIDENT, Genre.MOTION),
        (GameType.STOCKS, Genre.SIMULATION),
        (GameType.CARTOON, Genre.RPG),
        (GameType.CARTOON, Genre.ACTION),
        (GameType.CARTOON, Genre.ACTION_RPG),
        (GameType.CARTOON, Genre.TRIVIA),
        (GameType.CARTOON, Genre.BOARD),
        (GameType.COSPLAY, Genre.LIFE),
        (GameType.POP_STAR, Genre.TRIVIA),
        (GameType.POP_STAR, Genre.MUSIC),
        (GameType.POP_STAR, Genre.AUDIO_NOVEL),
        (GameType.MUSHROOM, Genre.TRIVIA),
        (GameType.CHESS, Genre.TABLE),
        (GameType.CHESS, Genre.TRIVIA),
        (GameType.CHESS, Genre.PUZZLE),
        (GameType.CHECKERS, Genre.TABLE),
        (GameType.CHECKERS, Genre.BOARD),
        (GameType.MAHJONG, Genre.SIMULATION),
        (GameType.MAHJONG, Genre.BOARD),
        (GameType.MAHJONG, Genre.PUZZLE),
        (GameType.REVERSI, Genre.TABLE),
        (GameType.REVERSI, Genre.BOARD),
        (GameType.DANCE, Genre.LIFE),
        (GameType.DRUMS, Genre.ACTION),
        (GameType.FITNESS, Genre.TRIVIA),
        (GameType.BASKETBALL, Genre.LIFE),
        (GameType.BASKETBALL, Genre.MOTION),
        (GameType.SKIING, Genre.ACTION),
        (GameType.SKIING, Genre.RACING),
        (GameType.SNOWBOARD, Genre.TRIVIA),
        (GameType.SNOWBOARD, Genre.MUSIC),
        (GameType.GOLF, Genre.SHOOTER),
        (GameType.GOLF, Genre.RACING),
        (GameType.GOLF, Genre.TRIVIA),
        (GameType.SWIMMING, Genre.ACTION),
        (GameType.SWIMMING, Genre.RACING),
        (GameType.SWIMMING, Genre.LIFE),
        (GameType.VOLLEYBALL, Genre.SIMULATION),
        (GameType.VOLLEYBALL, Genre.ADVENTURE),
        (GameType.MOTORSPORT, Genre.ACTION),
        (GameType.MOTORSPORT, Genre.ONLINE_SIM),
        (GameType.MOTORSPORT, Genre.LIFE),
        (GameType.MOTORSPORT, Genre.MOTION),
        (GameType.SOCCER, Genre.ACTION),
        (GameType.SOCCER, Genre.TRIVIA),
        (GameType.PING_PONG, Genre.ACTION),
        (GameType.PING_PONG, Genre.BOARD),
        (GameType.DATING, Genre.SIMULATION),
        (GameType.DATING, Genre.ADVENTURE),
        (GameType.DATING, Genre.TRIVIA),
        (GameType.SUMO, Genre.ADVENTURE),
        (GameType.SUMO, Genre.LIFE),
        (GameType.SUMO, Genre.AUDIO_NOVEL),
        (GameType.BASEBALL, Genre.SIMULATION),
        (GameType.BASEBALL, Genre.ACTION),
        (GameType.BASEBALL, Genre.LIFE),
        (GameType.BASEBALL, Genre.BOARD),
        (GameType.WRESTLING, Genre.ACTION),
        (GameType.WRESTLING, Genre.ONLINE_SIM),
        (GameType.WRESTLING, Genre.LIFE),
        (GameType.MARATHON, Genre.RPG),
        (GameType.MARATHON, Genre.ACTION),
        (GameType.MARATHON, Genre.RACING),
        (GameType.F1_RACING, Genre.ACTION),
        (GameType.F1_RACING, Genre.RACING),
        (GameType.F1_RACING, Genre.TRIVIA),
        (GameType.F1_RACING, Genre.MOTION),
        (GameType.PINBALL, Genre.SIMULATION),
        (GameType.PINBALL, Genre.TABLE),
        (GameType.SLOTS, Genre.SIMULATION),
        (GameType.SLOTS, Genre.TABLE),
        (GameType.SLOTS, Genre.BOARD),
        (GameType.SLOTS, Genre.PUZZLE),
    ],
    # Hmm
    [
        (GameType.SPORTS, Genre.SHOOTER),
        (GameType.SPORTS, Genre.AUDIO_NOVEL),
        (GameType.EXPLORATION, Genre.SHOOTER),
        (GameType.EXPLORATION, Genre.PUZZLE),
        (GameType.MARTIAL_ARTS, Genre.SIMULATION),
        (GameType.MARTIAL_ARTS, Genre.PUZZLE),
        (GameType.FANTASY, Genre.MUSIC),
        (GameType.VIRTUAL_PET, Genre.BOARD),
        (GameType.VIRTUAL_PET, Genre.MUSIC),
        (GameType.SAMURAI, Genre.SHOOTER),
        (GameType.SAMURAI, Genre.ONLINE_RPG),
        (GameType.DUNGEON, Genre.LIFE),
        (GameType.DUNGEON, Genre.PUZZLE),
        (GameType.DUNGEON, Genre.MUSIC),
        (GameType.ROMANCE, Genre.RPG),
        (GameType.ROMANCE, Genre.ACTION_RPG),
        (GameType.ROMANCE, Genre.PUZZLE),
        (GameType.PIRATE, Genre.PUZZLE),
        (GameType.PIRATE, Genre.AUDIO_NOVEL),
        (GameType.HORROR, Genre.TABLE),
        (GameType.HORROR, Genre.LIFE),
        (GameType.HORROR, Genre.PUZZLE),
        (GameType.WORD, Genre.ONLINE_SIM),
        (GameType.ANIMAL, Genre.SHOOTER),
        (GameType.ANIMAL, Genre.ONLINE_RPG),
        (GameType.ANIMAL, Genre.ONLINE_SIM),
        (GameType.ROBOT, Genre.PUZZLE),
        (GameType.AIRPLANE, Genre.LIFE),
        (GameType.CONV_STORE, Genre.RPG),
        (GameType.CONV_STORE, Genre.ACTION),
        (GameType.HISTORICAL, Genre.BOARD),
        (GameType.HISTORICAL, Genre.PUZZLE),
        (GameType.BOOKSTORE, Genre.SHOOTER),
        (GameType.BOOKSTORE, Genre.RACING),
        (GameType.BOOKSTORE, Genre.MUSIC),
        (GameType.COMICS, Genre.ACTION),
        (GameType.COMICS, Genre.RACING),
        (GameType.ART, Genre.TABLE),
        (GameType.ART, Genre.RACING),
        (GameType.ART, Genre.MUSIC),
        (GameType.ART, Genre.MOTION),
        (GameType.MOVIES, Genre.RACING),
        (GameType.GAME_CO, Genre.ADVENTURE),
        (GameType.GAME_CO, Genre.MUSIC),
        (GameType.EGYPT, Genre.TABLE),
        (GameType.TOWN, Genre.ACTION),
        (GameType.TOWN, Genre.ONLINE_RPG),
        (GameType.ARCHITECTURE, Genre.ACTION),
        (GameType.ARCHITECTURE, Genre.BOARD),
        (GameType.LAWYER, Genre.MUSIC),
        (GameType.LAWYER, Genre.AUDIO_NOVEL),
        (GameType.MONSTER, Genre.TABLE),
        (GameType.MONSTER, Genre.PUZZLE),
        (GameType.HUNTING, Genre.RPG),
        (GameType.HUNTING, Genre.BOARD),
        (GameType.HUNTING, Genre.MUSIC),
        (GameType.HIGH_SCHOOL, Genre.SHOOTER),
        (GameType.HIGH_SCHOOL, Genre.BOARD),
        (GameType.JUNIOR_HIGH, Genre.SHOOTER),
        (GameType.JUNIOR_HIGH, Genre.BOARD),
        (GameType.WAR, Genre.RACING),
        (GameType.WAR, Genre.PUZZLE),
        (GameType.NINJA, Genre.RACING),
        (GameType.CUTIE, Genre.SHOOTER),
        (GameType.OGRE, Genre.SHOOTER),
        (GameType.OGRE, Genre.LIFE),
        (GameType.OGRE, Genre.AUDIO_NOVEL),
        (GameType.MYSTERY, Genre.SIMULATION),
        (GameType.MYSTERY, Genre.BOARD),
        (GameType.MYSTERY, Genre.PUZZLE),
        (GameType.PRESIDENT, Genre.TABLE),
        (GameType.PRESIDENT, Genre.ONLINE_RPG),
        (GameType.PRESIDENT, Genre.ONLINE_SIM),
        (GameType.STOCKS, Genre.ACTION),
        (GameType.STOCKS, Genre.SHOOTER),
        (GameType.STOCKS, Genre.LIFE),
        (GameType.COSPLAY, Genre.ACTION),
        (GameType.POP_STAR, Genre.ACTION),
        (GameType.MUSHROOM, Genre.MOTION),
        (GameType.CHESS, Genre.SHOOTER),
        (GameType.CHESS, Genre.AUDIO_NOVEL),
        (GameType.CHECKERS, Genre.ACTION),
        (GameType.DANCE, Genre.SHOOTER),
        (GameType.WRESTLING, Genre.RPG),
        (GameType.WRESTLING, Genre.SIM_RPG),
        (GameType.BASKETBALL, Genre.RPG),
        (GameType.BASKETBALL, Genre.PUZZLE),
        (GameType.SNOWBOARD, Genre.TABLE),
        (GameType.SWIMMING, Genre.MUSIC),
        (GameType.VOLLEYBALL, Genre.ACTION),
        (GameType.VOLLEYBALL, Genre.PUZZLE),
        (GameType.MOTORSPORT, Genre.ADVENTURE),
        (GameType.SOCCER, Genre.SHOOTER),
        (GameType.PING_PONG, Genre.SHOOTER),
        (GameType.SUMO, Genre.SHOOTER),
        (GameType.BASEBALL, Genre.ACTION_RPG),
        (GameType.MARATHON, Genre.PUZZLE),
        (GameType.SLOTS, Genre.ONLINE_RPG),
    ],
    # Not Good
    [
        (GameType.SPORTS, Genre.ACTION_RPG),
        (GameType.SPORTS, Genre.MUSIC),
        (GameType.EXPLORATION, Genre.MUSIC),
        (GameType.MARTIAL_ARTS, Genre.RACING),
        (GameType.MARTIAL_ARTS, Genre.ONLINE_SIM),
        (GameType.FANTASY, Genre.RACING),
        (GameType.FANTASY, Genre.MOTION),
        (GameType.SAMURAI, Genre.MUSIC),
        (GameType.DUNGEON, Genre.TRIVIA),
        (GameType.DUNGEON, Genre.MOTION),
        (GameType.ROMANCE, Genre.ACTION),
        (GameType.ROMANCE, Genre.RACING),
        (GameType.PIRATE, Genre.TABLE),
        (GameType.PIRATE, Genre.SHOOTER),
        (GameType.PIRATE, Genre.RACING),
        (GameType.PIRATE, Genre.ONLINE_SIM),
        (GameType.COMEDY, Genre.RPG),
        (GameType.HORROR, Genre.RACING),
        (GameType.HORROR, Genre.MUSIC),
        (GameType.WORD, Genre.ACTION_RPG),
        (GameType.WORD, Genre.RACING),
        (GameType.WORD, Genre.ONLINE_RPG),
        (GameType.AIRPLANE, Genre.RPG),
        (GameType.AIRPLANE, Genre.ADVENTURE),
        (GameType.AIRPLANE, Genre.BOARD),
        (GameType.AIRPLANE, Genre.AUDIO_NOVEL),
        (GameType.CONV_STORE, Genre.SHOOTER),
        (GameType.HISTORICAL, Genre.RACING),
        (GameType.HISTORICAL, Genre.MUSIC),
        (GameType.COMICS, Genre.RPG),
        (GameType.COMICS, Genre.SHOOTER),
        (GameType.COMICS, Genre.MUSIC),
        (GameType.ART, Genre.ACTION_RPG),
        (GameType.MOVIES, Genre.SHOOTER),
        (GameType.GAME_CO, Genre.MOTION),
        (GameType.TOWN, Genre.SHOOTER),
        (GameType.TOWN, Genre.PUZZLE),
        (GameType.ARCHITECTURE, Genre.ADVENTURE),
        (GameType.ARCHITECTURE, Genre.RACING),
        (GameType.LAWYER, Genre.RACING),
        (GameType.HIGH_SCHOOL, Genre.RACING),
        (GameType.JUNIOR_HIGH, Genre.RACING),
        (GameType.WAR, Genre.ADVENTURE),
        (GameType.NINJA, Genre.PUZZLE),
        (GameType.OGRE, Genre.TRIVIA),
        (GameType.DETECTIVE, Genre.TABLE),
        (GameType.DETECTIVE, Genre.SHOOTER),
        (GameType.DETECTIVE, Genre.RACING),
        (GameType.MYSTERY, Genre.ONLINE_RPG),
        (GameType.PRESIDENT, Genre.SHOOTER),
        (GameType.STOCKS, Genre.RPG),
        (GameType.STOCKS, Genre.ADVENTURE),
        (GameType.STOCKS, Genre.RACING),
        (GameType.STOCKS, Genre.PUZZLE),
        (GameType.STOCKS, Genre.MUSIC),
        (GameType.STOCKS, Genre.AUDIO_NOVEL),
        (GameType.CARTOON, Genre.RACING),
        (GameType.COSPLAY, Genre.TABLE),
        (GameType.COSPLAY, Genre.MUSIC),
        (GameType.POP_STAR, Genre.SHOOTER),
        (GameType.POP_STAR, Genre.RACING),
        (GameType.MUSHROOM, Genre.BOARD),
        (GameType.MUSHROOM, Genre.MUSIC),
        (GameType.CHESS, Genre.RPG),
        (GameType.CHESS, Genre.MUSIC),
        (GameType.CHECKERS, Genre.RPG),
        (GameType.CHECKERS, Genre.SHOOTER),
        (GameType.MAHJONG, Genre.RACING),
        (GameType.REVERSI, Genre.RACING),
        (GameType.REVERSI, Genre.AUDIO_NOVEL),
        (GameType.WRESTLING, Genre.RACING),
        (GameType.BASKETBALL, Genre.TABLE),
        (GameType.SKIING, Genre.PUZZLE),
        (GameType.SWIMMING, Genre.ACTION_RPG),
        (GameType.MOTORSPORT, Genre.ONLINE_RPG),
        (GameType.MOTORSPORT, Genre.PUZZLE),
        (GameType.SOCCER, Genre.RACING),
        (GameType.PING_PONG, Genre.RACING),
        (GameType.SUMO, Genre.RACING),
        (GameType.BASEBALL, Genre.SHOOTER),
        (GameType.MARATHON, Genre.ADVENTURE),
        (GameType.MARATHON, Genre.SHOOTER),
        (GameType.F1_RACING, Genre.PUZZLE),
        (GameType.PINBALL, Genre.RACING),
        (GameType.SLOTS, Genre.SHOOTER),
    ],
]


def filter_combinations(combinations, game_types, genres):
    output = []
    for game_type, genre in combinations:
        if game_type in game_types and genre in genres:
            output.append((game_type, genre))
    return output


def filter_combination_tiers(game_types, genres):
    output = []
    for combinations in COMBINATIONS:
        output.append(filter_combinations(combinations, game_types, genres))
    return output


def append_type_or_genre(value, game_types, genres):
    try:
        genres.append(Genre(name))
    except ValueError:
        pass

    try:
        game_types.append(GameType(name))
    except ValueError:
        pass

    raise ValueError(value)


if __name__ == "__main__":
    game_types = []
    genres = []

    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <game-type-or-genre...>")
        sys.exit(1)

    for name in sys.argv[1:]:
        append_type_or_genre(name, game_types, genres)

    combinations = filter_combination_tiers(game_types, genres)
    for i, tier in enumerate(combinations):
        if tier:
            tier_name = COMBINATION_TIER_NAMES[i]
            print(tier_name)

            for game_type, genre in tier:
                print(f"* {game_type.value} & {genre.value}")
