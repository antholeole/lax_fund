import csv
from dataclasses import dataclass, field
from random import shuffle
from typing import List
import random
from typing_extensions import Self

@dataclass
class GameRanking:
    ohio: int = field(default_factory=lambda: 1)
    # If you didn't fill out the form, give the default baylor a weight
    # of 2 since it's the one people picked the least
    baylor: int = field(default_factory=lambda: 2)
    kansas_state: int = field(default_factory=lambda: 1)

    def rank_from_str(input_str: str) -> int:
        if input_str == 'Top Choice':
            return 3
        if input_str == 'Second Choice':
            return 2
        if input_str == 'Last Choice':
            return 1
        else:
            return 0

@dataclass
class Player:
    name: str
    ranking: GameRanking
    year: int

    def from_row(row: List[str]) -> Self:
        player_year = int(row[3])


        return Player(
            name=f"{row[1]} {row[2]}",
            year=player_year,
            ranking=GameRanking(
                ohio=GameRanking.rank_from_str(row[5]),
                kansas_state=GameRanking.rank_from_str(row[6]),
                baylor=GameRanking.rank_from_str(row[7]),
            )
        )



players: List[Player] = []
with open('form_res.csv') as fund_no_groupme:
    player_reader = csv.reader(fund_no_groupme)

    # skip the fucking header
    next(player_reader)

    players.extend([Player.from_row(row) for row in player_reader])

groupme_players = []
with open('groupme.csv') as groupme:
    player_reader = csv.reader(groupme)
    groupme_players.extend([f"{row[0]} {row[1]}" for row in player_reader])


difference = list(set(groupme_players).difference(set(map(lambda player: player.name, players))))

# Since these fuckers didn't want to fill out the form,
# they get game weights of one
map(lambda player_name: players.append(Player(name=player_name, ranking=GameRanking())), difference)
max_player_year = max(map(lambda player: player.year, players))

weights = [set(), set(), set()] #ohio, baylor, ks

# assign all the players that arent freshmen their desired game
for player in filter(lambda player: player.year >= 2, players):
    if player.ranking.baylor == 3:

        weights[1].add(player.name)
    elif player.ranking.kansas_state == 3:
        weights[2].add(player.name)
    elif player.ranking.ohio == 3:
        weights[0].add(player.name)

# give the freshmen all that isn't their last choice and isn't
for player in filter(lambda player: player.year == 1, players):
    if player.ranking.baylor > 1:
        weights[1].add(player.name)
    elif player.ranking.kansas_state > 1:
        weights[2].add(player.name)



shuffle(difference)
for player in difference:
    min(weights, key=len).add(player)

f = open("output.txt", "w")

f.write("# OHIO\n")
for player in weights[0]:
    f.write(player + "\n")

f.write("\n\n# BAYLOR\n")
for player in weights[1]:
    f.write(player + "\n")

f.write("\n\n# KANSAS STATE\n")
for player in weights[2]:
    f.write(player + "\n")

print([len(group) for group in weights])

