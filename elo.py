from consts import DEFAULT_K_FACTOR


def calculate_delta_elo(winner_elo, loser_elo, k_factor=DEFAULT_K_FACTOR):
    expected_winner = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
    expected_loser = 1 / (1 + 10 ** ((winner_elo - loser_elo) / 400))
    delta_winner = k_factor * (1 - expected_winner)
    delta_loser = k_factor * (0 - expected_loser)
    return delta_winner, delta_loser


def calculate_same_team_delta_elo(winner_elo, loser_elo, k_factor=DEFAULT_K_FACTOR):
    dwinner, dloser = calculate_delta_elo(winner_elo, loser_elo, k_factor)
    return dwinner, dloser


def calculate_diff_team_delta_elo(winner_elo, loser_elo, winner_team_elo, loser_team_elo, k_factor=DEFAULT_K_FACTOR):
    dwinner, dloser = calculate_delta_elo(
        winner_team_elo + winner_elo, loser_team_elo + loser_elo, k_factor)
    return dwinner, dloser
