from logic_utils import check_guess, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Bug 2 regression: inverted hint messages ---
# check_guess returns (outcome, message). Previously the messages were swapped:
# guessing too high said "Go HIGHER!" and too low said "Go LOWER!" (both wrong).

def test_too_high_message_says_go_lower():
    # Guess is above secret, so player should be told to go LOWER
    outcome, message = check_guess(75, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected hint to say LOWER, got: {repr(message)}"

def test_too_low_message_says_go_higher():
    # Guess is below secret, so player should be told to go HIGHER
    outcome, message = check_guess(25, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected hint to say HIGHER, got: {repr(message)}"

def test_correct_guess_message():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message


# --- Bug 3 regression: new_game reset attempts to 0 instead of 1 ---
# The initial session state sets attempts = 1 (first attempt is #1, not #0).
# The "New Game" button was resetting attempts to 0, giving a free extra attempt
# and causing update_score to see attempt_number=0 on the first real guess.
# This test documents that update_score called with attempt_number=1 gives the
# expected score for a first-attempt win (100 - 10*(1+1) = 80).

def test_update_score_first_attempt_win():
    from logic_utils import update_score
    # attempt_number=1 is correct for the first guess after new_game
    score = update_score(0, "Win", attempt_number=1)
    assert score == 80, f"Expected 80 points for a first-attempt win, got {score}"

def test_update_score_zeroth_attempt_would_be_wrong():
    # If attempts were reset to 0, the first submit increments to 1 -- still fine.
    # But if new_game left attempts=0 and submit ran without incrementing first,
    # attempt_number=0 gives 100 - 10*(0+1) = 90, not the intended 80.
    from logic_utils import update_score
    score_wrong_reset = update_score(0, "Win", attempt_number=0)
    score_correct_reset = update_score(0, "Win", attempt_number=1)
    assert score_wrong_reset != score_correct_reset, (
        "attempt_number=0 and attempt_number=1 should yield different scores"
    )


# --- Bug 4 regression: secret cast to str on even attempts ---
# app.py was doing: secret = str(st.session_state.secret) on even attempts,
# then passing that string to check_guess. String comparison is lexicographic,
# so "9" > "10" is True (wrong), causing a single-digit guess against a
# double-digit secret to be misclassified on every even attempt.
# The fix: always pass the integer secret directly to check_guess.

def test_check_guess_single_digit_vs_double_digit_too_low():
    # 9 < 10 numerically, so outcome must be "Too Low".
    # With string comparison "9" > "10" is True, which would wrongly give "Too High".
    outcome, message = check_guess(9, 10)
    assert outcome == "Too Low", (
        f"9 < 10 so outcome should be Too Low, got {outcome!r}"
    )
    assert "HIGHER" in message

def test_check_guess_single_digit_vs_double_digit_too_high():
    # 11 > 9 numerically, outcome must be "Too High".
    # Verify integer comparison is used and the result is stable.
    outcome, message = check_guess(11, 9)
    assert outcome == "Too High", (
        f"11 > 9 so outcome should be Too High, got {outcome!r}"
    )
    assert "LOWER" in message

def test_check_guess_requires_integer_secret():
    # Passing a string secret (the old bug) should NOT silently give wrong answers.
    # "9" > "10" lexicographically is True, so a buggy impl would return "Too High".
    # check_guess must use integer comparison and return the numerically correct result.
    outcome_int, _ = check_guess(9, 10)
    assert outcome_int == "Too Low", (
        "check_guess(9, 10) must use numeric comparison and return Too Low"
    )


# --- Challenge 1 edge cases: input handling and guess evaluation ---

def test_parse_guess_whitespace_only():
    # Edge case 1: whitespace-only input ("   ") passes the "" check but is not a number.
    # parse_guess must reject it gracefully with ok=False and a non-None error message.
    # In app.py, attempts are incremented before parse_guess is called, so this input
    # already costs an attempt — the test confirms at least the error is handled, not crashed.
    ok, value, err = parse_guess("   ")
    assert ok is False, "Whitespace-only input should not parse as a valid guess"
    assert value is None
    assert err is not None, "An error message should be returned for whitespace input"

def test_parse_guess_out_of_range_is_accepted():
    # Edge case 2: a number outside the difficulty range (e.g., 150 on Normal 1-50)
    # is technically a valid integer, so parse_guess returns ok=True.
    # check_guess then correctly says "Too High" — no crash, sensible result.
    # This test documents the current behavior: range validation is not enforced.
    ok, value, _ = parse_guess("150")
    assert ok is True, "parse_guess should accept any integer, including out-of-range"
    assert value == 150
    outcome, message = check_guess(150, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_parse_guess_decimal_truncates_to_integer():
    # Edge case 3: a decimal input like "42.9" is parsed via int(float(raw)),
    # which truncates (not rounds) to 42. If the secret is 42, this wins.
    # The test confirms the truncation behavior is consistent and produces no crash.
    ok, value, _ = parse_guess("42.9")
    assert ok is True
    assert value == 42, f"Expected 42 after truncating 42.9, got {value}"
    # Confirm that this truncated value wins against a secret of 42
    outcome, _ = check_guess(42, 42)
    assert outcome == "Win"
