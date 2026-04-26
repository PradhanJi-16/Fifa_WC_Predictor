from src.data_preprocessing import load_and_preprocess
from src.model import train_model
from src.tournament import simulate_multiple 

def main():
    print("Loading and preprocessing data...")
    df, team_stats = load_and_preprocess()

    
    print("Training model...")
    model = train_model(df)

    print("\nStarting FIFA World Cup Simulation...")
    simulate_multiple(model, team_stats, n=100)
    

if __name__ == "__main__":
    main()
