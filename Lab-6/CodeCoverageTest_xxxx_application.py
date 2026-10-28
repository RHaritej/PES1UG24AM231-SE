
import pytest
from pet_boarding import boarding_fee, admission_ok, checkout_status


# boarding_fee tests
def test_unknown_pet():
    with pytest.raises(ValueError, match="unknown pet type"):
        boarding_fee("parrot", 3, False)


def test_negative_days():
    with pytest.raises(ValueError, match="invalid days"):
        boarding_fee("cat", -1, False)


def test_within_included_days():
    assert boarding_fee("dog", 1, False) == 0


def test_premium_boarding():
    assert boarding_fee("dog", 4, True) == 30


def test_rabbit_boarding():
    assert boarding_fee("rabbit", 6, True) == 40


def test_cat_extra_days():
    assert boarding_fee("cat", 5, False) == 40


def test_dog_more_than_ten_extra_days():
    assert boarding_fee("dog", 14, False) == 540


def test_cat_more_than_ten_extra_days():
    assert boarding_fee("cat", 14, False) == 330


# admission_ok tests
def test_admission_ok():
    assert admission_ok(4, 2, False) is True


def test_young_pet_rejected():
    assert admission_ok(0, 5, False) is False


def test_senior_pet_accepted():
    assert admission_ok(10, 3, True) is True


def test_senior_pet_rejected():
    assert admission_ok(10, 2, True) is False


# checkout_status tests
def test_checkout_open():
    assert checkout_status(20, False, False) == "open"


def test_checkout_late():
    assert checkout_status(10, False, False) == "late"


def test_checkout_closed():
    assert checkout_status(-1, False, False) == "closed"


def test_weekend_checkout():
    assert checkout_status(35, False, True) == "open"


def test_long_stay_checkout():
    assert checkout_status(30, True, False) == "open"
