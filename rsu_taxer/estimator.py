from pydantic import BaseModel


class TaxSummaryUS(BaseModel):
    income: float
    federal: float
    state: float
    social_security: float
    medicare: float


# Federal and California tax brackets for married filing jointly (2024)
FEDERAL_TAX_BRACKETS: list[tuple[float, float]] = [
    (0, 0.10), (23_200, 0.12), (94_300, 0.22), (201_050, 0.24),
    (383_900, 0.32), (487_450, 0.35), (731_200, 0.37)
]

CALIFORNIA_TAX_BRACKETS: list[tuple[float, float]] = [
    (0, 0.01), (20_824, 0.02), (49_368, 0.04), (77_918, 0.06),
    (108_364, 0.08), (137_500, 0.093), (708_890, 0.103),
    (850_976, 0.113), (1_701_006, 0.123)
]

MARYLAND_TAX_BRACKETS: list[tuple[float, float]] = [
    (0, 0.045), (1_000, 0.055), (2_000, 0.065), (3_000, 0.0725),
    (150_000, 0.075), (175_000, 0.0775), (225_000, 0.08),
    (300_000, 0.0825)
]

SOCIAL_SECURITY_WAGE_BASE = 168_600  # Max taxable income for SS in 2024
SOCIAL_SECURITY_RATE = 0.062
MEDICARE_RATE = 0.0145
ADDITIONAL_MEDICARE_THRESHOLD = 250_000
ADDITIONAL_MEDICARE_RATE = 0.009
MENTAL_HEALTH_SURCHARGE_THRESHOLD = 1_000_000  # CA's 1% tax above $1M


CHINA_TAX_BRACKETS: list[tuple[float, float]] = [
    (0, 0.03),
    (36_000, 0.1),
    (144_000, 0.2),
    (300_000, 0.25),
    (420_000, 0.3),
    (660_000, 0.35),
    (960_000, 0.45)
]


def compute_progressive_tax(income: float, brackets: list[tuple[float, float]]) -> float:
    """Compute progressive tax based on tax brackets."""
    tax = 0.0
    previous_bracket = 0.0

    for bracket, rate in brackets:
        if income > bracket:
            tax += (bracket - previous_bracket) * rate
            previous_bracket = bracket
        else:
            tax += (income - previous_bracket) * rate
            break

    return tax


def compute_us_tax(num_shares: int, fmv: float,
                   state: str,
                   base_income: float = 0.0) -> TaxSummaryUS:
    rsu_income = num_shares * fmv
    total_income = base_income + rsu_income

    # Compute federal tax
    federal_tax = compute_progressive_tax(total_income, FEDERAL_TAX_BRACKETS)

    # Compute California state tax
    if state == "CA":
        state_tax = compute_progressive_tax(total_income, CALIFORNIA_TAX_BRACKETS)
    elif state == "MD":
        state_tax = compute_progressive_tax(total_income, MARYLAND_TAX_BRACKETS)
    else:
        raise ValueError(f"Unknown state '{state}'")

    # Add CA mental health surcharge if applicable
    if state == "CA" and total_income > MENTAL_HEALTH_SURCHARGE_THRESHOLD:
        state_tax += (total_income - MENTAL_HEALTH_SURCHARGE_THRESHOLD) * 0.01

    # Compute Social Security tax (only applies up to $168,600)
    social_security_income = min(total_income, SOCIAL_SECURITY_WAGE_BASE)
    social_security_tax = social_security_income * SOCIAL_SECURITY_RATE

    # Compute Medicare tax
    medicare_tax = total_income * MEDICARE_RATE
    if total_income > ADDITIONAL_MEDICARE_THRESHOLD:
        medicare_tax += (total_income - ADDITIONAL_MEDICARE_THRESHOLD) * ADDITIONAL_MEDICARE_RATE

    return TaxSummaryUS(
        income=total_income,
        federal=federal_tax,
        state=state_tax,
        social_security=social_security_tax,
        medicare=medicare_tax
    )


def compute_china_tax(num_shares: int, fmv: float, base_income: float = 0.0) -> float:
    rmb = num_shares * fmv * 7.24
    return compute_progressive_tax(rmb, CHINA_TAX_BRACKETS)

