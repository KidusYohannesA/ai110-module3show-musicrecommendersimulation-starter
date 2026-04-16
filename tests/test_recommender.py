import os
from src.recommender import Song, UserProfile, Recommender, load_songs, score_song, recommend_songs


# ── Fixtures ──────────────────────────────────────────────

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")

SAMPLE_SONG = {
    "id": 1, "title": "Test Song", "artist": "Artist",
    "genre": "pop", "mood": "happy", "energy": 0.80,
    "tempo_bpm": 120, "valence": 0.9, "danceability": 0.8,
    "acousticness": 0.20,
}

SAMPLE_PREFS = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.80,
    "likes_acoustic": False,
}


def make_small_recommender() -> Recommender:
    songs = [
        Song(id=1, title="Test Pop Track", artist="Test Artist",
             genre="pop", mood="happy", energy=0.8, tempo_bpm=120,
             valence=0.9, danceability=0.8, acousticness=0.2),
        Song(id=2, title="Chill Lofi Loop", artist="Test Artist",
             genre="lofi", mood="chill", energy=0.4, tempo_bpm=80,
             valence=0.6, danceability=0.5, acousticness=0.9),
    ]
    return Recommender(songs)


def make_catalog():
    return [
        {"id": 1, "title": "Pop Hit", "artist": "A", "genre": "pop",
         "mood": "happy", "energy": 0.82, "tempo_bpm": 118,
         "valence": 0.84, "danceability": 0.79, "acousticness": 0.18},
        {"id": 2, "title": "Lofi Beat", "artist": "B", "genre": "lofi",
         "mood": "chill", "energy": 0.42, "tempo_bpm": 78,
         "valence": 0.56, "danceability": 0.62, "acousticness": 0.71},
        {"id": 3, "title": "Rock Anthem", "artist": "C", "genre": "rock",
         "mood": "intense", "energy": 0.91, "tempo_bpm": 152,
         "valence": 0.48, "danceability": 0.66, "acousticness": 0.10},
        {"id": 4, "title": "Jazz Cafe", "artist": "D", "genre": "jazz",
         "mood": "relaxed", "energy": 0.37, "tempo_bpm": 90,
         "valence": 0.71, "danceability": 0.54, "acousticness": 0.89},
    ]


# ── load_songs tests ─────────────────────────────────────

class TestLoadSongs:
    def test_returns_list(self):
        songs = load_songs(CSV_PATH)
        assert isinstance(songs, list)

    def test_loads_all_rows(self):
        songs = load_songs(CSV_PATH)
        assert len(songs) == 18

    def test_each_item_is_dict(self):
        songs = load_songs(CSV_PATH)
        for song in songs:
            assert isinstance(song, dict)

    def test_numeric_fields_are_converted(self):
        songs = load_songs(CSV_PATH)
        first = songs[0]
        assert isinstance(first["id"], int)
        assert isinstance(first["tempo_bpm"], int)
        assert isinstance(first["energy"], float)
        assert isinstance(first["valence"], float)
        assert isinstance(first["danceability"], float)
        assert isinstance(first["acousticness"], float)

    def test_string_fields_remain_strings(self):
        songs = load_songs(CSV_PATH)
        first = songs[0]
        assert isinstance(first["title"], str)
        assert isinstance(first["artist"], str)
        assert isinstance(first["genre"], str)
        assert isinstance(first["mood"], str)

    def test_has_expected_keys(self):
        songs = load_songs(CSV_PATH)
        expected_keys = {"id", "title", "artist", "genre", "mood",
                         "energy", "tempo_bpm", "valence", "danceability",
                         "acousticness"}
        assert set(songs[0].keys()) == expected_keys


# ── score_song tests ─────────────────────────────────────

