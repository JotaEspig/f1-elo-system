from dataclasses import dataclass

from consts import BASE_ELO, BASE_TEAM_ELO


@dataclass
class Constructor:
    id: int
    name: str
    elo: float = BASE_TEAM_ELO
    delta_elo: float = 0


@dataclass
class Driver:
    id: int
    name: str
    elo: float = BASE_ELO
    delta_elo: float = 0

    def __repr__(self):
        return f"{self.name}"


@dataclass
class Race:
    id: int
    name: str
    year: int
    round: int
    circuit_id: int


@dataclass
class RaceResult:
    id: int
    race_id: int
    driver_id: int
    constructor_id: int
    position_order: int
    status_id: int
