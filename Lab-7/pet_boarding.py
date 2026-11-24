def parse_booking(text):
    if text is None:
        raise ValueError("Input cannot be None")
    if ':' not in text:
        raise ValueError("Input must contain ':' separator (e.g. 'dog:5')")
    parts = text.split(':', 1)
    if len(parts) != 2:
        raise ValueError("Input must be in 'pet:days' format")
    pet, days = parts
    pet = pet.strip()
    if not pet:
        raise ValueError("Pet name cannot be empty")
    try:
        days_val = float(days)
    except ValueError:
        raise ValueError(f"Days must be a valid number, got: '{days}'")
    return pet.title(), days_val


def stay_average(days_csv):
    if days_csv is None:
        raise ValueError("Input cannot be None")
    days_csv = days_csv.strip()
    if not days_csv:
        raise ValueError("Input cannot be empty")
    parts = days_csv.split(',')
    values = []
    for r in parts:
        r = r.strip()
        if not r:
            raise ValueError(f"Empty value found in CSV: '{days_csv}'")
        try:
            values.append(int(r))
        except ValueError:
            raise ValueError(f"Non-integer value in CSV: '{r}'")
    if not values:
        raise ValueError("No valid integers found in CSV")
    return sum(values) // len(values)


def payable_fee(text):
    if text is None:
        raise ValueError("Input cannot be None")
    if '|' not in text:
        raise ValueError("Input must contain '|' separator (e.g. '1500|100')")
    parts = text.split('|', 1)
    if len(parts) != 2:
        raise ValueError("Input must be in 'fee|discount' format")
    fee_str, discount_str = parts
    try:
        fee = float(fee_str)
    except ValueError:
        raise ValueError(f"Fee must be a valid number, got: '{fee_str}'")
    try:
        discount = float(discount_str)
    except ValueError:
        raise ValueError(f"Discount must be a valid number, got: '{discount_str}'")
    total = fee * 1.18 - discount
    return max(total, 0)


def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter pet:days (e.g. dog:5): ")
    try:
        result = parse_booking(user_input)
        print("Pet and Days:", result)
    except ValueError as e:
        print(f"Error: {e}")

    print("\n==== Running stay_average ====")
    user_input = input("Enter stay lengths in days as CSV (e.g. 2,5,7): ")
    try:
        result = stay_average(user_input)
        print("Average Stay:", result)
    except ValueError as e:
        print(f"Error: {e}")

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 1500|100): ")
    try:
        result = payable_fee(user_input)
        print("Payable Fee:", result)
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
