"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


# Data Flow — see docs/dataflow.md for a Mermaid.js visualization


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # User taste profile — defines what the recommender compares each song against
    # Chosen to sit in the middle of the feature space so the scoring formula
    # must genuinely differentiate between candidates (e.g., "Rooftop Lights"
    # should rank above "Storm Runner," but "Storm Runner" shouldn't score zero).
    user_prefs = {
        "favorite_genre": "indie pop",   # matches Rooftop Lights; overlaps with pop
        "favorite_mood": "happy",        # separates upbeat tracks from chill/intense
        "target_energy": 0.70,           # mid-high — rewards both pop and rock partially
        "likes_acoustic": False,         # prefers produced/electronic textures
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print("       Top 5 Recommendations")
    print("=" * 50)

    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']} by {song['artist']}")
        print(f"       Score: {score:.2f} / 7.50")
        print("       Reasons:")
        for reason in reasons:
            print(f"         - {reason}")
        print("-" * 50)


if __name__ == "__main__":
    main()
