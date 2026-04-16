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

    user_profiles = [
        {
            "name": "High-Energy Pop Fan",
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.90,
            "likes_acoustic": False,
        },
        {
            "name": "Chill Lofi Listener",
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.40,
            "likes_acoustic": True,
        },
        {
            "name": "Deep Intense Rocker",
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.85,
            "likes_acoustic": False,
        },
    ]

    for profile in user_profiles:
        name = profile.pop("name")
        recommendations = recommend_songs(profile, songs, k=5)

        print("\n" + "=" * 50)
        print(f"  Profile: {name}")
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
