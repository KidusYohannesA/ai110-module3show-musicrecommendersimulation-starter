# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real world recommenders like Spotify and YouTube analyze massive amounts of user behavior and audio data using machine learning to create perdictions. My version keeps uses a content-based approach that compares song features  directly against a user's stated preferences, scores each song with a weighted formula, and returns the top matches. (genre, mood, energy, acousticness)

- **Song features used:** genre, mood, energy, tempo_bpm, valence, danceability, and acousticness — loaded from `data/songs.csv` (18 songs across 14 genres)
- **UserProfile stores:** `favorite_genre`, `favorite_mood`, `target_energy`, and `likes_acoustic`
- **Scoring:** each song is scored against the user profile using four weighted rules:
  - Genre match (weight 3.0) — strongest signal for "what kind of music"
  - Mood match (weight 2.0) — refines the vibe
  - Energy fit (weight 1.5) — `1 - |song.energy - target_energy|`
  - Acoustic fit (weight 1.0) — tiebreaker for texture preference
  - Max possible score: 7.5
- **Ranking:** sort all songs by score descending, return the top k (default 5) with explanations

- **Potential biases:** Genre match carries the heaviest weight (3.0), so the system strongly favors songs in the user's stated genre and may rarely surface songs from other genres that the user might enjoy. The catalog itself is small (18 songs) and was hand-curated, meaning underrepresented genres get fewer chances to appear in results. Additionally, genre and mood are scored as exact string matches — "indie pop" and "pop" are treated as completely different, even though they overlap in practice.

See [docs/dataflow.md](docs/dataflow.md) for a Mermaid.js flowchart of the full pipeline.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Sample Output

```
==================================================
       Top 5 Recommendations
==================================================

  #1  Rooftop Lights by Indigo Parade
       Score: 7.06 / 7.50
       Reasons:
         - genre is indie pop (exact match, +3.0)
         - mood is happy (exact match, +2.0)
         - energy 0.76 vs target 0.70 (+1.41)
         - acousticness 0.35 (+0.65)
--------------------------------------------------

  #2  Sunrise City by Neon Echo
       Score: 4.14 / 7.50
       Reasons:
         - mood is happy (exact match, +2.0)
         - energy 0.82 vs target 0.70 (+1.32)
         - acousticness 0.18 (+0.82)
--------------------------------------------------

  #3  Night Drive Loop by Neon Echo
       Score: 2.21 / 7.50
       Reasons:
         - energy 0.75 vs target 0.70 (+1.42)
         - acousticness 0.22 (+0.78)
--------------------------------------------------

  #4  Binary Sunset by Glitch Throne
       Score: 2.15 / 7.50
       Reasons:
         - energy 0.88 vs target 0.70 (+1.23)
         - acousticness 0.08 (+0.92)
--------------------------------------------------

  #5  Concrete Jungle by Raw Signal
       Score: 2.12 / 7.50
       Reasons:
         - energy 0.87 vs target 0.70 (+1.24)
         - acousticness 0.12 (+0.88)
--------------------------------------------------
```

### Edge-Case Output

```
==================================================
  Profile: High-Energy Pop Fan
==================================================

  #1  Sunrise City by Neon Echo
       Score: 7.20 / 7.50
       Reasons:
         - genre is pop (exact match, +3.0)
         - mood is happy (exact match, +2.0)
         - energy 0.82 vs target 0.90 (+1.38)
         - acousticness 0.18 (+0.82)
--------------------------------------------------

  #2  Gym Hero by Max Pulse
       Score: 5.41 / 7.50
       Reasons:
         - genre is pop (exact match, +3.0)
         - energy 0.93 vs target 0.90 (+1.46)
         - acousticness 0.05 (+0.95)
--------------------------------------------------

==================================================
  Profile: Chill Lofi Listener
==================================================

  #1  Library Rain by Paper Lanterns
       Score: 7.29 / 7.50
       Reasons:
         - genre is lofi (exact match, +3.0)
         - mood is chill (exact match, +2.0)
         - energy 0.35 vs target 0.40 (+1.42)
         - acousticness 0.86 (+0.86)
--------------------------------------------------

  #2  Midnight Coding by LoRoom
       Score: 7.18 / 7.50
       Reasons:
         - genre is lofi (exact match, +3.0)
         - mood is chill (exact match, +2.0)
         - energy 0.42 vs target 0.40 (+1.47)
         - acousticness 0.71 (+0.71)
--------------------------------------------------

==================================================
  Profile: Deep Intense Rocker
==================================================

  #1  Storm Runner by Voltline
       Score: 7.31 / 7.50
       Reasons:
         - genre is rock (exact match, +3.0)
         - mood is intense (exact match, +2.0)
         - energy 0.91 vs target 0.85 (+1.41)
         - acousticness 0.10 (+0.90)
--------------------------------------------------

  #2  Gym Hero by Max Pulse
       Score: 4.33 / 7.50
       Reasons:
         - mood is intense (exact match, +2.0)
         - energy 0.93 vs target 0.85 (+1.38)
         - acousticness 0.05 (+0.95)
--------------------------------------------------
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

### Adversarial / Edge-Case Profiles

We tested profiles designed to expose weaknesses in the scoring logic:

```
==================================================
  Profile: Ghost Genre (k-pop)
==================================================

  #1  Sunrise City by Neon Echo
       Score: 4.29 / 7.50
       Reasons:
         - mood is happy (exact match, +2.0)
         - energy 0.82 vs target 0.80 (+1.47)
         - acousticness 0.18 (+0.82)
--------------------------------------------------

  #2  Rooftop Lights by Indigo Parade
       Score: 4.09 / 7.50
       Reasons:
         - mood is happy (exact match, +2.0)
         - energy 0.76 vs target 0.80 (+1.44)
         - acousticness 0.35 (+0.65)
--------------------------------------------------

==================================================
  Profile: Contradictory (Acoustic Metal)
==================================================

  #1  Neon Requiem by Pale Circuit
       Score: 6.56 / 7.50
       Reasons:
         - genre is metal (exact match, +3.0)
         - mood is dark (exact match, +2.0)
         - energy 0.95 vs target 0.95 (+1.50)
         - acousticness 0.06 (+0.06)
--------------------------------------------------

  #2  Hometown Dust by Carter Ridge
       Score: 1.61 / 7.50
       Reasons:
         - energy 0.47 vs target 0.95 (+0.78)
         - acousticness 0.83 (+0.83)
--------------------------------------------------

==================================================
  Profile: Extreme Low Energy Pop
==================================================

  #1  Sunrise City by Neon Echo
       Score: 6.09 / 7.50
       Reasons:
         - genre is pop (exact match, +3.0)
         - mood is happy (exact match, +2.0)
         - energy 0.82 vs target 0.00 (+0.27)
         - acousticness 0.18 (+0.82)
--------------------------------------------------

  #2  Gym Hero by Max Pulse
       Score: 4.05 / 7.50
       Reasons:
         - genre is pop (exact match, +3.0)
         - energy 0.93 vs target 0.00 (+0.10)
         - acousticness 0.05 (+0.95)
--------------------------------------------------
```

**Findings:**
- **Ghost Genre:** No song earns genre points — the system falls back on mood/energy/acoustic, recommending songs that have nothing to do with k-pop
- **Contradictory Preferences:** Genre+mood weight (5.0) dominates, so Neon Requiem wins despite only +0.06 acoustic — the system ignores the conflict
- **Extreme Low Energy:** Genre+mood (5.0) overpower a wildly wrong energy match — Sunrise City (energy 0.82) still beats quiet songs closer to the 0.0 target

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

