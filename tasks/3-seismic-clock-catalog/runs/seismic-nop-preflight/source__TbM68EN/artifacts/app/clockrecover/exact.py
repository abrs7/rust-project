"""Exact arithmetic required by the public contract."""


def round_half_away(numerator: int, denominator: int) -> int:
    """Round an exact rational value, with ties away from zero."""
    if denominator <= 0:
        raise ValueError("denominator must be positive")
    sign = -1 if numerator < 0 else 1
    magnitude = abs(numerator)
    quotient, remainder = divmod(magnitude, denominator)
    if 2 * remainder >= denominator:
        quotient += 1
    return sign * quotient
