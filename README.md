# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Game Purpose:**
A number guessing game where the player picks a difficulty (Easy: 1–20, Normal: 1–50, Hard: 1–100), then tries to guess the secret number within a limited number of attempts. Each guess earns or deducts points, and hints tell you whether to go higher or lower.

**Bugs Found:**
1. **Hints were backwards** — "Too High" said "Go HIGHER!" and "Too Low" said "Go LOWER!", which is the opposite of what the player needs.
2. **Normal/Hard difficulty ranges were swapped** — Normal used 1–100 and Hard used 1–50 instead of the other way around.
3. **Secret number type-switching** — On even-numbered attempts, the secret was cast to a string, causing correct guesses to silently fail and numeric comparisons to use lexicographic ordering.
4. **Win score formula off by one** — Used `attempt_number + 1` instead of `attempt_number - 1`, unfairly docking 10 extra points even on a first-guess win.
5. **"Too High" gave points on even attempts** — The score function added +5 for a wrong guess when `attempt_number % 2 == 0`, instead of always deducting.
6. **New Game button broken after winning** — `st.session_state.status` was never reset to `"playing"`, so the game froze on the win screen permanently.

**Fixes Applied:**
- Corrected hint messages in `check_guess` so "Too High" → "Go LOWER!" and "Too Low" → "Go HIGHER!"
- Swapped the ranges in `get_range_for_difficulty` so Hard is 1–100 and Normal is 1–50.
- Removed the type-switching code that was casting the secret to a string on even attempts.
- Fixed the TypeError fallback in `check_guess` to convert the secret back to `int` for numeric comparison instead of using string ordering.
- Fixed the win score formula to `100 - 10 * (attempt_number - 1)`.
- Removed the even/odd branch in `update_score` so "Too High" always deducts 5 points.
- Added `st.session_state.status = "playing"`, `st.session_state.score = 0`, and `st.session_state.history = []` to the New Game handler.

## 📸 Demo

- [created images folder that contains proof] [Insert a screenshot of your fixed, winning game here]

**pytest results (16 tests passing):**

- [ created images folder that contains proof] [Insert a screenshot of your pytest terminal output here]

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
