"""Exact arithmetic required by the public contract."""


def round_half_even(numerator: int, denominator: int) -> int:
    """Round an exact rational value, with ties to even."""
    if denominator <= 0:
        raise ValueError("denominator must be positive")
    sign = -1 if numerator < 0 else 1
    magnitude = abs(numerator)
    quotient, remainder = divmod(magnitude, denominator)
    doubled = remainder * 2
    if doubled > denominator or (doubled == denominator and quotient & 1):
        quotient += 1
    return sign * quotient