class TestScoreSong:
    def test_returns_tuple_of_float_and_list(self):
        score, reasons = score_song(SAMPLE_PREFS, SAMPLE_SONG)
        assert isinstance(score, float)
        assert isinstance(reasons, list)
        for r in reasons:
            assert isinstance(r, str)

    def test_perfect_match_score(self):
        """A song matching genre, mood, energy exactly with 0.0 acousticness should score 7.5."""
        perfect_song = {
            "genre": "pop", "mood": "happy", "energy": 0.80,
            "acousticness": 0.0,
        }
        prefs = {
            "favorite_genre": "pop", "favorite_mood": "happy",
            "target_energy": 0.80, "likes_acoustic": False,
        }
        score, _ = score_song(prefs, perfect_song)
        # genre(3.0) + mood(2.0) + energy(1.5) + acoustic(1.0) = 7.5
        assert score == 7.5

    def test_no_match_minimum_score(self):
        """A song matching nothing should still get positive energy + acoustic points."""
        song = {"genre": "metal", "mood": "dark", "energy": 0.95, "acousticness": 0.97}
        prefs = {
            "favorite_genre": "pop", "favorite_mood": "happy",
            "target_energy": 0.0, "likes_acoustic": False,
        }
        score, _ = score_song(prefs, song)
        assert score > 0
        assert score < 2.0

    def test_genre_match_adds_3_points(self):
        song_match = {**SAMPLE_SONG, "genre": "pop"}
        song_miss = {**SAMPLE_SONG, "genre": "rock"}
        score_match, _ = score_song(SAMPLE_PREFS, song_match)
        score_miss, _ = score_song(SAMPLE_PREFS, song_miss)
        assert score_match - score_miss == 3.0

    def test_mood_match_adds_2_points(self):
        song_match = {**SAMPLE_SONG, "mood": "happy"}
        song_miss = {**SAMPLE_SONG, "mood": "dark"}
        score_match, _ = score_song(SAMPLE_PREFS, song_match)
        score_miss, _ = score_song(SAMPLE_PREFS, song_miss)
        assert score_match - score_miss == 2.0

    def test_energy_perfect_match_gives_max(self):
        song = {**SAMPLE_SONG, "energy": 0.80}
        prefs = {**SAMPLE_PREFS, "target_energy": 0.80}
        score, reasons = score_song(prefs, song)
        energy_reason = [r for r in reasons if "energy" in r][0]
        assert "+1.50" in energy_reason

    def test_energy_far_apart_gives_low(self):
        song = {**SAMPLE_SONG, "energy": 0.0}
        prefs = {**SAMPLE_PREFS, "target_energy": 1.0}
        score, reasons = score_song(prefs, song)
        energy_reason = [r for r in reasons if "energy" in r][0]
        assert "+0.00" in energy_reason

    def test_likes_acoustic_true_rewards_high_acousticness(self):
        song_high = {**SAMPLE_SONG, "acousticness": 0.90}
        song_low = {**SAMPLE_SONG, "acousticness": 0.10}
        prefs = {**SAMPLE_PREFS, "likes_acoustic": True}
        score_high, _ = score_song(prefs, song_high)
        score_low, _ = score_song(prefs, song_low)
        assert score_high > score_low

    def test_likes_acoustic_false_rewards_low_acousticness(self):
        song_high = {**SAMPLE_SONG, "acousticness": 0.90}
        song_low = {**SAMPLE_SONG, "acousticness": 0.10}
        prefs = {**SAMPLE_PREFS, "likes_acoustic": False}
        score_high, _ = score_song(prefs, song_high)
        score_low, _ = score_song(prefs, song_low)
        assert score_low > score_high

    def test_case_insensitive_genre(self):
        song = {**SAMPLE_SONG, "genre": "Pop"}
        prefs = {**SAMPLE_PREFS, "favorite_genre": "pop"}
        score, reasons = score_song(prefs, song)
        assert any("exact match" in r for r in reasons)

    def test_case_insensitive_mood(self):
        song = {**SAMPLE_SONG, "mood": "HAPPY"}
        prefs = {**SAMPLE_PREFS, "favorite_mood": "happy"}
        score, reasons = score_song(prefs, song)
        assert any("mood" in r for r in reasons)

    def test_score_never_exceeds_max(self):
        songs = load_songs(CSV_PATH)
        for song in songs:
            score, _ = score_song(SAMPLE_PREFS, song)
            assert score <= 7.5

    def test_reasons_not_empty(self):
        score, reasons = score_song(SAMPLE_PREFS, SAMPLE_SONG)
        assert len(reasons) >= 2  # at least energy + acoustic always present


# ── recommend_songs tests ────────────────────────────────

class TestRecommendSongs:
    def test_returns_list_of_tuples(self):
        catalog = make_catalog()
        results = recommend_songs(SAMPLE_PREFS, catalog, k=3)
        assert isinstance(results, list)
        for song, score, reasons in results:
            assert isinstance(song, dict)
            assert isinstance(score, float)
            assert isinstance(reasons, list)

    def test_respects_k_parameter(self):
        catalog = make_catalog()
        for k in [1, 2, 3, 4]:
            results = recommend_songs(SAMPLE_PREFS, catalog, k=k)
            assert len(results) == k

    def test_k_larger_than_catalog(self):
        catalog = make_catalog()
        results = recommend_songs(SAMPLE_PREFS, catalog, k=100)
        assert len(results) == len(catalog)

    def test_sorted_descending_by_score(self):
        catalog = make_catalog()
        results = recommend_songs(SAMPLE_PREFS, catalog, k=4)
        scores = [score for _, score, _ in results]
        assert scores == sorted(scores, reverse=True)

    def test_top_result_is_best_genre_mood_match(self):
        catalog = make_catalog()
        prefs = {"favorite_genre": "pop", "favorite_mood": "happy",
                 "target_energy": 0.80, "likes_acoustic": False}
        results = recommend_songs(prefs, catalog, k=1)
        assert results[0][0]["genre"] == "pop"

    def test_different_prefs_give_different_top(self):
        catalog = make_catalog()
        pop_prefs = {"favorite_genre": "pop", "favorite_mood": "happy",
                     "target_energy": 0.80, "likes_acoustic": False}
        lofi_prefs = {"favorite_genre": "lofi", "favorite_mood": "chill",
                      "target_energy": 0.40, "likes_acoustic": True}
        pop_top = recommend_songs(pop_prefs, catalog, k=1)[0][0]["title"]
        lofi_top = recommend_songs(lofi_prefs, catalog, k=1)[0][0]["title"]
        assert pop_top != lofi_top

    def test_scores_all_songs_in_catalog(self):
        """Every song should be scored, not just the top k."""
        catalog = make_catalog()
        results = recommend_songs(SAMPLE_PREFS, catalog, k=4)
        assert len(results) == 4


# ── OOP Recommender tests ────────────────────────────────

class TestRecommenderClass:
    def test_recommend_returns_songs_sorted_by_score(self):
        user = UserProfile(favorite_genre="pop", favorite_mood="happy",
                           target_energy=0.8, likes_acoustic=False)
        rec = make_small_recommender()
        results = rec.recommend(user, k=2)
        assert len(results) == 2
        assert results[0].genre == "pop"
        assert results[0].mood == "happy"

    def test_explain_recommendation_returns_non_empty_string(self):
        user = UserProfile(favorite_genre="pop", favorite_mood="happy",
                           target_energy=0.8, likes_acoustic=False)
        rec = make_small_recommender()
        explanation = rec.explain_recommendation(user, rec.songs[0])
        assert isinstance(explanation, str)
        assert explanation.strip() != ""
