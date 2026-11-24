from hypothesis import given, strategies as st
from pet_boarding import parse_booking, stay_average, payable_fee

@given(st.text() | st.none())
def test_parse_booking_no_crash(s):
    try:
        parse_booking(s)
    except ValueError:
        pass  # Expected for invalid input — not a crash
    except Exception as e:
        assert False, f"parse_booking crashed unexpectedly with: {type(e).__name__}: {e}"

@given(st.text() | st.none())
def test_stay_average_no_crash(s):
    try:
        stay_average(s)
    except ValueError:
        pass  # Expected for invalid input — not a crash
    except Exception as e:
        assert False, f"stay_average crashed unexpectedly with: {type(e).__name__}: {e}"

@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
    try:
        payable_fee(s)
    except ValueError:
        pass  # Expected for invalid input — not a crash
    except Exception as e:
        assert False, f"payable_fee crashed unexpectedly with: {type(e).__name__}: {e}"
