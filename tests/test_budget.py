"""Tests for budget calculations."""

from src.budget import BudgetInput, calculate_budget, calculate_percentage, determine_risk_level


def test_calculate_percentage_returns_zero_when_income_is_zero() -> None:
    """Avoid division by zero when income is not available."""
    assert calculate_percentage(100, 0) == 0.0


def test_calculate_budget_balanced_green() -> None:
    """A budget with enough remaining money and low fixed burdens is stable."""
    result = calculate_budget(
        BudgetInput(
            income=100_000,
            housing=25_000,
            food=20_000,
            transportation=5_000,
            utilities=5_000,
            debt=5_000,
            other=10_000,
        )
    )

    assert result.total_expenses == 70_000
    assert result.remaining_money == 30_000
    assert result.savings_rate == 30.0
    assert result.housing_percentage == 25.0
    assert result.debt_percentage == 5.0
    assert result.risk_level == "green"


def test_negative_remaining_money_is_red() -> None:
    """A monthly deficit is critical."""
    result = calculate_budget(
        BudgetInput(
            income=50_000,
            housing=20_000,
            food=20_000,
            transportation=8_000,
            utilities=5_000,
            debt=5_000,
            other=3_000,
        )
    )

    assert result.remaining_money < 0
    assert result.risk_level == "red"


def test_high_housing_is_yellow() -> None:
    """Housing above 40 percent of income needs attention."""
    assert determine_risk_level(
        remaining_money=20_000,
        housing_percentage=45.0,
        debt_percentage=10.0,
        savings_rate=20.0,
    ) == "yellow"


def test_high_debt_is_yellow() -> None:
    """Debt above 30 percent of income needs attention."""
    assert determine_risk_level(
        remaining_money=20_000,
        housing_percentage=30.0,
        debt_percentage=35.0,
        savings_rate=20.0,
    ) == "yellow"


def test_low_savings_is_yellow() -> None:
    """Savings below 10 percent needs attention."""
    assert determine_risk_level(
        remaining_money=5_000,
        housing_percentage=30.0,
        debt_percentage=10.0,
        savings_rate=5.0,
    ) == "yellow"
