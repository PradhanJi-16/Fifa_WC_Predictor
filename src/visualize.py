import matplotlib.pyplot as plt


def plot_probabilities(winners_dict, top_n=10):
    # Sort teams by probability
    sorted_teams = sorted(winners_dict.items(), key=lambda x: x[1], reverse=True)

    # Take top N
    top_teams = sorted_teams[:top_n]

    teams = [team for team, _ in top_teams]
    counts = [count for _, count in top_teams]

    # Convert to percentage
    total = sum(winners_dict.values())
    percentages = [(c / total) * 100 for c in counts]

    # Plot
    plt.figure()
    plt.bar(teams, percentages)

    plt.title("Top Teams - World Cup Winning Probability")
    plt.xlabel("Teams")
    plt.ylabel("Probability (%)")

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()