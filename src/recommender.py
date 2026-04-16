from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read a CSV file and return a list of song dictionaries with numeric fields converted."""
    import csv

    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for key in int_fields:
                row[key] = int(row[key])
            for key in float_fields:
                row[key] = float(row[key])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences and return (score, reasons)."""
    score = 0.0
    reasons = []

    # Genre match (weight 3.0)
    genre_val = 1.0 if song["genre"].lower() == user_prefs["favorite_genre"].lower() else 0.0
    score += genre_val * 3.0
    if genre_val:
        reasons.append(f"genre is {song['genre']} (exact match, +3.0)")

    # Mood match (weight 2.0)
    mood_val = 1.0 if song["mood"].lower() == user_prefs["favorite_mood"].lower() else 0.0
    score += mood_val * 2.0
    if mood_val:
        reasons.append(f"mood is {song['mood']} (exact match, +2.0)")

    # Energy fit (weight 1.5)
    energy_val = 1 - abs(song["energy"] - user_prefs["target_energy"])
    energy_contribution = energy_val * 1.5
    score += energy_contribution
    reasons.append(f"energy {song['energy']:.2f} vs target {user_prefs['target_energy']:.2f} (+{energy_contribution:.2f})")

    # Acoustic fit (weight 1.0)
    if user_prefs["likes_acoustic"]:
        acoustic_val = song["acousticness"]
    else:
        acoustic_val = 1 - song["acousticness"]
    score += acoustic_val * 1.0
    reasons.append(f"acousticness {song['acousticness']:.2f} (+{acoustic_val * 1.0:.2f})")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Score all songs and return the top k sorted by score descending."""
    # Expected return format: (song_dict, score, explanation)
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]