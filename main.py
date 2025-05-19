import random
import csv

from consts import DEFAULT_K_FACTOR, FIRST_K_FACTOR, SECOND_K_FACTOR, BASE_TEAM_ELO
from classes import Driver, RaceResult, Constructor, Race
from elo import calculate_same_team_delta_elo, calculate_diff_team_delta_elo, calculate_delta_elo
from utils import read_csv


highest_elo = 0
highest_team_elo = 0
highest_driver: Driver | None = None
highest_team: Constructor | None = None


def results_per_race(race_results):
    group = []
    race_id = -1
    for rr in race_results:
        if race_id == -1:
            race_id = rr.race_id
        elif rr.race_id != race_id:
            yield group
            group = []
            race_id = rr.race_id

        group.append(rr)

    yield group


def simulator(races, drivers, constructors, race_results):
    global highest_elo
    global highest_driver
    global highest_team_elo
    global highest_team

    count = 0
    year = -1
    for rpr in results_per_race(race_results):
        race_year = races[rpr[0].race_id].year
        if year == -1:
            year = race_year
        elif year != race_year:
            year = race_year
            count = 0
            this_year_constructors = []
            for rr in rpr:
                if rr.constructor_id not in this_year_constructors:
                    this_year_constructors.append(rr.constructor_id)

            for constructor_id in this_year_constructors:
                constructors[constructor_id].elo = BASE_TEAM_ELO

        k_factor = DEFAULT_K_FACTOR
        # if count == 0:
        #    k_factor = FIRST_K_FACTOR
        #    count += 1
        # elif count == 1:
        #    k_factor = SECOND_K_FACTOR
        #    count += 1

        finish_order = [drivers[rr.driver_id] for rr in rpr]

        # ensures delta elo is 0 for every player and team
        for player in finish_order:
            player.delta_elo = 0
        for team in constructors.values():
            team.delta_elo = 0

        # update each constructor delta elo
        for i in range(len(finish_order)):
            for j in range(len(finish_order)):
                if i == j:
                    continue

                winner_rr = rpr[i] if i < j else rpr[j]
                loser_rr = rpr[j] if i < j else rpr[i]
                winner_constructor = constructors[winner_rr.constructor_id]
                loser_constructor = constructors[loser_rr.constructor_id]
                dwinner, dloser = calculate_delta_elo(
                    winner_constructor.elo, loser_constructor.elo,
                    32)
                winner_constructor.delta_elo += dwinner
                loser_constructor.delta_elo += dloser

        for c in constructors.values():
            c.elo += c.delta_elo
            if c.elo > highest_team_elo:
                highest_team_elo = c.elo
                highest_team = c

        # -----

        # update each player delta elo
        for i in range(len(finish_order)):
            for j in range(len(finish_order)):
                if i == j:
                    continue

                winner = finish_order[i] if i < j else finish_order[j]
                loser = finish_order[j] if i < j else finish_order[i]
                winner_rr = rpr[i] if i < j else rpr[j]
                loser_rr = rpr[j] if i < j else rpr[i]

                if winner_rr.constructor_id == loser_rr.constructor_id:
                    welo, delo = calculate_same_team_delta_elo(
                        winner.elo, loser.elo,
                        DEFAULT_K_FACTOR
                    )
                    winner.delta_elo += welo
                    loser.delta_elo += delo

                else:
                    winner_constructor = constructors[winner_rr.constructor_id]
                    loser_constructor = constructors[loser_rr.constructor_id]
                    dwinner, dloser = calculate_diff_team_delta_elo(
                        winner.elo, loser.elo, winner_constructor.elo, loser_constructor.elo,
                        2
                    )
                    winner.delta_elo += dwinner
                    loser.delta_elo += dloser

        # update each player and team elo
        for player in finish_order:
            player.elo += player.delta_elo
            if player.elo > highest_elo:
                highest_elo = player.elo
                highest_driver = player

        yield rpr[0].race_id if len(rpr) > 0 else -1, finish_order


def main():
    drivers, constructors, races, race_results = read_csv()

    races_filtered = list(
        filter(lambda x: x.year >= 1987, races.values()))
    races_filtered.sort(key=lambda x: (x.year, x.round))

    valid_race_ids = {r.id for r in races_filtered}
    race_results_filtered = list(
        filter(lambda x: x.race_id in valid_race_ids, race_results.values()))
    race_results_filtered.sort(key=lambda x: (
        races[x.race_id].year, races[x.race_id].round, x.position_order))

    valid_driver_ids = {rr.driver_id for rr in race_results_filtered}
    valid_constructor_ids = {
        rr.constructor_id for rr in race_results_filtered}

    drivers_filtered = [drivers[driver_id] for driver_id in valid_driver_ids]
    constructors_filtered = [constructors[constructor_id]
                             for constructor_id in valid_constructor_ids]
    year = -1
    for (race_id, finish_order) in simulator(races, drivers, constructors, race_results_filtered):
        race = races[race_id]
        if year == -1:
            year = race.year
        elif year != race.year:
            last_drivers = sorted(finish_order, key=lambda x: x.elo)
            rrs = list(filter(lambda x: x.race_id ==
                       race_id, race_results_filtered))
            last_constructors = list(filter(lambda x: x.id in [
                rr.constructor_id for rr in rrs], constructors_filtered))
            last_constructors = sorted(last_constructors, key=lambda x: x.elo)
            print(year)
            print("PEAK ELO")
            print(
                f"{highest_driver.name if highest_driver is not None else 'None'} -> {highest_elo}")
            print(
                f"{highest_team.name if highest_team is not None else 'None'} -> {highest_team_elo}")

            while True:
                c = input("Driver [d] or Constructor [c]? ")

                print("==== DRIVERS ====")
                if c == "d":
                    for driver in last_drivers:
                        print(
                            f"{driver.name}-> [{round(driver.elo, 1)}, {round(driver.delta_elo, 1)}]")
                elif c == "c":
                    print("==== CONSTRUCTORS ====")
                    for constructor in last_constructors:
                        print(
                            f"{constructor.name}-> [{round(constructor.elo, 1)}, {round(constructor.delta_elo, 1)}]")
                else:
                    break
            year = race.year


if __name__ == "__main__":
    main()
