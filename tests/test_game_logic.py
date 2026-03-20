from logic_utils import check_guess, get_range_for_difficulty, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Bug fix: hints were backwards ---
# Original bug: "Too High" said "Go HIGHER!" and "Too Low" said "Go LOWER!"

def test_too_high_message_says_go_lower():
    # Guess is above the secret, so player should be told to go LOWER
    outcome, message = check_guess(60, 50)
    assert "LOWER" in message, f"Expected 'LOWER' in hint but got: {message}"

def test_too_low_message_says_go_higher():
    # Guess is below the secret, so player should be told to go HIGHER
    outcome, message = check_guess(40, 50)
    assert "HIGHER" in message, f"Expected 'HIGHER' in hint but got: {message}"


# --- Bug fix: secret type-switching on even attempts ---
# Original bug: secret was cast to str() on even attempts, breaking numeric comparison.
# "9" > "10" is True in string comparison (lexicographic), so guess=9 vs secret=10
# incorrectly returned "Too High" instead of "Too Low".

def test_correct_guess_with_string_secret_still_wins():
    # Even if secret is passed as a string (as the bug did), a correct int guess should win
    outcome, _ = check_guess(42, "42")
    assert outcome == "Win"

def test_too_low_not_flipped_by_string_comparison():
    # 9 < 10, but "9" > "10" lexicographically — outcome must be "Too Low"
    outcome, _ = check_guess(9, "10")
    assert outcome == "Too Low", f"Expected 'Too Low' but got: {outcome}"


# --- Bug fix: Normal and Hard difficulty ranges were swapped ---
# Original bug: Normal returned (1, 100) and Hard returned (1, 50)

def test_normal_difficulty_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1 and high == 50, f"Normal should be 1–50, got {low}–{high}"

def test_hard_difficulty_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1 and high == 100, f"Hard should be 1–100, got {low}–{high}"

def test_easy_difficulty_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1 and high == 20, f"Easy should be 1–20, got {low}–{high}"


# --- Bug fix: win score formula used attempt_number + 1 instead of attempt_number - 1 ---
# Original bug: first-attempt win gave 100 - 10*(1+1) = 80 instead of 100

def test_win_on_first_attempt_gives_max_score():
    score = update_score(0, "Win", 1)
    assert score == 100, f"Win on attempt 1 should give 100 pts, got {score}"

def test_win_on_second_attempt_gives_90():
    score = update_score(0, "Win", 2)
    assert score == 90, f"Win on attempt 2 should give 90 pts, got {score}"

def test_win_score_never_goes_below_10():
    # Even on a very late attempt, minimum win bonus is 10
    score = update_score(0, "Win", 20)
    assert score >= 10, f"Win score floor should be 10, got {score}"


# --- Bug fix: Too High gave +5 points on even attempts ---
# Original bug: even attempt_number with "Too High" outcome added 5 pts instead of deducting

def test_too_high_always_deducts_points_on_even_attempt():
    score = update_score(50, "Too High", 2)
    assert score == 45, f"Too High on even attempt should deduct 5, got {score}"

def test_too_high_always_deducts_points_on_odd_attempt():
    score = update_score(50, "Too High", 3)
    assert score == 45, f"Too High on odd attempt should deduct 5, got {score}"

def test_too_low_always_deducts_points():
    score = update_score(50, "Too Low", 2)
    assert score == 45, f"Too Low should always deduct 5, got {score}"
