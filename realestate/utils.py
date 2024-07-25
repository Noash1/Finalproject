

def convert_currency(in_amount, in_currency="EUR", out_currency="USD"):
    if in_currency == "EUR" and out_currency == "USD":
        return in_amount * 1.08
    elif in_currency == "USD" and out_currency == "EUR":
        return in_amount / 1.08

    return in_amount
