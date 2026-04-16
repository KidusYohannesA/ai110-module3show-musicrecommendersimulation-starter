# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeMusi**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
  - It suggests the top 5 songs from a small catalog based on genre, mood, energy, and acoustic preference.
- What assumptions does it make about the user  
  - It assumes the user knows their preferred genre and mood ahead of time.
- Is this for real users or classroom exploration  
  - This is for classroom exploration. The reccomendations can be used for real users but the satisfaction rate may vary.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
  - Each song has a genre, mood, energy level, and acousticness value.
- What user preferences are considered  
  - The user provides a favorite genre, favorite mood, target energy level, and whether they like acoustic music.
- How does the model turn those into a score  
  - It checks if the genre matches (worth 3.0 points), if the mood matches (worth 2.0 points), how close the energy is (up to 1.5 points), and how well the acoustic texture fits (up to 1.0 points). The max score is 7.5. It scores every song, sorts them highest to lowest, and picks the top 5.
- What changes did you make from the starter logic  
  - The starter returned an empty list. There is now a full scoring formula, added reason tracking for each score, and formatted the output to show ranked results with explanations.

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
  - 18 songs total.
- What genres or moods are represented  
  - 14 genres (pop, lofi, rock, ambient, jazz, synthwave, indie pop, r&b, electronic, country, hip-hop, classical, reggae, metal, folk) and 14 moods (happy, chill, intense, relaxed, moody, focused, romantic, energetic, nostalgic, aggressive, melancholic, peaceful, dark, warm).
- Did you add or remove data  
  - We expanded the starter catalog from 10 songs to 18 by adding 8 new tracks across underrepresented genres.
- Are there parts of musical taste missing in the dataset  
  - Yes. There is no k-pop, latin, EDM, or R&B subgenres. Most genres only have one song, so the system has very little to choose.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
  - Users who like pop, lofi, or rock get strong top results because those genres have clear matches in the catalog.
- Any patterns you think your scoring captures correctly  
  - The weighted formula correctly prioritizes genre and mood as the main signals, with energy and acousticness acting as tiebreakers. This matches how I think about music.
- Cases where the recommendations matched your intuition  
  - The Chill Lofi Listener got Library Rain and Midnight Coding as the top 2, which are lofi songs. The Deep Intense Rocker got Storm Runner.

---

## 6. Limitations and Bias 

The system uses exact string matching for genre and mood, which means closely related labels like "pop" and "indie pop" or "chill" and "relaxed" are treated as completely different, a user who likes pop will never see indie pop ranked competitively, creating a filter bubble around a single label. Additionally, 12 out of 14 genres in the catalog have only one song, so after the single genre match is found, the remaining top 5 slots are filled by songs that scored on energy and acousticness alone, which have little to do with the user's actual taste. During the adversarial experiments, the "Ghost Genre" profile (k-pop) proved that when a user's preferred genre doesn't exist in the catalog, the system silently falls back to mood and numerical features with no warning, producing recommendations that feel random.

The catalog is also too small to draw better conclusions about how the scoring logic performs. I will generate more songs across a wider range of genres and moods to better stress-test the system and reduce the bias that comes from having so few candidates per genre.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
    - Tested three standard user profiles and verified that the top result for each matched the expected song. Then ran five adversarial profiles to check how the system handles edge cases and conflicting preferences.
- What you looked for in the recommendations
    - Looked for simmilar "vibes" based on my own intuition.
- What surprised you
    - What surprised me was how our scoring logic in a way segregated the songs by genre, since genre has 3/7.5 which is roughly a 40% impact, therefore a user can miss out on similar sounding songs they might love but is in a adjacent or another genre.
- Any simple tests or comparisons you ran 
    - To verify the scoring math, the tests manually calculated the score hand and confirmed the function output matched exactly. Also tested temporarily commented out the mood check to observe how rankings shifted, this confirmed that mood is doing meaningful work separating songs within the same genre.

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
  - Use tempo, valence, and danceability in scoring since they are already being ignored.
- Better ways to explain recommendations  
  - Showin what the song is missing, not just what matched.
- Improving diversity among the top results  
  - Add a diversity penalty so the top 5 does not return all songs from the same genre. Mix in at least one song from a different genre that still scores well.
- Handling more complex user tastes  
  - Let users pick multiple genres or moods instead of just one. A user who likes both lofi and jazz should see results from both.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
    - I learned these systems are very complex in their scoring. Hand written formulas are very ineffetive unles there is a way where this formula updates on its own with the help of AI automation.
- Something unexpected or interesting you discovered
    - Something I find intresting is that my simple scoring formula is not much worse than the massive AI systems spotify and youtube use. It explains why most recommendations I received have not peaked my interest.
- How this changed the way you think about music recommendation apps
    - I learned they are purly scoring songs on predetermined metrics. The recommendations can be satisfactory but it explains why I rarely like the songs I have been reccomended on music apps.

    - I would include more metrics to improve on accuracy but I will cautin in picking too many different metrics but to do test out certin combinations that would make more sense to users.
