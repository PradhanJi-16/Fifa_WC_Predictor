from collections import defaultdict
from src.predict import predict_match
import random

from src.visualize import plot_probabilities

def simulate_group(group_teams, model, team_stats, verbose=True):
    table = defaultdict(lambda:{
        "points": 0,
        "gd":0
    })

    matches = [
        (group_teams[0], group_teams[1]),
        (group_teams[2], group_teams[3]),
        (group_teams[0], group_teams[2]),
        (group_teams[1], group_teams[3]),
        (group_teams[0], group_teams[3]),
        (group_teams[1], group_teams[2])
    ]

    for team_a, team_b in matches:
        probs = predict_match(model, team_stats, team_a, team_b, is_home=0)
        if max(probs.values()) > 0.75:
            result = max(probs, key=probs.get)
        else:
            result = random.choices(
                ["Win", "Loss", "Draw"],
                weights=[probs.get("Win",0), probs.get("Loss",0), probs.get("Draw",0)]
            )[0]

        if result == "Win":
            table[team_a]["points"] += 3
            table[team_a]["gd"] +=1
            table[team_b]["gd"] -=1
        elif result == "Loss":
            table[team_b]["points"] += 3
            table[team_b]["gd"] += 1
            table[team_a]["gd"] -= 1
        else:
            table[team_a]["points"] += 1
            table[team_b]["points"] += 1

    sorted_teams = sorted(
        table.items(),
        key = lambda x:(x[1]["points"], x[1]["gd"]),
        reverse = True
    )

    return sorted_teams 


def knockout_match(team_a, team_b, model, team_stats):
    probs = predict_match(model, team_stats, team_a, team_b, is_home=0)

    choices = ["Win", "Loss", "Draw"]
    weights = [probs.get(c, 0) for c in choices]

    if max(probs.values()) > 0.75:
        result = max(probs, key=probs.get)
    else:
        result = random.choices(
            ["Win", "Loss", "Draw"],
            weights=[probs.get("Win",0), probs.get("Loss",0), probs.get("Draw",0)]
        )[0]

    if result == "Win":
        return team_a
    elif result == "Loss":
        return team_b
    else:
        return random.choice([team_a, team_b])
    

def generate_round_of_32(groups_results):
    qualified = []
    third_place = []

    for group in groups_results:
        # Top 2 directly qualify
        qualified.append(group[0][0])
        qualified.append(group[1][0])

        # Store 3rd place
        third_place.append(group[2])

    # Sort 3rd place teams
    third_place_sorted = sorted(
        third_place,
        key=lambda x: (x[1]["points"], x[1]["gd"]),
        reverse=True
    )

    # Take best 8
    best_third = [team[0] for team in third_place_sorted[:8]]

    return qualified + best_third


def play_knockout_round(teams, model, team_stats, round_name, verbose=True):
    if verbose:
        print(f"\n===== {round_name} =====")

    winners = []

    for i in range(0, len(teams), 2):
        t1 = teams[i]
        t2 = teams[i+1]

        winner = knockout_match(t1, t2, model, team_stats)
        if verbose:
            print(f"{t1} vs {t2} → {winner}")

        winners.append(winner)

    return winners

def simulate_multiple(model, team_stats, n=100):
    winners = {}

    # Show ONLY first simulation
    print("\n===== SAMPLE TOURNAMENT =====")
    simulate_tournament(model, team_stats, verbose=True)

    # Run rest silently
    for _ in range(n):
        winner = simulate_tournament(model, team_stats, verbose=False)
        winners[winner] = winners.get(winner, 0) + 1

    print("\n===== FINAL PROBABILITIES =====")

    for team, count in sorted(winners.items(), key=lambda x: x[1], reverse=True):
        prob = (count / n) * 100
        print(f"{team}: {prob:.2f}%")
    
    plot_probabilities(winners)


def simulate_tournament(model, team_stats, verbose=True):

    groups = {
        "A": ["Mexico", "South Africa", "South Korea", "Denmark"],

        "B": ["Canada", "Italy", "Qatar", "Switzerland"],

        "C": ["Brazil", "Morocco", "Haiti", "Scotland"],

        "D": ["United States", "Paraguay", "Australia", "Turkey"],

        "E": ["Germany", "Curacao", "Ivory Coast", "Ecuador"],

        "F": ["Netherlands", "Japan", "Albania", "Tunisia"],

        "G": ["Belgium", "Egypt", "Iran", "New Zealand"],

        "H": ["Spain", "Cape Verde", "Saudi Arabia", "Uruguay"],

        "I": ["France", "Senegal", "Bolivia", "Norway"],

        "J": ["Argentina", "Algeria", "Austria", "Jordan"],

        "K": ["Portugal", "Jamaica", "Uzbekistan", "Colombia"],

        "L": ["England", "Croatia", "Ghana", "Panama"],
    }

    group_results = []
    if verbose:
        print("\n===== GROUP STAGE =====")

    for group_name, teams in groups.items():
        if verbose:
            print(f"\n--- Group {group_name} ---")
        result = simulate_group(teams, model, team_stats,verbose)

        for team, stats in result:
            if verbose:
                print(team, stats)

        group_results.append(result)

    # Round of 32
    round_32 = generate_round_of_32(group_results)

    # Shuffle for randomness
    random.shuffle(round_32)

    r16 = play_knockout_round(round_32, model, team_stats, "ROUND OF 32",verbose)
    qf = play_knockout_round(r16, model, team_stats, "ROUND OF 16",verbose)
    sf = play_knockout_round(qf, model, team_stats, "QUARTER FINAL",verbose)
    final = play_knockout_round(sf, model, team_stats, "SEMI FINAL",verbose)

    champion = knockout_match(final[0], final[1], model, team_stats)
    if verbose:
        print(f"\n🏆 WORLD CUP WINNER: {champion}")
    return champion