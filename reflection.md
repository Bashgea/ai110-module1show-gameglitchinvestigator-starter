# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The game had six bugs in total. The most obvious ones when first playing were that the hints were completely backwards — guessing too high told you to go higher, and guessing too low told you to go lower — and the Normal/Hard difficulty ranges were swapped (Normal had 1–100 while Hard had 1–50, the opposite of what makes sense). There was also a sneaky bug where the secret number was cast to a string on every even-numbered attempt, which made correct guesses silently fail to match. On top of that, the score logic was broken: guessing too high on even attempts *added* 5 points instead of deducting them, the win bonus formula used `attempt_number + 1` causing an unfair extra 10-point penalty, and clicking "New Game" after winning froze the game because `status`, `score`, and `history` were never reset.

---

## 2. How did you use AI as a teammate?

I used Claude Code (Claude Sonnet) as my AI assistant throughout this project.

**Correct suggestion:** Claude identified that the New Game button was broken because `st.session_state.status` was never reset back to `"playing"` after a win. It suggested adding `st.session_state.status = "playing"` (along with resetting `history` and `score`) inside the `if new_game:` block. I verified this by reading the code myself — line 141 checks `if st.session_state.status != "playing"` and calls `st.stop()`, which is exactly why the game froze. I confirmed the fix worked by winning a game and clicking New Game, which now correctly starts a fresh round.

**Incorrect/misleading suggestion:** When Claude implemented the `check_guess` TypeError fallback in `logic_utils.py`, it initially kept the string-based comparison (`"9" > "10"`) from the original buggy code. This meant that even after fixing the type-switching bug, the fallback path still gave wrong hints — `check_guess(9, "10")` returned "Too High" instead of "Too Low" because `"9" > "10"` is `True` in Python's lexicographic string ordering. I only caught this because the pytest test `test_too_low_not_flipped_by_string_comparison` failed when I ran the test suite. Without that test, the bug would have stayed hidden since it only triggers when the secret is passed as a string.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed by manually playing through the exact scenario that broke it. For the New Game bug, I won a game then clicked New Game and confirmed play resumed normally. For the type-switching bug, I traced through the code and saw that on even attempts `secret` became a string like `"42"` while `guess_int` stayed an `int`, so `42 == "42"` is always `False` in Python — a correct guess would silently be treated as wrong. For the score logic, I traced the math by hand: on attempt 1, `100 - 10 * (1 + 1) = 80` confirmed the `+1` was wrong, while `attempt_number - 1` gives 100 points for a first-guess win. Claude helped me see the even/odd `Too High` branch was also broken since guessing wrong should never reward points.

---

## 4. What did you learn about Streamlit and state?

Streamlit reruns the entire Python script from top to bottom every time the user interacts with anything — clicking a button, typing in a box, etc. Because of this, regular variables reset on every rerun, so you need `st.session_state` to store anything that should persist across interactions, like the secret number, attempt count, score, and game status. The New Game bug was a perfect example of this: forgetting to reset `st.session_state.status` meant the old "won" value survived into the new game's rerun, immediately stopping the game again. Think of session state like a small sticky notepad that Streamlit keeps between reruns, while everything else gets erased each time.

---

## 5. Looking ahead: your developer habits

- One habit I want to reuse is tracing through the math or logic of a function by hand with a concrete example (like plugging in `attempt_number = 1`) before assuming the code is right — it caught the off-by-one in the win score formula immediately.
- Next time I work with AI on a coding task, I'd ask it to explain *why* a fix works, not just what the fix is, so I understand the reasoning and can catch it if the AI is wrong.
- This project changed how I think about AI-generated code: it can produce code that looks reasonable and runs without errors but still has subtle logic bugs that only show up in specific situations, so you always need to test the edge cases yourself.
