
import pytest
from pet_boarding import boarding_fee, admission_ok, checkout_status


# boarding_fee: pet type and day validation
def test_unknown_pet():
    with pytest.raises(ValueError):
        boarding_fee("parrot", 2, False)


def test_negative_days():
    with pytest.raises(ValueError):
        boarding_fee("cat", -1, False)


# Included days and premium conditions
def test_cat_no_extra_days():
    assert boarding_fee("cat", 3, False) == 0


def test_cat_premium_extra_days():
    assert boarding_fee("cat", 4, True) == 0


def test_rabbit_premium_extra_days():
    assert boarding_fee("rabbit", 5, True) == 20


def test_dog_extra_days():
    assert boarding_fee("dog", 4, False) == 60


# Extra days greater than 10 and nested dog condition
def test_dog_high_extra_fee():
    assert boarding_fee("dog", 14, False) == 540


def test_cat_high_extra_fee():
    assert boarding_fee("cat", 14, False) == 330


# admission_ok: senior and non-senior branches
def test_senior_enough_vaccinations():
    assert admission_ok(12, 3, True) is True


def test_senior_insufficient_vaccinations():
    assert admission_ok(12, 2, True) is False


def test_young_pet_rejected():
    assert admission_ok(0, 5, False) is False


def test_adult_enough_vaccinations():
    assert admission_ok(2, 2, False) is True


def test_adult_insufficient_vaccinations():
    assert admission_ok(2, 1, False) is False


# checkout_status: long stay, weekend, and result branches
def test_weekday_open():
    assert checkout_status(15, False, False) == "open"


def test_weekday_late():
    assert checkout_status(10, False, False) == "late"


def test_weekday_closed():
    assert checkout_status(-1, False, False) == "closed"


def test_long_stay_open():
    assert checkout_status(30, True, False) == "open"


def test_weekend_open():
    assert checkout_status(35, False, True) == "open"


def test_weekend_late():
    assert checkout_status(20, False, True) == "late"


def test_weekend_closed():
    assert checkout_status(0, False, True) == "closed"
