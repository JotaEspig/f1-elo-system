import csv

from classes import Driver, Constructor, Race, RaceResult


def read_csv() -> tuple[dict[int, Driver], dict[int, Constructor], dict[int, Race], dict[int, RaceResult]]:
    drivers = {}
    constructors = {}  # ELO must be reset every start of the season
    races = {}
    race_results = {}

    with open("f1data/drivers.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            driver_id = int(row["driverId"])
            driver = Driver(id=driver_id,
                            name=f"{row['forename']} {row['surname']}")
            drivers[driver_id] = driver

    with open("f1data/constructors.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            constructor_id = int(row["constructorId"])
            constructor = Constructor(id=constructor_id,
                                      name=row["name"])
            constructors[constructor_id] = constructor

    with open("f1data/races.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            race_id = int(row["raceId"])
            race = Race(id=race_id,
                        name=row["name"],
                        year=int(row["year"]),
                        round=int(row["round"]),
                        circuit_id=int(row["circuitId"]))
            races[race_id] = race

    with open("f1data/results.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            result_id = int(row["resultId"])
            rr = RaceResult(id=result_id,
                            race_id=int(row["raceId"]),
                            driver_id=int(row["driverId"]),
                            constructor_id=int(row["constructorId"]),
                            position_order=int(row["positionOrder"]),
                            status_id=int(row["statusId"]))
            race_results[result_id] = rr

    return drivers, constructors, races, race_results
