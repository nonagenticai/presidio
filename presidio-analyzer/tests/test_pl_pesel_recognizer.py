import pytest
from presidio_analyzer.predefined_recognizers import PlPeselRecognizer

from tests import assert_result


@pytest.fixture(scope="module")
def recognizer():
    return PlPeselRecognizer()


@pytest.fixture(scope="module")
def entities():
    return ["PL_PESEL"]


@pytest.mark.parametrize(
    "text, expected_len, expected_positions",
    [
        # fmt: off
        # valid PESEL scores
        (
            "11111111114",
            1,
            ((0, 11),),
        ),
        ("My pesel is 11111111114.", 1, ((12, 23),)),
        # invalid PESEL scores
        ("1111321111", 0, ()),
        ("11110021111", 0, ()),
        # Invalid: hyphen-separated groups are not a PESEL format
        ("11-11-11-11114", 0, ()),
        # fmt: on
    ],
)
def test_when_all_pl_pesels_then_succeed(
    text, expected_len, expected_positions, recognizer, entities, max_score
):
    results = recognizer.analyze(text, entities)
    assert len(results) == expected_len
    for res, (st_pos, fn_pos) in zip(results, expected_positions):
        assert_result(res, entities[0], st_pos, fn_pos, max_score)


@pytest.mark.parametrize(
    "pesel, expected",
    [
        # Real-world and algorithmically-generated valid PESEL numbers
        ("44051401458", True),
        ("02070803628", True),
        ("11111111116", True),
        # Wrong check digit
        ("44051401459", False),
        ("85040812345", False),
        # Wrong length
        ("4405140145", False),
        ("440514014588", False),
        # Non-digit characters
        ("4405140145A", False),
        ("44-051401458", False),
    ],
)
def test_validate_result_checksum(pesel, expected, recognizer):
    assert recognizer.validate_result(pesel) is expected
