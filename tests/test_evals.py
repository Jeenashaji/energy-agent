import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "evals"))
from run_evals import grade  # noqa: E402


def test_numeric_answer_within_one_percent():
    assert grade("The average price was 81.6 EUR/MWh.", "81.61") == "pass"
    assert grade("The average price was 95 EUR/MWh.", "81.61") == "FAIL"


def test_text_answer():
    assert grade("That date is not in the data.", "not in the data") == "pass"


def test_empty_expected_is_not_graded():
    assert grade("anything", "") == "not graded"
