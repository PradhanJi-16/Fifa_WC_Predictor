# src/elo.py

def expected_score(rating_a, rating_b):
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))


def update_elo(rating_a, rating_b, result, k=30):
    """
    result:
    1 → A wins
    0 → B wins
    0.5 → draw
    """

    exp_a = expected_score(rating_a, rating_b)
    exp_b = expected_score(rating_b, rating_a)

    new_a = rating_a + k * (result - exp_a)
    new_b = rating_b + k * ((1 - result) - exp_b)

    return new_a, new_b