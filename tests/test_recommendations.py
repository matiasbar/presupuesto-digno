"""Tests for Spanish recommendation messages."""

from src.budget import BudgetResult
from src.recommendations import build_recommendations


def test_deficit_recommendation() -> None:
    """A deficit should produce a critical recommendation."""
    messages = build_recommendations(
        BudgetResult(
            total_expenses=120_000,
            remaining_money=-20_000,
            savings_rate=-20.0,
            housing_percentage=35.0,
            debt_percentage=10.0,
            risk_level="red",
        )
    )

    assert any("déficit" in message for message in messages)


def test_high_housing_recommendation() -> None:
    """High housing percentage should be mentioned."""
    messages = build_recommendations(
        BudgetResult(
            total_expenses=85_000,
            remaining_money=15_000,
            savings_rate=15.0,
            housing_percentage=45.0,
            debt_percentage=10.0,
            risk_level="yellow",
        )
    )

    assert any("alquiler" in message for message in messages)


def test_high_debt_recommendation() -> None:
    """High debt percentage should be mentioned."""
    messages = build_recommendations(
        BudgetResult(
            total_expenses=85_000,
            remaining_money=15_000,
            savings_rate=15.0,
            housing_percentage=30.0,
            debt_percentage=35.0,
            risk_level="yellow",
        )
    )

    assert any("deudas" in message for message in messages)


def test_low_savings_recommendation() -> None:
    """Low savings should produce a gradual savings recommendation."""
    messages = build_recommendations(
        BudgetResult(
            total_expenses=95_000,
            remaining_money=5_000,
            savings_rate=5.0,
            housing_percentage=30.0,
            debt_percentage=10.0,
            risk_level="yellow",
        )
    )

    assert any("ahorro" in message for message in messages)


def test_balanced_budget_recommendation() -> None:
    """A healthy budget should suggest an emergency fund."""
    messages = build_recommendations(
        BudgetResult(
            total_expenses=70_000,
            remaining_money=30_000,
            savings_rate=30.0,
            housing_percentage=25.0,
            debt_percentage=5.0,
            risk_level="green",
        )
    )

    assert messages == [
        "Tu presupuesto está balanceado. Intentá construir un fondo de emergencia "
        "equivalente a 1 mes de gastos."
    ]
